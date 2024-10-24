from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, Http404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator

from home.models import (
    get_latest_blog_posts,
    BlogPost,
    BlogPostComment,
)
from home.forms import BlogPostForm
from home.constants import (
    MAX_BLOG_POSTS_ON_HOME_PAGE,
    MAX_BLOG_POSTS_ON_BLOG_PAGE,
    BLOG_POST_COMMENTS_PER_PAGE,
)


def home(request: HttpRequest):
    """Endpoint for viewing the home page of the website."""
    latest_posts = get_latest_blog_posts(end_index=MAX_BLOG_POSTS_ON_HOME_PAGE)
    return render(request, "home/home.html", {"latest_posts": latest_posts})


def about(request: HttpRequest):
    """Endpoint for viewing information about me."""
    return render(request, "home/about.html")


def blog_post(request: HttpRequest, id: int):
    """Endpoint for checking an individual blog post."""
    blog_post = get_object_or_404(BlogPost, pk=id)
    paginator = Paginator(
        BlogPostComment.objects.filter(blog_post=blog_post).order_by("-created_date"),
        BLOG_POST_COMMENTS_PER_PAGE,
    )

    page = request.GET.get("page", 1)
    comments = paginator.get_page(page)

    page_number = comments.number
    if not comments.count == 0:
        if page_number < 1:
            raise Http404(
                f"Comments for blog post do not exist on page {comments.number}"
            )
        elif page_number > paginator.num_pages:
            raise Http404(
                f"Comments for blog post do not exist on page {comments.number}"
            )

    return render(
        request,
        "home/blog_post.html",
        {
            "blog_post": blog_post,
            "comments": comments,
        },
    )


class BlogPosts(ListView):
    """View for viewing all the blog posts."""

    paginate_by = MAX_BLOG_POSTS_ON_BLOG_PAGE
    model = BlogPost
    ordering = ["-published_date"]
    template_name = "home/blog.html"


class EditBlogPost(PermissionRequiredMixin, View):
    """View to edit individual blog post."""

    permission_required = "home.can_edit"

    def get(self, request: HttpRequest, id: int):
        """GET Endpoint for editing an individual blog post."""
        blog_post = get_object_or_404(BlogPost, pk=id)
        form = BlogPostForm({"title": blog_post.title, "content": blog_post.content})
        return render(
            request, "home/blog_post_edit.html", {"blog_post": blog_post, "form": form}
        )

    def post(self, request: HttpRequest, id: int):
        """POST endpoint for submitting individual blog post edit."""
        form = BlogPostForm(request.POST)
        post = get_object_or_404(BlogPost, pk=id)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            post.title = title
            post.content = content
            post.edited_date = now()
            post.save()
            return redirect(reverse("blog_post", args=[id]))
        return render(request, "home/blog_post_edit.html", {"form": form})


class DeleteBlogPost(PermissionRequiredMixin, View):
    """View to delete individual blog post."""

    permission_required = "home.can_remove"

    def get(self, request: HttpRequest, id: int):
        """GET Endpoint for deleting an individual blog post."""
        blog_post = get_object_or_404(BlogPost, pk=id)
        return render(request, "home/blog_post_delete.html", {"blog_post": blog_post})

    def post(self, _: HttpRequest, id: int):
        """POST Endpoint for submitting blog post deletion."""
        post = get_object_or_404(BlogPost, pk=id)
        post.delete()
        return redirect(reverse("blog"))


class PublishBlogPost(PermissionRequiredMixin, View):
    """View to publish a new blog post."""

    permission_required = "home.can_publish"

    def get(self, request: HttpRequest):
        """GET Endpoint for publishing a new blog post."""
        form = BlogPostForm()
        return render(request, "home/blog_post_publish.html", {"form": form})

    def post(self, request: HttpRequest):
        """POST Endpoint for submitting created blog post."""
        form = BlogPostForm(request.POST)
        if form.is_valid():
            data = {
                "title": form.cleaned_data["title"],
                "content": form.cleaned_data["content"],
                "published_date": now(),
                "author": request.user,
            }
            blog_post = BlogPost.objects.create(**data)
            blog_post.save()
            return redirect(reverse("blog"))
        return render(request, "home/blog_post_publish.html", {"form": form})

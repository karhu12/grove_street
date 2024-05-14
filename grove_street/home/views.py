from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, Http404
from django.views import View
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.mixins import PermissionRequiredMixin

from home.models import get_latest_blog_posts, BlogPost
from home.forms import BlogPostForm
from home.constants import MAX_BLOG_POSTS_ON_HOME_PAGE, MAX_BLOG_POSTS_ON_BLOG_PAGE

# GET


def home(request: HttpRequest):
    """Endpoint for viewing the home page of the website."""
    latest_posts = get_latest_blog_posts(end_index=MAX_BLOG_POSTS_ON_HOME_PAGE)
    return render(request, "home/home.html", {"latest_posts": latest_posts})


def about(request: HttpRequest):
    """Endpoint for viewing information about me."""
    return render(request, "home/about.html")


def blog(request: HttpRequest, page: int = 1):
    """Endpoint for viewing all blog posts."""
    if page < 1:
        raise Http404("Page number can not be lower than 1.")

    end_index = MAX_BLOG_POSTS_ON_BLOG_PAGE * page
    start_index = end_index - MAX_BLOG_POSTS_ON_BLOG_PAGE
    latest_posts = get_latest_blog_posts(start_index, end_index)
    return render(
        request,
        "home/blog.html",
        {
            "latest_posts": latest_posts,
            "previous_page": page - 1,
            "page": page,
            "next_page": page + 1,
        },
    )


def blog_post(request: HttpRequest, id: int):
    """Endpoint for checking an individual blog post."""
    blog_post = get_object_or_404(BlogPost, pk=id)
    return render(request, "home/blog_post.html", {"blog_post": blog_post})


class BlogPostEditView(PermissionRequiredMixin, View):
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


class BlogPostDeleteView(PermissionRequiredMixin, View):
    """View to delete individual blog post."""

    permission_required = "home.can_delete"

    def get(self, request: HttpRequest, id: int):
        """GET Endpoint for deleting an individual blog post."""
        blog_post = get_object_or_404(BlogPost, pk=id)
        return render(request, "home/blog_post_delete.html", {"blog_post": blog_post})

    def post(self, _: HttpRequest, id: int):
        """POST Endpoint for submitting blog post deletion."""
        post = get_object_or_404(BlogPost, pk=id)
        post.delete()
        return redirect(reverse("blog"))


# POST


def publish_blog_post(request: HttpRequest):
    pass

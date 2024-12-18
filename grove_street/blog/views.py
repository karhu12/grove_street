from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, Http404
from django.views import View
from django.views.generic import ListView
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator

from blog.models import (
    BlogPost,
    BlogPostComment,
)
from blog.forms import BlogPostForm, BlogPostCommentForm
from blog.constants import (
    MAX_BLOG_POSTS_ON_BLOG_PAGE,
    BLOG_POST_COMMENTS_PER_PAGE,
)


class IndividualBlogPost(View):
    """View for checking an individual blog post."""

    def get(self, request: HttpRequest, id: int, form: BlogPostCommentForm = None):
        """Endpoint for rendering an individual blog post."""
        blog_post = get_object_or_404(BlogPost, pk=id)
        paginator = Paginator(
            BlogPostComment.objects.filter(blog_post=blog_post).order_by(
                "-created_date"
            ),
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

        if form is None:
            form = BlogPostCommentForm()

        return render(
            request,
            "blog/blog_post.html",
            {
                "blog_post": blog_post,
                "comments": comments,
                "form": form,
            },
        )

    def post(self, request: HttpRequest, id: int):
        """Endpoint for leaving a comment for an inidividual blog post."""
        form = BlogPostCommentForm(request.POST)

        if not request.user.has_perm("blog.can_comment"):
            form.add_error(None, "User has no permission to post a comment.")
            return self.get(request, id, form)

        if form.is_valid():
            content = form.cleaned_data["content"]
            data = {
                "blog_post": get_object_or_404(BlogPost, pk=id),
                "author": request.user,
                "created_date": now(),
                "content": content,
            }
            comment = BlogPostComment.objects.create(**data)
            comment.save()

        return self.get(request, id, form)


class BlogPosts(ListView):
    """View for viewing all the blog posts."""

    paginate_by = MAX_BLOG_POSTS_ON_BLOG_PAGE
    model = BlogPost
    ordering = ["-published_date"]
    template_name = "blog/blog.html"


class EditBlogPost(PermissionRequiredMixin, View):
    """View to edit individual blog post."""

    permission_required = "blog.can_edit"

    def get(self, request: HttpRequest, id: int, form: BlogPostForm | None = None):
        """GET Endpoint for editing an individual blog post."""
        blog_post = get_object_or_404(BlogPost, pk=id)

        if form is None:
            form = BlogPostForm(
                {"title": blog_post.title, "content": blog_post.content}
            )

        return render(
            request, "blog/blog_post_edit.html", {"blog_post": blog_post, "form": form}
        )

    def post(self, request: HttpRequest, id: int):
        """POST endpoint for submitting individual blog post edit."""
        form = BlogPostForm(request.POST)
        blog_post = get_object_or_404(BlogPost, pk=id)

        if not request.user.has_perm("blog.can_edit"):
            form.add_error(None, "User has no permission to edit a blog post.")
            return render(
                request,
                "blog/blog_post_edit.html",
                {"blog_post": blog_post, "form": form},
            )

        if form.is_valid() and request.user.has_perm("blog.can_edit"):
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            blog_post.title = title
            blog_post.content = content
            blog_post.edited_date = now()
            blog_post.save()
            return redirect(reverse("blog_post", args=[id]))

        return render(
            request, "blog/blog_post_edit.html", {"blog_post": blog_post, "form": form}
        )


class DeleteBlogPost(PermissionRequiredMixin, View):
    """View to delete individual blog post."""

    permission_required = "blog.can_remove"

    def get(self, request: HttpRequest, id: int):
        """GET Endpoint for deleting an individual blog post."""
        blog_post = get_object_or_404(BlogPost, pk=id)
        return render(request, "blog/blog_post_delete.html", {"blog_post": blog_post})

    def post(self, request: HttpRequest, id: int):
        """POST Endpoint for submitting blog post deletion."""
        if request.user.has_perm("blog.can_remove"):
            post = get_object_or_404(BlogPost, pk=id)
            post.delete()
        return redirect(reverse("blog"))


class PublishBlogPost(PermissionRequiredMixin, View):
    """View to publish a new blog post."""

    permission_required = "blog.can_publish"

    def get(self, request: HttpRequest):
        """GET Endpoint for publishing a new blog post."""
        form = BlogPostForm()
        return render(request, "blog/blog_post_publish.html", {"form": form})

    def post(self, request: HttpRequest):
        """POST Endpoint for submitting created blog post."""
        form = BlogPostForm(request.POST)
        if form.is_valid() and request.user.has_perm("blog.can_publish"):
            data = {
                "title": form.cleaned_data["title"],
                "content": form.cleaned_data["content"],
                "published_date": now(),
                "author": request.user,
            }
            blog_post = BlogPost.objects.create(**data)
            blog_post.save()
            return redirect(reverse("blog"))
        return render(request, "blog/blog_post_publish.html", {"form": form})

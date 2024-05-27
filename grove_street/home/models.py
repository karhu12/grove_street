from typing import Optional

from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    """Model that represents a blog post that users can publish."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField("Published date")
    edited_date = models.DateTimeField("Edited date", blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_publish", "Can publish new blog posts."),
            ("can_edit", "Can modify existing blog posts."),
            ("can_remove", "Can remove existing blog posts."),
            ("can_comment", "Can comment on blog posts."),
        ]

        constraints = [
            models.CheckConstraint(
                check=(~models.Q(title="")), name="blog_post_title_populated"
            ),
            models.CheckConstraint(
                check=(~models.Q(content="")), name="blog_post_content_populated"
            ),
        ]


def get_latest_blog_posts(
    start_index: Optional[int] = None, end_index: Optional[int] = None
) -> Optional[models.QuerySet[BlogPost]]:
    """Get latest blog posts.

    Args:
        start_index: Start index of returned posts.
        end_index: End index of returned posts.
    Returns:
        Latest blog posts (Or None if none found).
    """
    try:
        blog_posts = BlogPost.objects.order_by("-published_date")
        if start_index is not None or end_index is not None:
            blog_posts = blog_posts[start_index:end_index]
    except BlogPost.DoesNotExist:
        blog_posts = None
    return blog_posts


class BlogPostComment(models.Model):
    """Model that represents comment that users can leave for blog posts."""

    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField("Created date")
    edited_date = models.DateTimeField("Edited date", blank=True, null=True)
    content = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(~models.Q(content="")),
                name="blog_post_comment_content_populated",
            ),
        ]


def get_latest_blog_post_comments(
    blog_post_id: int,
    start_index: Optional[int] = None,
    end_index: Optional[int] = None,
) -> Optional[models.QuerySet[BlogPostComment]]:
    """Get latest comments for given blog post.

    Args:
        blog_post_id: Blog post id which to fetch comments for.
        start_index: Start index of returned posts.
        end_index: End index of returned posts.
    Returns:
        Latest blog post comments (Or None if none found).
    """

from typing import Optional

from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField("Published date")
    title = models.CharField(max_length=100)
    content = models.TextField()
    edited_date = models.DateTimeField("Edited date", blank=True, null=True)

    class Meta:
        permissions = [
            ("can_publish", "Can publish new blog posts."),
            ("can_edit", "Can modify existing blog posts."),
            ("can_remove", "Can remove existing blog posts."),
        ]

        constraints = [
            models.CheckConstraint(check=(~models.Q(title="")), name="title_populated"),
            models.CheckConstraint(
                check=(~models.Q(content="")), name="content_populated"
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

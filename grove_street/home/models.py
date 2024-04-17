from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    published_date = models.DateTimeField("Published date")
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        permissions = [
            ("can_publish", "Can publish new blog posts."),
            ("can_edit", "Can modify existing blog posts."),
            ("can_remove", "Can remove existing blog posts."),
        ]

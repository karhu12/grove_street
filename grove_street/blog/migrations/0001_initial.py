# Generated by Django 5.1.3 on 2024-11-19 12:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("published_date", models.DateTimeField(verbose_name="Published date")),
                (
                    "edited_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Edited date"
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("can_publish", "Can publish new blog posts."),
                    ("can_edit", "Can modify existing blog posts."),
                    ("can_remove", "Can remove existing blog posts."),
                    ("can_comment", "Can comment on blog posts."),
                ],
            },
        ),
        migrations.CreateModel(
            name="BlogPostComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_date", models.DateTimeField(verbose_name="Created date")),
                (
                    "edited_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Edited date"
                    ),
                ),
                ("content", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "blog_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.blogpost"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="blogpost",
            constraint=models.CheckConstraint(
                condition=models.Q(("title", ""), _negated=True),
                name="blog_post_title_populated",
            ),
        ),
        migrations.AddConstraint(
            model_name="blogpost",
            constraint=models.CheckConstraint(
                condition=models.Q(("content", ""), _negated=True),
                name="blog_post_content_populated",
            ),
        ),
        migrations.AddConstraint(
            model_name="blogpostcomment",
            constraint=models.CheckConstraint(
                condition=models.Q(("content", ""), _negated=True),
                name="blog_post_comment_content_populated",
            ),
        ),
    ]

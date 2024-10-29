# Generated by Django 5.0.4 on 2024-05-21 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_blogpost_edited_date"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blogpost",
            options={
                "permissions": [
                    ("can_publish", "Can publish new blog posts."),
                    ("can_edit", "Can modify existing blog posts."),
                    ("can_remove", "Can remove existing blog posts."),
                    ("can_comment", "Can comment on blog posts."),
                ]
            },
        ),
    ]

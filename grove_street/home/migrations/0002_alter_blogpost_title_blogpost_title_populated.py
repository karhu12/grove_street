# Generated by Django 5.0.4 on 2024-04-23 11:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="title",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddConstraint(
            model_name="blogpost",
            constraint=models.CheckConstraint(
                check=models.Q(("title", ""), _negated=True), name="title_populated"
            ),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-26 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExperienceItem",
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
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                ("role", models.CharField(max_length=100, verbose_name="Role")),
                ("description", models.TextField(verbose_name="Description")),
                ("start_date", models.DateTimeField(verbose_name="Start date")),
                (
                    "end_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="End date"
                    ),
                ),
                ("category", models.CharField(max_length=100, verbose_name="Category")),
            ],
        ),
    ]
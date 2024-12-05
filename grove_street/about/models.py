from django.db import models


class ExperienceItem(models.Model):
    """Model that represents gained experience from specific category (work, education, etc.)."""

    title = models.CharField("Title", max_length=100)
    role = models.CharField("Role", max_length=100)
    description = models.TextField("Description")
    start_date = models.DateTimeField("Start date")
    end_date = models.DateTimeField("End date", blank=True, null=True)
    category = models.CharField("Category", max_length=100)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(~models.Q(title="")), name="experience_item_title_populated"
            ),
            models.CheckConstraint(
                condition=(~models.Q(role="")), name="experience_item_role_populated"
            ),
            models.CheckConstraint(
                condition=(~models.Q(description="")),
                name="experience_item_description_populated",
            ),
            models.CheckConstraint(
                condition=(~models.Q(category="")),
                name="experience_item_category_populated",
            ),
        ]


class ExpertiseItem(models.Model):
    """Model that represents expertise in specific category (programming language, framework, etc.)."""

    title = models.CharField("Title", max_length=100)
    category = models.CharField("Category", max_length=100)
    experience_months = models.IntegerField("Experience months")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(~models.Q(title="")), name="expertise_item_title_populated"
            ),
            models.CheckConstraint(
                condition=(~models.Q(category="")), name="expertise_item_category_populated"
            ),
            models.CheckConstraint(
                condition=(models.Q(experience_months__gt=0)), name="expertise_item_has_non_zero_experience"
            )
        ]

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


def is_present_experience(item: ExperienceItem) -> bool:
    """Check if the experience is present in the given experience item.

    Args:
        item: Experience item to check.
    Returns:
        Is present experience.
    """
    return item.end_date is None

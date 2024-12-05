from datetime import datetime, timezone

from django import template


register = template.Library()


@register.filter(name="user_friendly_months")
def user_friendly_months(months: int) -> str:
    """Return a user friendly string from given number of months.

    Examples:
    1 - "1 Month"
    2 - "2 Months"
    12 - "1 Year"
    18 - "1 Year"
    24 - "2 Years"

    Args:
        months: Number of months converted to duration string.
    Returns:
        String representation of the months in clear format.
    """

    if months < 12:
        return f"{months} Month{"s" if months > 1 else ""}"
    years = int(months // 12)
    return f"{years} Year{"s" if years > 1 else ""}"


@register.filter(name="get_category_class")
def get_category_class(category: str) -> str:
    """Returns class name for the given category."""

    category_classes = {
        "work": "work-item",
        "education": "education-item",
        "project": "project-item",
    }

    category_lower = category.lower()
    if category_lower in category_classes:
        return category_classes[category_lower]
    return "other-item"

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
        return f"{months} month{"s" if months > 1 else ""}"
    years = int(months // 12)
    return f"{years} year{"s" if years > 1 else ""}"

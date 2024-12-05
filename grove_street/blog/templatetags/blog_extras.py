from datetime import datetime

from django import template
from django.utils.timezone import now


register = template.Library()


def time_units_to_str(units: float | int, unit: str) -> str:
    """Convert given units based on given unit.

    If there is more than 1 units append 's' to end of resulting unit.
    """
    truncated = int(units)
    return f"{truncated} {unit}{"s" if truncated > 1 else ""} ago"


YEAR_IN_DAYS = 365.242
MONTHS_IN_YEAR = 12
DAYS_IN_WEEK = 7
MINUTE_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600
DAY_IN_SECONDS = HOUR_IN_SECONDS * 24
WEEK_IN_SECONDS = DAY_IN_SECONDS * 7
MONTH_IN_SECONDS = WEEK_IN_SECONDS * (YEAR_IN_DAYS / MONTHS_IN_YEAR / DAYS_IN_WEEK)
YEAR_IN_SECONDS = DAY_IN_SECONDS * YEAR_IN_DAYS


@register.filter(name="time_since_date")
def time_since_date(date: datetime) -> str:
    """Return how long time has it been since date as a string.

    Examples:
    "Just now"
    "1 second ago"
    "5 seconds ago"
    "1 minute ago"
    "24 minutes ago"
    "1 hour ago"
    "3 hours ago"
    "1 week ago"
    "3 weeks ago"
    "1 month ago"
    "3 months ago"
    "1 year ago"
    "3 years ago"

    This function is not accurate, as it does not take in account leap years, but uses year  fractions.

    Args:
        date: Date to be filtered.
    Returns:
        String representation of time since date.
    """
    delta = now() - date

    seconds = delta.total_seconds()
    minutes = seconds / MINUTE_IN_SECONDS
    hours = seconds / HOUR_IN_SECONDS
    days = seconds / DAY_IN_SECONDS
    weeks = seconds / WEEK_IN_SECONDS
    months = seconds / MONTH_IN_SECONDS
    years = seconds / YEAR_IN_SECONDS

    if int(years) > 0:
        return time_units_to_str(years, "year")
    elif int(months) > 0:
        return time_units_to_str(months, "month")
    elif int(weeks) > 0:
        return time_units_to_str(weeks, "week")
    elif int(days) > 0:
        return time_units_to_str(days, "day")
    elif int(hours) > 0:
        return time_units_to_str(hours, "hour")
    elif int(minutes) > 0:
        return time_units_to_str(minutes, "minute")
    elif int(seconds) > 0:
        return time_units_to_str(seconds, "second")
    return "Just now"

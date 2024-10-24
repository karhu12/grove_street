from datetime import datetime, timezone

from django import template


register = template.Library()

YEAR_IN_SECONDS = 31556926


@register.filter(name="time_since_date")
def time_since_date(date: datetime) -> str:
    """Return how long time has it been since date as a string.

    Examples:
    "1 second ago"
    "5 seconds ago"
    "1 minute ago"
    "24 minutes ago"
    "1 hour ago"
    "3 hours ago"
    "1 week ago"
    "4 weeks ago"
    "1 year ago"
    "3 years ago"

    Args:
        date: Date to be filtered.
    Returns:
        String representation of time since date.
    """
    delta = datetime.now(timezone.utc) - date

    if delta.days > 0:
        if delta.days > 7:
            weeks = int(delta.days / 7)
            return f"{weeks} {"weeks" if weeks > 1 else "week"} ago"
        return f"{delta.days} {"days" if delta.days > 1 else "day"} ago"
    elif (years := int(delta.seconds // YEAR_IN_SECONDS)) >= 1:
        return f"{years} {"years" if years > 1 else "year"} ago"
    elif (hours := int(delta.seconds / 60 // 60)) >= 1:
        return f"{hours} {"hours" if hours > 1 else "hour"} ago"
    elif (minutes := int(delta.seconds // 60)) >= 1:
        minutes = int(delta.seconds // 60)
        return f"{int(minutes)} {"minutes" if minutes > 1 else "minute"} ago"
    return f"{delta.seconds} {"seconds" if delta.seconds > 1 else "second"} ago"
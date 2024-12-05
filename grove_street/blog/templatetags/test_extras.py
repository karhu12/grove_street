import pytest
from datetime import timedelta

from django.utils.timezone import now

from .blog_extras import time_since_date


@pytest.mark.parametrize(
    "time_delta,expected_output",
    [
        (timedelta(), "Just now"),
        (timedelta(seconds=1), "1 second ago"),
        (timedelta(seconds=2), "2 seconds ago"),
        (timedelta(minutes=1), "1 minute ago"),
        (timedelta(minutes=2), "2 minutes ago"),
        (timedelta(hours=1), "1 hour ago"),
        (timedelta(hours=2), "2 hours ago"),
        (timedelta(weeks=1), "1 week ago"),
        (timedelta(weeks=2), "2 weeks ago"),
        (timedelta(weeks=4.349), "1 month ago"),
        (timedelta(weeks=4.349*2), "2 months ago"),
        (timedelta(weeks=52.18), "1 year ago"),
        (timedelta(weeks=104.36), "2 years ago"),
    ],
)
def test_that_extras_work(time_delta: timedelta, expected_output: str):
    """Test that extras work as intended."""
    date = now() - time_delta
    assert time_since_date(date) == expected_output

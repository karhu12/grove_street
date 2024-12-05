import pytest

from .about_extras import user_friendly_months


@pytest.mark.parametrize(
    "months,expected_output",
    [
        (1, "1 Month"),
        (2, "2 Months"),
        (12, "1 Year"),
        (13, "1 Year"),
        (24, "2 Years"),
        (25, "2 Years"),
    ],
)
def test_that_extras_work(months: int, expected_output: str):
    """Test that extras work as intended."""
    assert user_friendly_months(months) == expected_output

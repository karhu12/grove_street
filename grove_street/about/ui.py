import enum
from dataclasses import dataclass

from django.utils.timezone import now
from about.models import ExperienceItem


@dataclass
class ItemPosition:
    """Describes an absolute item positioned on experience timeline."""

    top: int
    height: int


MONTHS = 12


class Month(enum.Enum):
    """Enum describing the month with numeral value."""

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


# pixels
YEAR_MARKER = 50
MONTH_MARKER = 25
GAP = 40
TIMELINE_YEAR_HEIGHT = YEAR_MARKER + GAP + 11 * (GAP + MONTH_MARKER)
MONTH_EXPERIENCE = 50


def calculate_item_placement_on_timeline(
    item: ExperienceItem, latest_year: int
) -> ItemPosition:
    """Calculates ExperienceItem's position on experience timeline based on start and end date.

    Timeline is formed programmatically in following way:
    - year markers are 60 px tall, year markers also display december month
    - month markers are 25 px tall
    - there is a 40 px gap between markers

    Top position is placed at end date marker and element height should match the start date.

    Args:
        item: Experience item used to calculate it's position on UI.
        latest_year: Which year is the latest year shown on the timeline (required for calculation).
    Returns:
        ItemPosition describing the UI position.
    """

    def calculate_top(year: int, month: int) -> int:
        """Calculates where the top of experience item should be on the timeline."""

        # If month is december of the latest year, position is 0
        top = 0

        year_diff = latest_year - year
        if year_diff != 0:
            top += year_diff * TIMELINE_YEAR_HEIGHT

        if month != Month.DECEMBER.value:
            month_diff = MONTHS - month
            top += YEAR_MARKER + GAP + (month_diff - 1) * (MONTH_MARKER + GAP)

        return top

    def calculate_height(
        start_year: int, start_month: int, end_year: int, end_month: int
    ) -> int:
        """Calculates the height of the container based on difference of years and months."""
        height = 0

        year_diff = end_year - start_year
        if year_diff != 0:
            if end_month != Month.DECEMBER.value:
                height += end_month * (MONTH_MARKER + GAP)
                year_diff -= 1
            height += year_diff * TIMELINE_YEAR_HEIGHT

            if start_month == Month.DECEMBER.value:
                height += YEAR_MARKER
            else:
                month_diff = Month.DECEMBER.value - start_month
                height += (
                    YEAR_MARKER
                    + GAP
                    + (month_diff - 1) * (MONTH_MARKER + GAP)
                    + MONTH_MARKER
                )
        else:
            if start_year == end_year and start_month == end_month:
                height = MONTH_EXPERIENCE
            elif end_month != Month.DECEMBER.value:
                month_diff = end_month - start_month
                height += month_diff * (MONTH_MARKER + GAP) + MONTH_MARKER
            else:
                month_diff = end_month - start_month
                height += (
                    YEAR_MARKER + month_diff * (MONTH_MARKER + GAP)
                )

        return height

    # End date can be None to indicate it's an present experience
    if item.end_date is None:
        end_date = now()
    else:
        end_date = item.end_date

    top = calculate_top(end_date.year, end_date.month)
    height = calculate_height(
        item.start_date.year,
        item.start_date.month,
        end_date.year,
        end_date.month,
    )

    return ItemPosition(top, height)

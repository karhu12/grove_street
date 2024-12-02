from datetime import datetime, timezone

from django.test import TestCase

from test_utils import create_experience_item


class AboutPageTestCase(TestCase):
    """/about/ page test cases."""

    def test_page_loads(self):
        """Test that page can be reached."""
        request = self.client.get("/about/")
        self.assertEqual(request.status_code, 200)

    def test_that_experience_items_work(self):
        """Test that experience items are loaded correctly on the site.

        Experience items are created based on start and end date.
        They should be at specific top pixel position on their relative container with specific height.
        """
        test_content = [
            # December is year marker and month marker, should be 50px tall and at the top (as latest year).
            (
                datetime(2024, 12, 1, tzinfo=timezone.utc),
                datetime(2024, 12, 1, tzinfo=timezone.utc),
                0,
                50,
            ),
            # If the year and month match, item should be 50 px tall, starting from top of the month marker.
            (
                datetime(2024, 11, 1, tzinfo=timezone.utc),
                datetime(2024, 11, 1, tzinfo=timezone.utc),
                90,
                50,
            ),
            # In between months spanning from 1 to more months should be  month_diff * (marker + gap height) + month marker pixels tall.
            (
                datetime(2024, 9, 1, tzinfo=timezone.utc),
                datetime(2024, 10, 1, tzinfo=timezone.utc),
                155,
                90,
            ),
            (
                datetime(2024, 2, 1, tzinfo=timezone.utc),
                datetime(2024, 8, 1, tzinfo=timezone.utc),
                285,
                415,
            ),
            # Dates spanning from one year to another should take in account year marker height (50px from month marker 25 px)
            (
                datetime(2023, 11, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                740,
                180,
            ),
            # Oldest date with a start date of december of that year, should not create a new timeline under it.
            (
                datetime(2022, 12, 1, tzinfo=timezone.utc),
                datetime(2022, 12, 31, tzinfo=timezone.utc),
                1610,
                50,
            ),

        ]

        for item in test_content:
            create_experience_item(start_date=item[0], end_date=item[1])

        request = self.client.get("/about/")
        for item in test_content:
            self.assertContains(request, f"<h1 class=\"experience-year-highlight-text\">{item[0].year}</h1>", 1)
            self.assertContains(request, f"<h1 class=\"experience-year-highlight-text\">{item[1].year}</h1>", 1)
            self.assertContains(request, f"<div style=\"top: {item[2]}px; height: {item[3]}px\" class=\"work-experience-item card-shadow\">", 1)

        oldest_year = test_content[-1][0].year
        self.assertNotContains(request, f"<h1 class=\"experience-year-highlight-text\">{oldest_year - 1}</h1>")
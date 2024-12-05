from datetime import datetime, timezone

from django.test import TestCase

from test_utils import create_experience_item, create_expertise_item
from about.templatetags.about_extras import user_friendly_months, get_category_class


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
        request = self.client.get("/about/")

        self.assertContains(request, "<p>No experience items available.</p>", 1)

        test_content = [
            # December is year marker and month marker, should be 50px tall and at the top (as latest year).
            (
                datetime(2024, 12, 1, tzinfo=timezone.utc),
                datetime(2024, 12, 1, tzinfo=timezone.utc),
                0,
                50,
                "Work",
            ),
            # If the year and month match, item should be 50 px tall, starting from top of the month marker.
            (
                datetime(2024, 11, 1, tzinfo=timezone.utc),
                datetime(2024, 11, 1, tzinfo=timezone.utc),
                90,
                50,
                "Work",
            ),
            # In between months spanning from 1 to more months should be  month_diff * (marker + gap height) + month marker pixels tall.
            (
                datetime(2024, 9, 1, tzinfo=timezone.utc),
                datetime(2024, 10, 1, tzinfo=timezone.utc),
                155,
                90,
                "Work",
            ),
            (
                datetime(2024, 2, 1, tzinfo=timezone.utc),
                datetime(2024, 8, 1, tzinfo=timezone.utc),
                285,
                415,
                "Work",
            ),
            # Dates spanning from one year to another should take in account year marker height (50px from month marker 25 px)
            (
                datetime(2023, 11, 1, tzinfo=timezone.utc),
                datetime(2024, 1, 1, tzinfo=timezone.utc),
                740,
                180,
                "Work",
            ),
            # Education item should appear on the right side of the timeline with different color (and add new category to legend)
            (
                datetime(2024, 11, 1, tzinfo=timezone.utc),
                datetime(2024, 12, 1, tzinfo=timezone.utc),
                0,
                115,
                "Education",
            ),
            # Oldest date with a start date of december of that year, should not create a new timeline under it.
            (
                datetime(2022, 12, 1, tzinfo=timezone.utc),
                datetime(2022, 12, 31, tzinfo=timezone.utc),
                1610,
                50,
                "Work",
            ),
        ]

        for item in test_content:
            create_experience_item(start_date=item[0], end_date=item[1], category=item[4])

        request = self.client.get("/about/")
        for item in test_content:
            self.assertContains(
                request,
                f'<h1 class="experience-year-highlight-text">{item[0].year}</h1>',
                1,
            )
            self.assertContains(
                request,
                f'<h1 class="experience-year-highlight-text">{item[1].year}</h1>',
                1,
            )
            if item[4] == "Work":
                self.assertContains(
                    request,
                    f'<div style="top: {item[2]}px; height: {item[3]}px" class="{get_category_class(item[4])} left-experience-item card-shadow">',
                    1,
                )
            else:
                self.assertContains(
                    request,
                    f'<div style="top: {item[2]}px; height: {item[3]}px" class="{get_category_class(item[4])} right-experience-item card-shadow">',
                    1,
                )

        oldest_year = test_content[-1][0].year
        self.assertNotContains(
            request,
            f'<h1 class="experience-year-highlight-text">{oldest_year - 1}</h1>',
        )

        self.assertContains(request, f"<div class=\"work-item experience-category-color-marker\"></div>", 1)
        self.assertContains(request, f"<label class=\"no-margin\">Work</label>", 1)
        self.assertContains(request, f"<div class=\"education-item experience-category-color-marker\"></div>", 1)
        self.assertContains(request, f"<label class=\"no-margin\">Education</label>", 1)

    def test_that_expertise_items_work(self):
        """Test that expertise items are loaded as expected."""
        request = self.client.get("/about/")

        self.assertContains(request, "<p>No expertise items available.</p>", 1)

        item = create_expertise_item(
            title="Title 1", category="One", experience_months=1
        )
        item_2 = create_expertise_item(
            title="Title 2", category="Two", experience_months=2
        )

        request = self.client.get("/about/")

        self.assertContains(request, '<div class="expertise-item-content-row">', 2)
        self.assertContains(request, f"<p>{item.category}</p>", 1)
        self.assertContains(request, f"<p>{item_2.category}</p>", 1)
        self.assertContains(
            request, f'<p class="expertise-item-content-row-title">{item.title}</p>', 1
        )
        self.assertContains(
            request,
            f'<p class="expertise-item-content-row-title">{item_2.title}</p>',
            1,
        )
        item_months = user_friendly_months(item.experience_months)
        item_2_months = user_friendly_months(item_2.experience_months)
        self.assertContains(
            request,
            f'<p class="expertise-item-content-row-experience">{item_months}</p>',
            1,
        )
        self.assertContains(
            request,
            f'<p class="expertise-item-content-row-experience">{item_2_months}</p>',
            1,
        )

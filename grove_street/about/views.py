from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpRequest
from django.utils.timezone import now

from about.models import ExperienceItem, ExpertiseItem
from about.ui import calculate_item_placement_on_timeline, Month


def about(request: HttpRequest):
    """Endpoint for viewing the about page of the website."""
    experience_items_query = ExperienceItem.objects.order_by("-end_date")

    work_items = []
    non_work_items = []
    experience_item_categories = []

    if experience_items_query:
        first = experience_items_query.first()
        if first.end_date is None:
            latest_year = now().year
        else:
            latest_year = first.end_date.year

        oldest_date = experience_items_query.latest("-start_date").start_date
        for item in experience_items_query:
            experience_item = {
                "placement": calculate_item_placement_on_timeline(item, latest_year),
                "item": item,
            }
            if item.category.lower() == "work":
                work_items.append(experience_item)
            else:
                non_work_items.append(experience_item)

            if item.category not in experience_item_categories:
                experience_item_categories.append(item.category)

        if latest_year == oldest_date.year:
            experience_range = range(latest_year + 1, latest_year, -1)
        elif oldest_date.month == Month.DECEMBER.value:
            experience_range = range(latest_year + 1, oldest_date.year + 1, -1)
        else:
            experience_range = range(latest_year + 1, oldest_date.year, -1)
        end_year = experience_range[-1] - 1
    else:
        experience_range = None
        end_year = None

    expertise_items_query = ExpertiseItem.objects.order_by("-experience_months")

    categorized_expertise_items = {}
    if expertise_items_query:
        for item in expertise_items_query:
            if item.category not in categorized_expertise_items:
                categorized_expertise_items[item.category] = []
            categorized_expertise_items[item.category].append(item)

    context = {
        "experience_range": experience_range,
        "experience_item_categories": experience_item_categories,
        "work_experience_items": work_items,
        "non_work_experience_items": non_work_items,
        "categorized_expertise_items": categorized_expertise_items,
        "end_year": end_year
    }

    return render(request, "about/about.html", context)

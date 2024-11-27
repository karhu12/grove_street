from django.shortcuts import render
from django.http import HttpRequest

from blog.models import get_latest_blog_posts
from home.constants import (
    MAX_BLOG_POSTS_ON_HOME_PAGE,
)


def home(request: HttpRequest):
    """Endpoint for viewing the home page of the website."""
    latest_posts = get_latest_blog_posts(end_index=MAX_BLOG_POSTS_ON_HOME_PAGE)
    return render(request, "home/home.html", {"latest_posts": latest_posts})

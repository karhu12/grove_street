from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, Http404
from django.views import View

from home.models import get_latest_blog_posts, BlogPost
from home.constants import MAX_BLOG_POSTS_ON_HOME_PAGE, MAX_BLOG_POSTS_ON_BLOG_PAGE

# GET


def home(request: HttpRequest):
    """Endpoint for viewing the home page of the website."""
    latest_posts = get_latest_blog_posts(end_index=MAX_BLOG_POSTS_ON_HOME_PAGE)
    return render(request, "home/home.html", {"latest_posts": latest_posts})


def about(request: HttpRequest):
    """Endpoint for viewing information about me."""
    return render(request, "home/about.html")


def blog(request: HttpRequest, page: int = 1):
    """Endpoint for viewing all blog posts."""
    if page < 1:
        raise Http404("Page number can not be lower than 1.")

    end_index = MAX_BLOG_POSTS_ON_BLOG_PAGE * page
    start_index = end_index - MAX_BLOG_POSTS_ON_BLOG_PAGE
    latest_posts = get_latest_blog_posts(start_index, end_index)
    return render(
        request,
        "home/blog.html",
        {
            "latest_posts": latest_posts,
            "previous_page": page - 1,
            "page": page,
            "next_page": page + 1
        },
    )

def blog_post(request: HttpRequest, id: int):
    """Endpoint for checking an individual blog post."""
    blog_post = get_object_or_404(BlogPost, pk=id)
    return render(request, "home/blog_post.html", {"blog_post": blog_post})

# POST


def publish_blog_post(request: HttpRequest):
    pass

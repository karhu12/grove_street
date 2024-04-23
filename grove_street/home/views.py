from django.shortcuts import render
from django.http import HttpRequest, Http404

from home.models import BlogPost, get_latest_blog_posts
from home.constants import MAX_BLOG_POSTS_ON_HOME_PAGE, MAX_BLOG_POSTS_ON_BLOG_PAGE

# GET


def home(request: HttpRequest):
    latest_posts = get_latest_blog_posts(end_index=MAX_BLOG_POSTS_ON_HOME_PAGE)
    return render(request, "home/home.html", {"latest_posts": latest_posts})


def about(request: HttpRequest):
    return render(request, "home/about.html")


def blog(request: HttpRequest, page=1):
    if page < 1:
        raise Http404

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


# POST


def publish_blog_post(request: HttpRequest):
    pass

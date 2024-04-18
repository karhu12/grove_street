from django.shortcuts import render
from django.http import HttpRequest

from home.models import BlogPost

# GET

def home(request: HttpRequest):
    try:
        latest_posts = BlogPost.objects.order_by("published_date")[:3]
    except BlogPost.DoesNotExist:
        latest_posts = None
    return render(request, "home/home.html", {"latest_posts": latest_posts})

def about_me(request: HttpRequest):
    return render(request, "home/about.html")

def my_background(request: HttpRequest):
    return render(request, "home/background.html")

def miscellaneous(request: HttpRequest):
    return render(request, "home/miscellaneous.html")
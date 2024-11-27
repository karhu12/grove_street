from django.shortcuts import render
from django.http import HttpRequest


def about(request: HttpRequest):
    """Endpoint for viewing the about page of the website."""
    return render(request, "about/about.html")

from django.shortcuts import render
from django.http import HttpRequest

def home(request: HttpRequest):
    return render(request, "home/home.html")

def about_me(request: HttpRequest):
    return render(request, "home/about.html")

def my_background(request: HttpRequest):
    return render(request, "home/background.html")

def miscellaneous(request: HttpRequest):
    return render(request, "home/miscellaneous.html")
from django.shortcuts import render
from django.http import HttpRequest

def home(request: HttpRequest):
    return render(request, "home/index.html")

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home(request: HttpRequest):
    return HttpResponse("Grove street, Home.")

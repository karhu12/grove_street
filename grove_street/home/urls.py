from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about_me, name="about"),
    path("background", views.my_background, name="background"),
    path("miscellaneous", views.miscellaneous, name="miscellaneous"),
]

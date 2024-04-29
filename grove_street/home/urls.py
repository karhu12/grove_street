from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("blog/posts/", views.blog, name="blog"),
    path("blog/posts/page-<int:page>/", views.blog, name="blog"),
    path("blog/post/<int:id>/", views.blog_post, name="blog_post"),
]

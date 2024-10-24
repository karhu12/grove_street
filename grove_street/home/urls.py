from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/posts/", views.BlogPosts.as_view(), name="blog"),
    path(
        "blog/posts/publish/",
        views.PublishBlogPost.as_view(),
        name="blog_post_publish",
    ),
    path("blog/post/<int:id>/", views.blog_post, name="blog_post"),
    path(
        "blog/post/<int:id>/edit/",
        views.EditBlogPost.as_view(),
        name="blog_post_edit",
    ),
    path(
        "blog/post/<int:id>/delete/",
        views.DeleteBlogPost.as_view(),
        name="blog_post_delete",
    ),
]

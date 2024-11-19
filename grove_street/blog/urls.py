from django.urls import path

from . import views

urlpatterns = [
    path("posts/", views.BlogPosts.as_view(), name="blog"),
    path(
        "posts/publish/",
        views.PublishBlogPost.as_view(),
        name="blog_post_publish",
    ),
    path("post/<int:id>/", views.IndividualBlogPost.as_view(), name="blog_post"),
    path(
        "post/<int:id>/edit/",
        views.EditBlogPost.as_view(),
        name="blog_post_edit",
    ),
    path(
        "post/<int:id>/delete/",
        views.DeleteBlogPost.as_view(),
        name="blog_post_delete",
    ),
]

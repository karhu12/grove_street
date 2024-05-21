from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/posts/", views.blog, name="blog"),
    path("blog/posts/page-<int:page>/", views.blog, name="blog"),
    path("blog/posts/publish/", views.PublishBlogPostView.as_view(), name="blog_post_publish"),
    path("blog/post/<int:id>/", views.blog_post, name="blog_post"),
    path(
        "blog/post/<int:id>/edit/",
        views.BlogPostEditView.as_view(),
        name="blog_post_edit",
    ),
    path(
        "blog/post/<int:id>/delete/",
        views.BlogPostDeleteView.as_view(),
        name="blog_post_delete",
    ),
]

from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth.models import User

from home.models import BlogPost


def create_test_user(username: str = "TEST_USER", password: str = "TEST_PW") -> User:
    """Creates test user with given username and password.

    Args:
        username: Username for the new user.
        password: Password for the new user.
    Returns:
        Created user.
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(username="test_user", password="1234")
    user.save()
    return user


def create_blog_post(
    user: User,
    published_date: datetime = now(),
    title: str = "Title",
    content: str = "Content",
) -> BlogPost:
    """Creates and saves new blog post with given arguments to the database.

    Args:
        user: Author of the blog post.
        published_date: Datetime when the blog post was published.
        title: Title of the blog post.
        content: Content of the blog post.
    Returns:
        Created blog post.
    """
    blog_post = BlogPost.objects.create(author=user, published_date=published_date, title=title, content=content)
    blog_post.save()
    return blog_post


class HomeViewTestCase(TestCase):
    """Test that home root view works as intended."""

    def test_no_blog_posts_shown(self):
        """Test that no blog posts are shown when database contains none."""
        response = self.client.get("")
        self.assertContains(response, "<p>No blog posts available!</p>", count=1)

    def test_1_blog_post_shown(self):
        """Test that only one blog post is shown when database contains it."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        response = self.client.get("")
        self.assertEqual(len(response.context["latest_posts"]), 1)
        self.assertEqual(response.context["latest_posts"][0], blog_post)
        self.assertContains(response, "<div class=\"blog-post-container\">", count=1)

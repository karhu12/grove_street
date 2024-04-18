from datetime import datetime
from typing import Optional

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
    user: Optional[User] = None,
    published_date: datetime = now(),
    title: str = "Title",
    content: str = "Content",
) -> BlogPost:
    """Creates and saves new blog post with given arguments to the database.

    Args:
        user: Author of the blog post (Can be none).
        published_date: Datetime when the blog post was published.
        title: Title of the blog post.
        content: Content of the blog post.
    Returns:
        Created blog post.
    """
    options = {}
    for option, option_name in [
        (user, "author"),
        (published_date, "published_date"),
        (title, "title"),
        (content, "content")
    ]:
        if option:
            options[option_name] = option

    blog_post = BlogPost.objects.create(**options)
    blog_post.save()
    return blog_post
from datetime import datetime, timedelta
from typing import Optional

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth.models import User, Permission

from home.models import BlogPost


def create_test_user(
    username: str = "TEST_USER", password: str = "TEST_PW", permissions: list[str] = []
) -> User:
    """Creates test user with given username and password.

    Args:
        username: Username for the new user.
        password: Password for the new user.
        permissions: Permission codenames to be given to the user as a list.
    Returns:
        Created user.
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(username=username, password=password)
    for code_name in permissions:
        permission = Permission.objects.get(codename=code_name)
        user.user_permissions.add(permission)
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
    Raises:
        IntegrityError: Saving blog post failed.
    """
    options = {}
    for option, option_name in [
        (user, "author"),
        (published_date, "published_date"),
        (title, "title"),
        (content, "content"),
    ]:
        if option:
            options[option_name] = option

    blog_post = BlogPost(**options)
    blog_post.save()
    return blog_post


def create_blog_posts_with_differing_published_date(count: int) -> list[BlogPost]:
    """Creates blog posts with each of the blog post having different published date.

    Args:
        count: How many blog posts to create.
    Returns:
        list of created blog posts.
    """
    blog_posts = []
    user = create_test_user()
    current_datetime = now()
    for i in range(count):
        # Make sure all blog posts have different published date (by 1 microsecond)
        blog_post = create_blog_post(
            user,
            published_date=(
                current_datetime
                + timedelta(microseconds=current_datetime.microsecond + i)
            ),
        )
        blog_posts.append(blog_post)

    blog_posts.sort(key=lambda item: item.published_date, reverse=True)
    return blog_posts

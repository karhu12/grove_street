from datetime import datetime, timedelta
from typing import Optional

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth.models import User, Permission

from home.models import BlogPost, BlogPostComment


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
        user: Author of the blog post.
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


def create_blog_posts_with_differing_published_date(
    count: int, user: Optional[User] = None
) -> list[BlogPost]:
    """Creates blog posts with each of the blog post having different published date.

    Args:
        count: How many blog posts to create.
        user: User which the blog post and comments belong to (create new one if not passed).
    Returns:
        list of created blog posts sorted from newest to oldest.
    """
    blog_posts = []

    if user is None:
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


def create_blog_post_comment(
    blog_post: Optional[BlogPost] = None,
    user: Optional[User] = None,
    created_date: datetime = now(),
    edited_date: Optional[datetime] = None,
    content: str = "Content",
) -> BlogPostComment:
    """Creates a blog post comment for the given blog post using the given information.

    Args:
        blog_post: Blog post for which this comment is created for.
        user: Author of the this comment.
        created_date: Datetime when the comment was created.
        edited_date: Datetime when the comment was edited.
        content: Content of the blog post.
    Returns:
        Created blog post.
    Raises:
        IntegrityError: Saving blog post failed.
    """
    options = {}
    for option, option_name in [
        (blog_post, "blog_post"),
        (user, "author"),
        (created_date, "created_date"),
        (edited_date, "edited_date"),
        (content, "content"),
    ]:
        if option:
            options[option_name] = option

    comment = BlogPostComment(**options)
    comment.save()
    return comment


def create_blog_post_comments_with_differing_published_date(
    count: int, blog_post: BlogPost, user: Optional[User] = None
) -> list[BlogPostComment]:
    """Creates blog post comments with each of the comment having different published date.

    Args:
        count: How many blog post comments to create.
        blog_post: Blog post which the comments belong to.
        user: User which the new comments belong to (create new one if not passed).
    Returns:
        list of created comments sorted from newest to oldest.
    """
    comments = []
    if not user:
        user = create_test_user()

    current_datetime = now()
    for i in range(count):
        # Make sure all comments have different published date (by 1 microsecond)
        comment = create_blog_post_comment(
            blog_post,
            user,
            created_date=(
                current_datetime
                + timedelta(microseconds=current_datetime.microsecond + i)
            ),
        )
        comments.append(comment)

    comments.sort(key=lambda item: item.created_date, reverse=True)
    return comments

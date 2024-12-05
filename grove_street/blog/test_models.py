import pytest

from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils.timezone import now

from test_utils import create_blog_post, create_test_user, create_blog_post_comment


@pytest.mark.django_db
@pytest.mark.parametrize(
    "parameter,expected_error",
    [
        ("user", IntegrityError),
        ("title", IntegrityError),
        ("content", IntegrityError),
        ("published_date", IntegrityError),
        ("edited_date", None),
    ],
)
def test_creating_blog_post_without_parameter(
    parameter: str, expected_error: Exception | None
):
    """Attempt to create an blog post without a given parameter."""
    user = create_test_user()

    params = {
        "user": user
    }

    params[parameter] = None

    if expected_error is None:
        create_blog_post(**params)
    else:
        with pytest.raises(expected_error):
            create_blog_post(**params)


class BlogPostTestCase(TestCase):
    """Tests related to BlogPost model."""

    def test_creating(self):
        """Attempt to create a blog post with necessary information."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertEqual(blog_post.edited_date, None)

    def test_modifying_edited_date(self):
        """Attempt to create a blog post and modify edited date after creation."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertEqual(blog_post.edited_date, None)

        edited_date = now()
        blog_post.edited_date = edited_date
        blog_post.save()
        self.assertEqual(blog_post.edited_date, edited_date)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "parameter,expected_error",
    [
        ("user", IntegrityError),
        ("blog_post", IntegrityError),
        ("content", IntegrityError),
        ("created_date", IntegrityError),
        ("edited_date", None),
    ],
)
def test_creating_blog_post_comment_without_parameter(
    parameter: str, expected_error: Exception | None
):
    """Attempt to create an blog post comment without a given parameter."""
    user = create_test_user()
    blog_post = create_blog_post(user)

    params = {
        "user": user,
        "blog_post": blog_post,
    }

    params[parameter] = None

    if expected_error is None:
        create_blog_post_comment(**params)
    else:
        with pytest.raises(expected_error):
            create_blog_post_comment(**params)


class BlogPostCommentTestCase(TestCase):
    """Tests related to BlogPostComment model."""

    def test_creating(self):
        """Attempt to create a blog post comment with necessary information."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        comment = create_blog_post_comment(blog_post, user)
        self.assertEqual(comment.edited_date, None)

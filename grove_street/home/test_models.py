from django.test import TestCase
from django.db.utils import IntegrityError

from home.test_utils import create_blog_post, create_test_user


class BlogPostTestCase(TestCase):
    """Tests related to BlogPost model."""

    def test_creating(self):
        """Attempt to create a blog post with necessary information."""
        user = create_test_user()
        create_blog_post(user)

    def test_creating_without_user(self):
        """Attempt to create a blog post without a user."""
        self.assertRaises(IntegrityError, create_blog_post, user=None)

    def test_creating_without_title(self):
        """Attempt to create a blog post without a title."""
        user = create_test_user()
        self.assertRaises(IntegrityError, create_blog_post, user, title=None)

    def test_creating_without_content(self):
        """Attempt to create a blog post without content."""
        user = create_test_user()
        self.assertRaises(IntegrityError, create_blog_post, user, content=None)

    def test_creating_without_published_date(self):
        """Attempt to create a blog post without published date."""
        user = create_test_user()
        self.assertRaises(IntegrityError, create_blog_post, user, published_date=None)
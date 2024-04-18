from django.test import TestCase
from django.db.utils import IntegrityError

from home.models import BlogPost

from home.test_utils import create_blog_post, create_test_user


class BlogPostTestCase(TestCase):
    """Tests related to BlogPost model."""

    def test_creating_without_user(self):
        """Attempt to create a blog post without a user."""
        self.assertRaises(IntegrityError, create_blog_post, user=None)


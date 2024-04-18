from django.test import TestCase, Client


class HomeViewTestCase(TestCase):
    """Test that home root view works as intended."""

    def test_no_blog_posts_shown(self):
        """Test that no blog posts are shown when database contains none."""
        client = Client()
        response = client.get("")
        self.assertContains(response, "<p>No blog posts available!</p>", count=1)

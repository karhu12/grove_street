from django.test import TestCase

from test_utils import (
    create_blog_post,
    create_test_user,
    create_blog_posts_with_differing_published_date,
)
from home.constants import MAX_BLOG_POSTS_ON_HOME_PAGE


class HomeViewTestCase(TestCase):
    """Test that home root view works as intended."""

    def test_not_shown(self):
        """Test that no blog posts are shown when database contains none."""
        response = self.client.get("")
        self.assertContains(response, "No blog posts available!", count=1)

    def test_created_posts_shown(self):
        """Test that only one blog post is shown when database contains it."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        response = self.client.get("")
        self.assertEqual(len(response.context["latest_posts"]), 1)
        self.assertEqual(response.context["latest_posts"][0], blog_post)
        self.assertContains(
            response, '<div class="blog-post-preview-container">', count=1
        )

    def test_max_created_posts_shown_in_correct_order(self):
        """Test that maximum of three blog posts are shown in correct order
        when database contains more than three.
        """
        blog_posts = create_blog_posts_with_differing_published_date(
            MAX_BLOG_POSTS_ON_HOME_PAGE + 1
        )
        response = self.client.get("")

        self.assertEqual(
            len(response.context["latest_posts"]), MAX_BLOG_POSTS_ON_HOME_PAGE
        )

        for i in range(MAX_BLOG_POSTS_ON_HOME_PAGE):
            self.assertEqual(response.context["latest_posts"][i], blog_posts[i])

        self.assertContains(
            response,
            '<div class="blog-post-preview-container">',
            count=MAX_BLOG_POSTS_ON_HOME_PAGE,
        )

from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from home.test_utils import create_blog_post, create_test_user


class HomeViewTestCase(TestCase):
    """Test that home root view works as intended."""

    def test_not_shown(self):
        """Test that no blog posts are shown when database contains none."""
        response = self.client.get("")
        self.assertContains(response, "<p>No blog posts available!</p>", count=1)

    def test_1_post_shown(self):
        """Test that only one blog post is shown when database contains it."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        response = self.client.get("")
        self.assertEqual(len(response.context["latest_posts"]), 1)
        self.assertEqual(response.context["latest_posts"][0], blog_post)
        self.assertContains(response, "<div class=\"blog-post-preview-container\">", count=1)

    def test_2_posts_shown(self):
        """Test that two blog posts are shown when database contains them."""
        user = create_test_user()
        blog_posts = []
        for _ in range(2):
            blog_posts.append(create_blog_post(user))
        response = self.client.get("")
        self.assertEqual(len(response.context["latest_posts"]), 2)
        for i in range(2):
            self.assertEqual(response.context["latest_posts"][i], blog_posts[i])
        self.assertContains(response, "<div class=\"blog-post-preview-container\">", count=2)

    def test_3_posts_shown(self):
        """Test that three blog posts are shown when database contains them."""
        user = create_test_user()
        blog_posts = []
        for _ in range(3):
            blog_posts.append(create_blog_post(user))
        response = self.client.get("")
        self.assertEqual(len(response.context["latest_posts"]), 3)
        for i in range(3):
            self.assertEqual(response.context["latest_posts"][i], blog_posts[i])
        self.assertContains(response, "<div class=\"blog-post-preview-container\">", count=3)

    def test_max_3_posts_shown_in_correct_order(self):
        """Test that maximum of three blog posts are shown in correct order
        when database contains more than three.
        """
        user = create_test_user()
        blog_posts = []
        current_datetime = now()
        for i in range(4):
            # Make sure all blog posts have different published date (by 1 microsecond)
            blog_post = create_blog_post(
                user,
                published_date=(
                    current_datetime +
                    timedelta(microseconds=current_datetime.microsecond + i)
                )
            )
            blog_posts.append(blog_post)

        blog_posts.sort(key=lambda item: item.published_date, reverse=True)
        response = self.client.get("")
        self.assertEqual(len(response.context["latest_posts"]), 3)
        for i in range(3):
            self.assertEqual(response.context["latest_posts"][i], blog_posts[i])
        self.assertContains(response, "<div class=\"blog-post-preview-container\">", count=3)

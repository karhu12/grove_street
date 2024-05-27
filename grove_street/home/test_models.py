from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils.timezone import now

from home.test_utils import create_blog_post, create_test_user, create_blog_post_comment


class BlogPostTestCase(TestCase):
    """Tests related to BlogPost model."""

    def test_creating(self):
        """Attempt to create a blog post with necessary information."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertEqual(blog_post.edited_date, None)

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

    def test_modifying_edited_date(self):
        """Attempt to create a blog post and modify edited date after creation."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertEqual(blog_post.edited_date, None)

        edited_date = now()
        blog_post.edited_date = edited_date
        blog_post.save()
        self.assertEqual(blog_post.edited_date, edited_date)


class BlogPostCommentTestCase(TestCase):
    """Tests related to BlogPostComment model."""

    def test_creating(self):
        """Attempt to create a blog post comment with necessary information."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        comment = create_blog_post_comment(blog_post, user)
        self.assertEqual(comment.edited_date, None)

    def test_creating_without_user(self):
        """Attempt to create a blog post comment without a user."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertRaises(IntegrityError, create_blog_post_comment, blog_post, None)

    def test_creating_without_blog_post(self):
        """Attempt to create a blog post comment without a blog post."""
        user = create_test_user()
        self.assertRaises(IntegrityError, create_blog_post_comment, None, user)

    def test_creating_without_content(self):
        """Attempt to create a blog post comment without content."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertRaises(
            IntegrityError,
            create_blog_post_comment,
            blog_post,
            user,
            content=None,
        )

    def test_creating_without_created_date(self):
        """Attempt to create a blog post comment without created date."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        self.assertRaises(
            IntegrityError, create_blog_post_comment, blog_post, user, created_date=None
        )

    def test_modifying_edited_date(self):
        """Attempt to create a blog post comment and modify edited date after creation."""
        user = create_test_user()
        blog_post = create_blog_post(user)
        comment = create_blog_post_comment(blog_post, user)
        self.assertEqual(comment.edited_date, None)

        edited_date = now()
        comment.edited_date = edited_date
        comment.save()
        self.assertEqual(comment.edited_date, edited_date)
from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.auth import login

from home.test_utils import (
    create_blog_post,
    create_test_user,
    create_blog_posts_with_differing_published_date,
)
from home.constants import MAX_BLOG_POSTS_ON_BLOG_PAGE, MAX_BLOG_POSTS_ON_HOME_PAGE
from home.models import BlogPost


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


class BlogViewTestCase(TestCase):
    """Test that 'blog/posts/' view works as intended."""

    def test_404_on_invalid_pages(self):
        """Test that 404 is raised when invalid pages are tried to be accessed."""
        invalid_pages = [-1.5, -1, 0, 1.5]
        for invalid_page in invalid_pages:
            response = self.client.get(f"/blog/posts/page-{invalid_page}/")

            self.assertEqual(
                response.status_code,
                404,
                "Response should have status code 404 on invalid pages.",
            )

    def test_200_on_valid_pages(self):
        """Test that page is shown when url is valid for pages.

        Page numbers > 0 should be considered valid up to
        atleast postgresql signed integer max value.
        """
        valid_pages = [1, 2147483647]
        for valid_page in valid_pages:
            response = self.client.get(f"/blog/posts/page-{valid_page}/")

            self.assertEqual(response.status_code, 200, "Status code")

    def test_not_shown(self):
        """Test that no blog posts are shown when none are available."""
        response = self.client.get("/blog/posts/page-1/")

        self.assertContains(response, "No blog posts available!", 1)

    def test_created_posts_shown(self):
        """Test that the created posts are shown on the first page."""
        blog_posts = create_blog_posts_with_differing_published_date(5)

        response = self.client.get("/blog/posts/page-1/")

        self.assertEqual(len(response.context["latest_posts"]), 5)

        for i in range(5):
            self.assertEqual(response.context["latest_posts"][i], blog_posts[i])

        self.assertContains(
            response, '<div class="blog-post-preview-container">', count=5
        )

    def test_up_to_max_posts_shown(self):
        """Test that only up to maximum amount of posts per page are shown on the first page."""
        blog_posts = create_blog_posts_with_differing_published_date(
            MAX_BLOG_POSTS_ON_BLOG_PAGE + 1
        )

        response = self.client.get("/blog/posts/page-1/")

        self.assertEqual(
            len(response.context["latest_posts"]), MAX_BLOG_POSTS_ON_BLOG_PAGE
        )

        for i in range(MAX_BLOG_POSTS_ON_BLOG_PAGE):
            self.assertEqual(response.context["latest_posts"][i], blog_posts[i])

        self.assertContains(
            response,
            '<div class="blog-post-preview-container">',
            count=MAX_BLOG_POSTS_ON_BLOG_PAGE,
        )

    def correct_posts_shown_on_page_2(self):
        """Test that pages that are not shown on page 1 contain the correct created posts."""
        blog_posts = create_blog_posts_with_differing_published_date(
            MAX_BLOG_POSTS_ON_BLOG_PAGE + 1
        )

        response = self.client.get("/blog/posts/page-2/")

        self.assertEqual(len(response.context["latest_posts"]), 1)

        self.assertEqual(response.context["latest_posts"][-1], blog_posts[-1])

        self.assertContains(
            response,
            '<div class="blog-post-preview-container">',
            count=1,
        )


class BlogEditViewTestCase(TestCase):
    """Test that '/blog/post/<id>/edit/' view works as intended."""

    def test_that_view_is_not_shown_without_permissions(self):
        """Test that user logged in without permissions can not view the page."""
        user = create_test_user()
        self.client.force_login(user)
        blog_post = create_blog_post(user)

        response = self.client.get(f"/blog/post/{blog_post.pk}/edit/", follow=True)
        self.assertEqual(response.status_code, 403)

    def test_that_view_is_shown_with_permissions(self):
        """Test that user logged in with permissions can view the page."""
        user = create_test_user(permissions=["can_edit"])
        self.client.force_login(user)
        blog_post = create_blog_post(user)

        response = self.client.get(f"/blog/post/{blog_post.pk}/edit/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_that_view_redirects_to_login(self):
        """Test that edit view redirects to login page if user has not logged in."""
        user = create_test_user()
        blog_post = create_blog_post(user)

        response = self.client.get(f"/blog/post/{blog_post.pk}/edit/", follow=True)
        self.assertRedirects(
            response, f"/accounts/login/?next=/blog/post/{blog_post.pk}/edit/"
        )

    def test_that_view_works(self):
        """Test that submitted form from edit view modifies the created blog post."""
        user = create_test_user(permissions=["can_edit"])
        self.client.force_login(user)
        blog_post = create_blog_post(user)

        new_title = "Edited title"
        new_content = "Edited content"

        response = self.client.post(
            f"/blog/post/{blog_post.pk}/edit/",
            {"title": new_title, "content": new_content},
            follow=True,
        )
        self.assertRedirects(response, f"/blog/post/{blog_post.pk}/")

        blog_post = BlogPost.objects.get(pk=blog_post.pk)
        self.assertEqual(blog_post.title, new_title)
        self.assertEqual(blog_post.content, new_content)
        self.assertNotEqual(blog_post.edited_date, None)


class BlogPublishViewTestCase(TestCase):
    """Test that '/blog/posts/publish/' view works as intended."""

    def test_that_view_is_not_shown_without_permissions(self):
        """Test that user logged in without permissions can not view the page."""
        user = create_test_user()
        self.client.force_login(user)

        response = self.client.get(f"/blog/posts/publish/", follow=True)
        self.assertEqual(response.status_code, 403)

    def test_that_view_is_shown_with_permissions(self):
        """Test that user logged in with permissions can view the page."""
        user = create_test_user(permissions=["can_publish"])
        self.client.force_login(user)

        response = self.client.get(f"/blog/posts/publish/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_that_view_redirects_to_login(self):
        """Test that publish view redirects to login page if user has not logged in."""
        response = self.client.get(f"/blog/posts/publish/", follow=True)
        self.assertRedirects(
            response, f"/accounts/login/?next=/blog/posts/publish/"
        )

    def test_that_view_works(self):
        """Test that submitted form from publish view creates a new blog post."""
        user = create_test_user(permissions=["can_publish"])
        self.client.force_login(user)

        title = "Title"
        content = "Content"

        response = self.client.post(
            f"/blog/posts/publish/",
            {"title": title, "content": content},
            follow=True,
        )
        self.assertRedirects(response, f"/blog/posts/")

        blog_post = BlogPost.objects.get(title=title)
        self.assertEqual(blog_post.title, title)
        self.assertEqual(blog_post.content, content)
        self.assertEqual(blog_post.edited_date, None)

    def test_invalid_blog_post(self):
        """Test that invalid blog post can not be published."""
        user = create_test_user(permissions=["can_publish"])
        self.client.force_login(user)

        # Empty content for either title or content is considered invalid
        title = ""
        content = ""

        response = self.client.post(
            f"/blog/posts/publish/",
            {"title": title, "content": content},
            follow=True,
        )
        self.assertEqual(len(response.context["form"].errors), 2)
        self.assertEqual(
            response.context["form"].errors["title"][0],
            "This field is required.",
        )
        self.assertEqual(
            response.context["form"].errors["content"][0],
            "This field is required.",
        )
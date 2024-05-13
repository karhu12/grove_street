from django.test import TestCase


class SignUpViewTestCase(TestCase):
    """Tests that sign up view works as intended."""

    def test_create_new_user(self):
        """Test that a new user can be created."""
        user_data = {
            "username": "test_user",
            "password": "test_password",
        }

        # Success should redirect to 'sign-up-completed' page.
        response = self.client.post("/user-management/sign-up/", user_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-management/sign-up-completed/")

    def test_attempt_create_user_with_existing_username(self):
        """Test that a new user with a username that already exists can not be created."""
        user_data = {
            "username": "test_user",
            "password": "test_password",
        }

        # Success should redirect to 'sign-up-completed' page.
        response = self.client.post("/user-management/sign-up/", user_data)
        self.assertRedirects(response, "/user-management/sign-up-completed/")

        # Failure re-renders the views with form failures shown
        response = self.client.post("/user-management/sign-up/", user_data)
        self.assertEqual(len(response.context["form"].errors), 1)
        self.assertEqual(
            response.context["form"].errors["__all__"][0],
            "Account with the given username already exists.",
        )

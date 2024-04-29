from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User

from user_management.forms import SignUpForm


class SignUpView(View):
    """View for users to create a new account."""

    def get(self, request: HttpRequest):
        """GET endpoint for rendering the sign up view."""
        return render(request, "user_management/sign_up.html", {"form": SignUpForm()})

    def post(self, request: HttpRequest):
        """POST endpoint for handling new user sign ups."""
        form = SignUpForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            User.objects.create_user(username=username, password=password)
            return redirect("sign-up-completed")

        return render(request, "user_management/sign_up.html", {"form": form})


def sign_up_completed(request: HttpRequest):
    """GET endpoint for informing the user that said account was created successfully."""
    return render(request, "user_management/sign_up_completed.html")

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    """Form user for signing up."""

    username = forms.CharField(label="Your username", max_length=256)
    password = forms.CharField(
        label="Your password", max_length=256, widget=forms.PasswordInput
    )

    def clean(self):
        """Clean form data.

        Also check if account with given username already exists.

        Raises:
            ValidationError: Invalid form data or account with username already exists.
        """
        data = super().clean()
        username = data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Account with the given username already exists.")

        return data

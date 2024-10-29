from django.urls import path

from user_management import views


urlpatterns = [
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
    path("sign-up-completed/", views.sign_up_completed, name="sign-up-completed"),
]

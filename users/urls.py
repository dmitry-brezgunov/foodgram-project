from django.urls import include, path

from .views import (Login, PasswordChange, SignUp, author_page,
                    subscriptions_page)

urlpatterns = [
        path("auth/signup/", SignUp.as_view(), name="signup"),
        path("auth/login/", Login.as_view(), name='login'),
        path("auth/password_change/", PasswordChange.as_view(),
             name='password_change'),
        path("auth/", include("django.contrib.auth.urls")),
        path("profile/<str:username>", author_page, name="author_page"),
        path("subscriptions/", subscriptions_page, name="subscriptions"),
]

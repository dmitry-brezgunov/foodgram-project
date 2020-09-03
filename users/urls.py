from django.urls import include, path

from .views import SignUp, author_page

urlpatterns = [
        path("auth/signup/", SignUp.as_view(), name="signup"),
        path("auth/", include("django.contrib.auth.urls")),
        path("profile/<str:username>", author_page, name="author_page"),
]

import pytest
from django.urls import resolve, reverse

from medium.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/api/site-users/{user.username}/"
    )
    assert resolve(f"/api/site-users/{user.username}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/api/site-users/"
    assert resolve("/api/site-users/").view_name == "api:user-list"


def test_user_me():
    assert reverse("api:user-me") == "/api/site-users/me/"
    assert resolve("/api/site-users/me/").view_name == "api:user-me"

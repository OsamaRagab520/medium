import pytest
from django.urls import resolve, reverse

from medium.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("site_users:detail", kwargs={"username": user.username})
        == f"/site-users/{user.username}/"
    )
    assert resolve(f"/site-users/{user.username}/").view_name == "site_users:detail"


def test_update():
    assert reverse("site_users:update") == "/site-users/~update/"
    assert resolve("/site-users/~update/").view_name == "site_users:update"


def test_redirect():
    assert reverse("site_users:redirect") == "/site-users/~redirect/"
    assert resolve("/site-users/~redirect/").view_name == "site_users:redirect"

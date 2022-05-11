import pytest
from django.urls import resolve, reverse

from medium.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("api:users:get_user", kwargs={"username": user.pk})
        == f"/api/users/{user.pk}/"
    )
    assert resolve(f"/api/users/{user.pk}/").view_name == "api:users:get_user"


def test_user_create():
    assert reverse("api:users:create_user") == "/api/users/create/"
    assert resolve("/api/users/create/").view_name == "api:users:create_user"


def test_user_update(user: User):
    assert reverse("api:users:update_user") == f"/api/users/{user.pk}/update"
    assert resolve(f"/api/users/{user.pk}/update").view_name == "api:users:update_user"

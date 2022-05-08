from django.shortcuts import get_object_or_404

from medium.users.models import User


def get_user(user_id: int) -> User:
    user = get_object_or_404(User, pk=user_id)
    return user

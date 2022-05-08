from django.shortcuts import get_object_or_404

from .models import User


def get_user(user_id: int):
    return get_object_or_404(User, user_id)

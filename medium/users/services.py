from typing import Any, Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email

from medium.users.models import User


class UserService:
    def create_user(self, username: str, name: str, email: str, password: str) -> User:
        username = User.normalize_username(username)
        email = BaseUserManager.normalize_email(email)

        validate_email(email)

        user: User = User(username=username, name=name, email=email)

        validate_password(password, user)
        user.password = make_password(password)

        user.save()
        return user

    def update_user(self, id: int, data: Dict[str, Any]) -> User:
        user: User = User.objects.get(pk=id)

        for field in data:
            if field == "password":
                continue

            if field == "email":
                validate_email(data.get(field))

            setattr(user, field, data.get(field))

        password: str = data.get("password")
        if password:
            validate_password(password, user)
            user.password = make_password(password)

        user.save()
        return user

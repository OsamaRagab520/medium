from typing import Any, Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjValidationError
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError

from medium.users.models import User


class UserService:
    def create_user(
        self, username: str, name: str, email: str, password: str, **other_fields
    ) -> User:
        username = User.normalize_username(username)
        email = BaseUserManager.normalize_email(email)

        try:
            validate_email(email)
        except DjValidationError as e:
            raise ValidationError(e.messages)

        user: User = User(username=username, name=name, email=email)

        try:
            validate_password(password, user)
        except DjValidationError as e:
            raise ValidationError(e.messages)
        user.password = make_password(password)

        for field in other_fields:
            setattr(user, field, other_fields[field])

        user.save()
        return user

    def update_user(self, id: int, data: Dict[str, Any]) -> User:
        user: User = User.objects.get(pk=id)

        for field in data:
            if field == "password":
                continue

            if field == "email":
                try:
                    validate_email(data.get(field))
                except DjValidationError as e:
                    raise ValidationError(e.messages)

            setattr(user, field, data.get(field))

        password: str = data.get("password")
        if password:
            try:
                validate_password(password, user)
            except DjValidationError as e:
                raise ValidationError(e.messages)
            user.password = make_password(password)

        user.save()
        return user

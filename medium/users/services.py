from typing import Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from medium.common.services import model_update
from medium.users.models import User
from medium.users.selectors import get_user


class UserService:
    def create_user(self, username: str, name: str, email: str, password: str) -> User:

        # Pack user data for validation
        user: User = User(username=username, name=name, email=email)

        # Password validation
        validate_password(password, user)
        user.password = make_password(password)

        # Data validation and normalization
        user.full_clean()

        # TODO Add email confirmation

        # Saving user to the database
        user.save()

        return user

    def update_user(self, user_id: int, data: Dict) -> User:

        # Fetch user instance
        user: User = get_user(user_id)

        # Update non side effect fields
        # TODO Remove email field when email confirmation is implemented
        non_side_effect_fields = ["email", "name"]

        user, _ = model_update(
            instance=user,
            fields=non_side_effect_fields,
            data=data,
        )

        # Changing password
        password: str = data.get("password")
        if password:
            validate_password(password, user)
            user.set_password(password)

        # Saving changes to the database
        user.save()

        return user

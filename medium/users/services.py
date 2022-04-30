from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from medium.users.models import User


class UserService:
    def create_user(self, name: str, email: str, password: str) -> User:
        user: User = User(name=name, email=email)
        validate_password(password, user)
        hashed_password: str = make_password(password)
        user.password = hashed_password

        user.save()
        return user

    def update_user(
        self, id: int, name: str = None, email: str = None, password: str = None
    ) -> User:
        user: User = User.objects.get(pk=id)
        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            validate_password(password, user)
            hashed_password: str = make_password(password)
            user.password = hashed_password

        user.save()
        return user

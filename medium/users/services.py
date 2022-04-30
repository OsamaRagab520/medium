from django.contrib.auth.hashers import make_password

from medium.users.models import User


class UserService:
    def create_user(self, data: dict) -> User:
        user: User = User()
        user.name = data.get("name")
        user.email = data.get("email")
        user.password = make_password(data.get("password"))
        user.save()
        return user

    def update_user(self, id: int, data: dict) -> User:
        user: User = User.objects.get(pk=id)
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        password: str = data.get("password")
        user.password = make_password(password) if password else user.password
        user.save()
        return user

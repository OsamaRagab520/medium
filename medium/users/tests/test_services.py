from django.core.exceptions import ValidationError
from django.test import TestCase
from users.models import User
from users.services import UserService


class UserServiceTestCase(TestCase):
    def test_create_user(self):
        data: dict = {"name": "Hazem", "email": "user1@medium.com", "password": "123"}
        service: UserService = UserService()
        user: User = service.create_user(data)
        self.assertEqual(user.name, data.get("name"))
        self.assertNotEqual(user.pk, None)

    def test_create_user_without_email(self):
        data: dict = {"name": "Hazem", "password": "123"}
        service: UserService = UserService()
        with self.assertRaises(ValidationError):
            service.create_user(data)

    def test_create_user_with_already_exist_email(self):
        data: dict = {"name": "Hazem", "email": "user1@medium.com", "password": "123"}
        service: UserService = UserService()
        with self.assertRaises(ValidationError):
            service.create_user(data)
            service.create_user(data)

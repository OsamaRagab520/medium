from django.test import TestCase

from medium.users.models import User
from medium.users.services import UserService


class UserServiceTestCase(TestCase):
    def test_create_user(self):
        service: UserService = UserService()
        user: User = service.create_user(
            username="hazemessam",
            name="Hazem",
            email="user1@medium.com",
            password="Tt123456789huehw",
        )
        self.assertEqual(user.name, "Hazem")
        self.assertNotEqual(user.pk, None)

    def test_create_user_without_email(self):
        service: UserService = UserService()
        with self.assertRaises(Exception):
            service.create_user(
                username="hazemessam", name="Hazem", password="Tt123456789huehw"
            )

    def test_create_user_with_already_exist_email(self):
        service: UserService = UserService()
        with self.assertRaises(Exception):
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium.com",
                password="Tt123456789huehw",
            )
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium.com",
                password="Tt123456789huehw",
            )

    def test_create_user_with_already_exist_username(self):
        service: UserService = UserService()
        with self.assertRaises(Exception):
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium.com",
                password="Tt123456789huehw",
            )
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user2@medium.com",
                password="Tt123456789huehw",
            )

    def test_create_user_with_invalid_email(self):
        service: UserService = UserService()
        with self.assertRaises(Exception):
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1",
                password="Tt123456789huehw",
            )
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium",
                password="Tt123456789huehw",
            )
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1medium.com",
                password="Tt123456789huehw",
            )

    def test_create_user_with_weak_password(self):
        service: UserService = UserService()
        with self.assertRaises(Exception):
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium.com",
                password="123",
            )
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium.com",
                password="user1",
            )
            service.create_user(
                username="hazemessam",
                name="Hazem",
                email="user1@medium.com",
                password="hazem",
            )

    def test_update_user(self):
        service: UserService = UserService()
        user: User = service.create_user(
            username="hazemessam",
            name="Hazem",
            email="user1@medium.com",
            password="Tt123456789huehw",
        )
        updated_user: User = service.update_user(user.pk, {"name": "Hazem Essam"})
        self.assertEqual(updated_user.name, "Hazem Essam")

    def test_update_unexisting_user(self):
        service: UserService = UserService()
        with self.assertRaises(Exception):
            service.update_user(1000, {"name": "Hazem Essam"})

    def test_update_user_with_weak_password(self):
        service: UserService = UserService()
        user: User = service.create_user(
            username="hazemessam",
            name="Hazem",
            email="user1@medium.com",
            password="Tt123456789huehw",
        )
        with self.assertRaises(Exception):
            service.update_user(user.pk, {"password": "1234"})

    def test_update_user_with_already_existing_username(self):
        service: UserService = UserService()
        user: User = service.create_user(
            username="hazemessam",
            name="Hazem",
            email="user1@medium.com",
            password="Tt123456789huehw",
        )
        service.create_user(
            username="hazemessam2",
            name="Hazem",
            email="user2@medium.com",
            password="Tt123456789huehw",
        )
        with self.assertRaises(Exception):
            service.update_user(user, user, {"username": "hazemessam2"})

from urllib import request

from djagno.core.files import File
from django.test import TestCase

from medium.profiles.services import ProfileService
from medium.users.models import User


class ProfileServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            email="test_user@dummy.com",
            password="Test_pass123!",
        )
        self.test_img_url = """https://cdn.dribbble.com/users/278089/screenshots/1
            4822259/media/4dd328a4a29049e3c67f0a55184a4633.jpeg?compress=1&resize=400x300"""
        self.img = request.urlretrieve(self.test_img_url)[0]
        self.service = ProfileService(
            self.user.id, File(open(self.img, "rb")), File(open(self.img, "rb"))
        )

    def tearDown(self):
        self.user.delete()

    def test_create_profile(self):
        profile = self.service.create_profile(
            about_text="test_about_text",
            short_bio="test_short_bio",
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.about_text, "test_about_text")
        self.assertEqual(profile.short_bio, "test_short_bio")
        self.assertEqual(profile.profile_views, 0)
        self.assertEqual(profile.accent_color, "#FFFFFF")
        self.assertEqual(profile.background_color, "#FFFFFF")

    def test_create_profile_with_invalid_data(self):
        with self.assertRaises(Exception):
            self.service.create_profile(
                about_text=1,
                short_bio="test_short_bio",
            )

    def test_create_profile_with_same_user_id(self):
        self.service.create_profile(
            about_text="test_about_text",
            short_bio="test_short_bio",
        )
        with self.assertRaises(Exception):
            self.service.create_profile(
                about_text="test_about_text",
                short_bio="test_short_bio",
            )

    def test_update_profile(self):
        profile = self.service.create_profile(
            about_text="test_about_text",
            short_bio="test_short_bio",
        )
        profile = self.service.update_profile(
            data={
                "about_text": "test_about_text_updated",
                "short_bio": "test_short_bio_updated",
            }
        )

        self.assertEqual(profile.about_text, "test_about_text_updated")
        self.assertEqual(profile.short_bio, "test_short_bio_updated")

    def test_update_profile_with_invalid_data(self):
        self.service.create_profile(
            about_text="test_about_text",
            short_bio="test_short_bio",
        )
        with self.assertRaises(Exception):
            self.service.update_profile(
                data={
                    "about_text": 42,
                    "short_bio": 42,
                }
            )

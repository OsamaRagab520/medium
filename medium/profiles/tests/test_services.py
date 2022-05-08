from urllib import request

from django.core.files import File
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
        self.non_existent_user_id = self.user.id + 1
        self.test_img_url = "https://bit.ly/3vQgl0t"
        self.img = request.urlretrieve(self.test_img_url)[0]
        self.service = ProfileService()

    def test_create_profile(self):
        profile = self.service.create_profile(
            self.user.id,
            about_text="test_about_text",
            short_bio="test_short_bio",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.about_text, "test_about_text")
        self.assertEqual(profile.short_bio, "test_short_bio")
        self.assertEqual(profile.profile_views, 0)
        self.assertEqual(profile.accent_color, "#FFFFFF")
        self.assertEqual(profile.background_color, "#FFFFFF")

    def test_create_profile_with_same_user(self):
        self.service.create_profile(
            self.user.id,
            about_text="test_about_text",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        with self.assertRaises(Exception):
            self.service.create_profile(
                self.user.id,
                about_text="test_about_text",
                profile_pic=File(open(self.img, "rb")),
                header_pic=File(open(self.img, "rb")),
            )

    def test_create_profile_with_invalid_data(self):
        with self.assertRaises(Exception):
            self.service.create_profile(
                self.user.id,
                about_text="test_about_text",
                short_bio="test_short_bio",
                profile_pic=File(open(self.img, "rb")),
                header_pic=None,
            )

    def test_create_profile_with_nonexistentuser(self):
        with self.assertRaises(Exception):
            self.service.create_profile(
                self.non_existent_user_id,
                about_text="test_about_text",
                short_bio="test_short_bio",
                profile_pic=File(open(self.img, "rb")),
                header_pic=File(open(self.img, "rb")),
            )

    def test_update_profile(self):
        profile = self.service.create_profile(
            self.user.id,
            about_text="test_about_text",
            short_bio="test_short_bio",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        profile = self.service.update_profile(
            self.user.id,
            data={
                "about_text": "test_about_text_updated",
                "short_bio": "test_short_bio_updated",
            },
        )

        self.assertEqual(profile.about_text, "test_about_text_updated")
        self.assertEqual(profile.short_bio, "test_short_bio_updated")

    def test_update_non_existent_profile(self):
        with self.assertRaises(Exception):
            self.service.update_profile(
                self.non_existent_user_id,
                data={
                    "about_text": "test_about_text_updated",
                    "short_bio": "test_short_bio_updated",
                },
            )

    def test_update_profile_with_invalid_data(self):
        self.service.create_profile(
            self.user.id,
            about_text="test_about_text",
            short_bio="test_short_bio",
            profile_pic=File(open(self.img, "rb")),
            header_pic=File(open(self.img, "rb")),
        )
        with self.assertRaises(Exception):
            self.service.update_profile(
                data={
                    "profile_views": "Nan",
                }
            )

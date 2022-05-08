from typing import Any, BinaryIO, Dict, Optional

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from medium.profiles.models import Profile
from medium.users.models import User


class ProfileService:
    def create_profile(
        self,
        user_id: int,
        about_text: str,
        profile_pic: BinaryIO,
        header_pic: BinaryIO,
        profile_views: Optional[int] = None,
        short_bio: Optional[str] = None,
        accent_color: Optional[str] = None,
        background_color: Optional[str] = None,
    ) -> Profile:
        try:
            user: User = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise DRFValidationError({"user": f"User {user_id} does not exist"})

        if Profile.objects.filter(user_id=user_id).exists():
            raise DRFValidationError({"user": f"User {user_id} already has a profile"})

        try:
            profile = Profile(
                user=user,
                about_text=about_text,
                profile_pic=profile_pic,
                header_pic=header_pic,
            )

            if profile_views:
                profile.profile_views = profile_views
            if short_bio:
                profile.short_bio = short_bio
            if accent_color:
                profile.accent_color = accent_color
            if background_color:
                profile.background_color = background_color

            profile.full_clean()
            profile.save()
            return profile

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

    def update_profile(self, user_id: int, data: Dict[str, Any]) -> Profile:
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            raise DRFValidationError(
                {"user": f"User {self.user_id} does not have a profile"}
            )

        try:
            for field in data:
                setattr(profile, field, data[field])

            profile.full_clean()
            profile.save()
            return profile

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

from typing import Any, BinaryIO, Optional

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from medium.common.services import model_update
from medium.profiles.models import Profile
from medium.users.models import User


class ProfileService:
    def create_profile(
        self,
        *,
        user: User,
        about_text: str,
        profile_pic: BinaryIO,
        header_pic: BinaryIO,
        profile_views: Optional[int] = 0,
        short_bio: Optional[str] = "no bio",
        accent_color: Optional[str] = "#FFFFFF",
        background_color: Optional[str] = "#FFFFFF",
    ) -> Profile:
        try:
            user: User = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise DRFValidationError({"user": f"User {user.id} does not exist"})

        if Profile.objects.filter(user_id=user.id).exists():
            raise DRFValidationError({"user": f"User {user.id} already has a profile"})

        try:
            profile = Profile(
                user=user,
                about_text=about_text,
                profile_pic=profile_pic,
                header_pic=header_pic,
                profile_views=profile_views,
                short_bio=short_bio,
                accent_color=accent_color,
                background_color=background_color,
            )

            profile.full_clean()
            profile.save()
            return profile

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

    def update_profile(
        self,
        *,
        user: User,
        data: dict[str, Any],
    ) -> Profile:
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise DRFValidationError(
                {"user": f"User {self.user.id} does not have a profile"}
            )
        try:

            non_side_effect_fields = [
                "about_text",
                "profile_pic",
                "header_pic",
                "profile_views",
                "short_bio",
                "accent_color",
                "background_color",
            ]

            profile, _ = model_update(
                instance=profile,
                fields=non_side_effect_fields,
                data=data,
            )

            profile.full_clean()
            profile.save()
            return profile

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

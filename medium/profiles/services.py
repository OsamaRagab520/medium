from typing import Any, BinaryIO, Dict, Optional

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from medium.common.services import model_update
from medium.profiles.models import Profile
from medium.users.models import User


class ProfileService:
    def __init__(self, user_id: int, profile_pic: BinaryIO, header_pic: BinaryIO):
        self.user_id = user_id
        self.profile_pic = profile_pic
        self.header_pic = header_pic

    def create_profile(
        self,
        about_text: str,
        **optional_fields: Optional[Dict[str, Any]],
    ) -> Profile:
        try:
            user: User = User.objects.get(id=self.user_id)
            profile = Profile(
                user=user,
                about_text=about_text,
                profile_pic=self.profile_pic,
                header_pic=self.header_pic,
            )

            for field in optional_fields:
                setattr(profile, field, optional_fields[field])

            profile.full_clean()
            profile.save()
            return profile

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

    def update_profile(self, data: Dict[str, Any]) -> Profile:
        try:
            profile = Profile.objects.get(user_id=self.user_id)
            profile_fields = [
                "short_bio",
                "about_text",
                "profile_pic",
                "profile_views",
                "accent_color",
                "background_color",
                "header_pic",
            ]

            for field in ["profile_pic", "header_pic"]:
                if field in data:
                    setattr(self, field, data[field])

            new_profile, _ = model_update(
                instance=profile, fields=profile_fields, data=data
            )
            return new_profile

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

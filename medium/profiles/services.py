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
        **optional_fields: Optional[Dict[str, Any]],
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

            for field in optional_fields:
                setattr(profile, field, optional_fields[field])

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

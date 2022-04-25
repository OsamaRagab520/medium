from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # Disable fname and lname fields
    first_name = None
    last_name = None

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    # Remaining fields lays in AbstractUser model

    def get_absolute_url(self):
        """
        Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

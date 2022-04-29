from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# LOCAL IMPORTS GOES HERE!
from .utils import header_pic_url, profile_pic_url, resize


class Profile(models.Model):
    class Colors(models.TextChoices):
        BLACK = "#000000", _("Black")
        WHITE = "#FFFFFF", _("White")

    class Meta:
        verbose_name = _("Profiles")
        ordering = ["-created_at"]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    short_bio = models.CharField(max_length=255, default="no bio")
    about_page_url = models.TextField()
    profile_pic_url = models.ImageField(upload_to=profile_pic_url)
    profile_views = models.IntegerField(default=0)
    accent_color = models.CharField(
        max_length=7, choices=Colors.choices, default=Colors.WHITE
    )
    background_color = models.CharField(
        max_length=7, choices=Colors.choices, default=Colors.WHITE
    )
    header_pic_url = models.ImageField(upload_to=header_pic_url)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        resize(self.profile_pic_url, (200, 200))
        resize(self.header_pic_url, (200, 200))
        super().save(*args, **kwargs)

from django.db import models
import uuid
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model


def profile_pic_url(instance, filename):
    return f'profile_images/{instance.user}/{filename}'

def header_pic_url(instance, filename):
    return f'header_images/{instance.user}/{filename}'

User = get_user_model()

class ResizeImageMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def resize(self, imageField: models.ImageField, size:tuple):
        im = Image.open(imageField)
        source_image = im.convert('RGB')
        source_image.thumbnail(size) 
        output = BytesIO()
        source_image.save(output, format='JPEG') 
        output.seek(0)

        content_file = ContentFile(output.read())   
        file = File(content_file)

        random_name = f'{uuid.uuid4()}.jpeg'
        imageField.save(random_name, file, save=False)
    
    class Meta:
        ordering = ('-updated_at',)

class Profile(ResizeImageMixin):
    COLORS = (
        ("#000000", "BLACK"),
        ("#FFFFFF", "WHITE")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, default='no bio')
    about_page_url = models.TextField()
    profile_pic_url = models.ImageField(upload_to=profile_pic_url)
    profile_views = models.IntegerField(default=0)
    accent_color = models.CharField(max_length=7, choices=COLORS)
    background_color = models.CharField(max_length=7, choices=COLORS)
    header_pic_url = models.ImageField(upload_to=header_pic_url)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = ('User Profile')
    
    def save(self, *args, **kwargs):
        self.resize(self.profile_pic_url, (200, 200))
        self.resize(self.header_pic_url, (200, 200))
        super().save(*args, **kwargs)

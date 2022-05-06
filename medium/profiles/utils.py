import uuid
from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


def get_profile_pic_url(instance, filename):
    return f"profile_images/{instance.user}/{filename}"


def get_header_pic_url(instance, filename):
    return f"header_images/{instance.user}/{filename}"


def resize(imageField: models.ImageField, size: tuple):
    im = Image.open(imageField)
    source_image = im.convert("RGB")
    source_image.thumbnail(size)
    output = BytesIO()
    source_image.save(output, format="JPEG")
    output.seek(0)
    content_file = ContentFile(output.read())
    file = File(content_file)
    random_name = f"{uuid.uuid4()}.jpeg"
    imageField.save(random_name, file, save=False)

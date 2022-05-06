# Generated by Django 3.2.13 on 2022-05-06 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import medium.profiles.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_text', models.TextField()),
                ('profile_pic', models.ImageField(upload_to=medium.profiles.utils.get_profile_pic_url)),
                ('header_pic', models.ImageField(upload_to=medium.profiles.utils.get_header_pic_url)),
                ('short_bio', models.CharField(default='no bio', max_length=255)),
                ('profile_views', models.IntegerField(default=0)),
                ('accent_color', models.CharField(choices=[('#000000', 'Black'), ('#FFFFFF', 'White')], default='#FFFFFF', max_length=7)),
                ('background_color', models.CharField(choices=[('#000000', 'Black'), ('#FFFFFF', 'White')], default='#FFFFFF', max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'ordering': ['-created_at'],
            },
        ),
    ]

# Generated by Django 3.0.7 on 2024-10-16 20:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_auto_20241016_1948'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='playlist',
            new_name='playlist_model',
        ),
    ]
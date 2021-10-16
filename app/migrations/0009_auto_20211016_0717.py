# Generated by Django 3.1.13 on 2021-10-15 22:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_auto_20211016_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='updated',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='study_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
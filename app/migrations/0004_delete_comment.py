# Generated by Django 3.1.13 on 2021-10-15 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]

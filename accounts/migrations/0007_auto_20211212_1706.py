# Generated by Django 3.1.13 on 2021-12-12 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20211212_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='first_listenig',
            new_name='first_listening',
        ),
    ]

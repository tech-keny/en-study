# Generated by Django 3.1.13 on 2021-12-12 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20211212_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='first_listnig',
            new_name='first_listenig',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='max_Reading',
            new_name='max_reading',
        ),
    ]

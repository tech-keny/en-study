# Generated by Django 3.1.13 on 2021-10-15 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20211016_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(default='ここに入力'),
        ),
    ]
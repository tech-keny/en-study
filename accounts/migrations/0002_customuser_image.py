# Generated by Django 3.1.13 on 2021-10-14 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='プロフィール画像'),
        ),
    ]

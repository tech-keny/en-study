# Generated by Django 3.1.13 on 2021-10-31 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20211101_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='part',
        ),
        migrations.AddField(
            model_name='post',
            name='part',
            field=models.ManyToManyField(to='app.Part', verbose_name='Part'),
        ),
    ]

# Generated by Django 3.1.13 on 2021-12-11 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_question_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('created',)},
        ),
    ]
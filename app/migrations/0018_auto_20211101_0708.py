# Generated by Django 3.1.13 on 2021-10-31 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20211101_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='part',
            field=models.ManyToManyField(related_name='posts', to='app.Part', verbose_name='Part'),
        ),
    ]
# Generated by Django 3.1.13 on 2022-04-18 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20220419_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_total',
            field=models.IntegerField(default=0, verbose_name='最初のスコア'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='max_total',
            field=models.IntegerField(default=0, verbose_name='最高スコア'),
        ),
    ]

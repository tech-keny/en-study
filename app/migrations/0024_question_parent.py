# Generated by Django 3.1.13 on 2021-12-10 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_remove_question_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='app.question'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-26 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='allowed_habits_count',
            field=models.IntegerField(default=3),
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-26 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0004_alter_userscore_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('profile', 'Profile'), ('habit_limit', 'Habit Limit Increase')], max_length=255)),
                ('description', models.TextField()),
                ('cost', models.PositiveIntegerField()),
                ('habit_increase_amount', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='userreward',
            name='reward',
        ),
        migrations.RemoveField(
            model_name='userreward',
            name='user',
        ),
        migrations.CreateModel(
            name='PurchasedFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unlocked_at', models.DateTimeField(auto_now_add=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='scoring.feature')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rewards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Reward',
        ),
        migrations.DeleteModel(
            name='UserReward',
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-12 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0006_alter_habitinstance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringhabit',
            name='score',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='singlehabit',
            name='score',
            field=models.PositiveIntegerField(default=1),
        ),
    ]

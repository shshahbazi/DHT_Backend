# Generated by Django 5.0.7 on 2024-08-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0004_singlehabit_reminder_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitinstance',
            name='celery_task_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

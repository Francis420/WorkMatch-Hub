# Generated by Django 5.1.2 on 2025-03-30 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='extra_data',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]

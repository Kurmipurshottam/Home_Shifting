# Generated by Django 5.0.4 on 2024-05-21 15:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_user_contact_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

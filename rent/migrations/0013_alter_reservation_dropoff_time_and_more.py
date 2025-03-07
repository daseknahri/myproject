# Generated by Django 5.1.4 on 2025-02-24 01:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0012_alter_reservation_dropoff_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='dropoff_time',
            field=models.TimeField(default=datetime.datetime(2025, 2, 24, 1, 23, 40, 64615, tzinfo=datetime.timezone.utc), verbose_name='Dropoff Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_time',
            field=models.TimeField(default=datetime.datetime(2025, 2, 24, 1, 23, 40, 64615, tzinfo=datetime.timezone.utc), verbose_name='Pickup Time'),
        ),
    ]

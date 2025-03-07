# Generated by Django 5.1.4 on 2025-02-23 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0002_alter_reservation_dropoff_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='dropoff_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Dropoff Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pickup_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Pickup Time'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Total Cost'),
        ),
    ]

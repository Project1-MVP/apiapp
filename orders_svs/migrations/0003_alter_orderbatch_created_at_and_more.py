# Generated by Django 4.2.9 on 2025-01-21 17:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_svs', '0002_alter_orderbatch_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbatch',
            name='created_at',
            field=models.IntegerField(default=1737479616),
        ),
        migrations.AlterField(
            model_name='orderbatch',
            name='updated_at',
            field=models.IntegerField(default=1737479616),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='actual_delivery',
            field=models.DateTimeField(default=datetime.datetime(2026, 1, 21, 17, 13, 36, 779185, tzinfo=datetime.timezone.utc)),
        ),
    ]

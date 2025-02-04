# Generated by Django 4.2.9 on 2025-01-10 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_svs', '0010_rename_productbatch_inbound_by_productbatch_productbatch_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbatch',
            name='productBatch_DateOfExpiry',
            field=models.DateField(default=datetime.date(2124, 12, 17)),
        ),
        migrations.AlterField(
            model_name='productbatch',
            name='productBatch_created_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 10, 12, 59, 15, 814831)),
        ),
        migrations.AlterField(
            model_name='productbatchledger',
            name='order_time',
            field=models.IntegerField(default=1736513955),
        ),
    ]

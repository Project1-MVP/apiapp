# Generated by Django 4.2.16 on 2025-01-02 15:34

import backend.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_svs', '0003_alter_productbatchledger_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbatchledger',
            name='order_time',
            field=models.IntegerField(default=1735832082),
        ),
        migrations.AlterField(
            model_name='productbatchledger',
            name='order_type',
            field=models.CharField(choices=[(backend.enums.OrderType['PROVISIONING'], 'Provisioning'), (backend.enums.OrderType['SALE'], 'Sale'), (backend.enums.OrderType['BACKORDER'], 'Backorder'), (backend.enums.OrderType['RETURN'], 'Return'), (backend.enums.OrderType['EXCHANGE'], 'Exchange'), (backend.enums.OrderType['TRIAL'], 'Trial'), (backend.enums.OrderType['GIFT'], 'Gift'), (backend.enums.OrderType['PROMOTIONAL'], 'Promotional'), (backend.enums.OrderType['STOCK_ADJUSTMENT'], 'Stock Adjustment'), (backend.enums.OrderType['INTERNAL_TRANSFER'], 'Internal Transfer'), (backend.enums.OrderType['PURCHASE_ORDER'], 'Purchase Order'), (backend.enums.OrderType['STOCK_DAMAGE'], 'Stock Damage'), (backend.enums.OrderType['STOCK_RETURN'], 'Stock Return'), (backend.enums.OrderType['STOCK_ENTRY'], 'Stock Entry')], max_length=20),
        ),
    ]

# Generated by Django 4.2.16 on 2025-01-02 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_svs', '0002_productbatchcount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbatchledger',
            name='order_time',
            field=models.IntegerField(default=1735823579),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-03 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InventApp', '0007_remove_order_products_order_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.JSONField(default=list),
        ),
    ]

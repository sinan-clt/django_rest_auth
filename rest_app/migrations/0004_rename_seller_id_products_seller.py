# Generated by Django 3.2.15 on 2022-11-06 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_app', '0003_products_seller_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='seller_id',
            new_name='seller',
        ),
    ]

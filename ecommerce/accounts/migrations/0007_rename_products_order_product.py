# Generated by Django 3.2 on 2021-08-09 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='products',
            new_name='product',
        ),
    ]

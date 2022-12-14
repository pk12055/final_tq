# Generated by Django 3.1.6 on 2021-08-12 08:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_quantity',
            new_name='added_product_quantity',
        ),
        migrations.AddField(
            model_name='product',
            name='remaining_product_quantity',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, null=True, size=None),
        ),
    ]

# Generated by Django 3.1.6 on 2021-07-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_store_shop_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='visit',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
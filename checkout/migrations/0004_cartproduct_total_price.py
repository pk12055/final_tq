# Generated by Django 3.1.6 on 2021-08-16 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210812_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]
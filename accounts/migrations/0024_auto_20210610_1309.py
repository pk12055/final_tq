# Generated by Django 3.1.6 on 2021-06-10 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20210610_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_quantity',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_size',
            field=models.CharField(choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=255, null=True),
        ),
    ]
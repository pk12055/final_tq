# Generated by Django 3.1.6 on 2021-06-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='file',
            field=models.ImageField(null=True, upload_to='media/', verbose_name=''),
        ),
    ]

# Generated by Django 3.1.6 on 2021-07-01 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_auto_20210701_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
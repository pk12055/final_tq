# Generated by Django 3.1.6 on 2021-05-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210527_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]

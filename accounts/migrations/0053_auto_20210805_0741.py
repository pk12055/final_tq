# Generated by Django 3.1.6 on 2021-08-05 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_auto_20210805_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='first_main_text',
            field=models.TextField(blank=True, default='1st Main Category', null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='second_main_text',
            field=models.TextField(blank=True, default='2nd Main Category', null=True),
        ),
    ]
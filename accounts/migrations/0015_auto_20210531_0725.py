# Generated by Django 3.1.6 on 2021-05-31 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210528_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storefollow',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_store', to='accounts.store'),
        ),
    ]
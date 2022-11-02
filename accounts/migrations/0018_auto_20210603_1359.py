# Generated by Django 3.1.6 on 2021-06-03 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20210531_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='brand_store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_brands', to='accounts.store'),
        ),
    ]
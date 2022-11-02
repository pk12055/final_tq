# Generated by Django 3.1.6 on 2021-06-22 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20210621_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('is_same_as_delivery', models.BooleanField(default=False)),
                ('address_type', models.CharField(choices=[('Home', 'Home'), ('Office', 'Office'), ('Other', 'Other')], default='Home', max_length=255)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_addresses', to='accounts.address')),
                ('billing_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_billing_addresses', to='accounts.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_billing_addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
# Generated by Django 3.1.6 on 2021-05-31 07:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210531_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='follower_count',
            field=models.ManyToManyField(blank=True, default=None, related_name='store_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 3.1.6 on 2021-07-13 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0048_auto_20210712_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('main_pic_1', models.ImageField(blank=True, null=True, upload_to='')),
                ('main_pic_2', models.ImageField(blank=True, null=True, upload_to='')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_homecategory', to='accounts.brand')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

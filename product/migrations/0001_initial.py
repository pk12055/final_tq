# Generated by Django 3.1.6 on 2021-07-16 16:39

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(blank=True, max_length=255, null=True)),
                ('product_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_price', models.IntegerField(blank=True, null=True)),
                ('product_category', models.CharField(blank=True, choices=[('Activewears', 'Activewears'), ('Dresses', 'Dresses'), ('Jackets And Coats', 'Jackets And Coats'), ('Jumpsuits and Playsuits', 'Jumpsuits and Playsuits'), ('Knitwear', 'Knitwear'), ('Swimwear', 'Swimwear'), ('Tops', 'Tops'), ('Trouser', 'Trouser'), ('Accessories', 'Accessories'), ('Clothing', 'Clothing'), ('Other', 'Other')], max_length=255, null=True)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('product_size', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, null=True, size=None)),
                ('product_quantity', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, null=True, size=None)),
                ('product_color', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, null=True, size=None)),
                ('product_material', models.CharField(blank=True, max_length=255, null=True)),
                ('product_designer', models.CharField(blank=True, max_length=255, null=True)),
                ('is_sale', models.BooleanField(default=False)),
                ('product_sale_type', models.CharField(blank=True, choices=[('Value', 'Value'), ('Percentage', 'Percentage')], max_length=255, null=True)),
                ('product_sale_amount', models.IntegerField(blank=True, null=True)),
                ('tag_1', models.TextField(blank=True, null=True)),
                ('tag_2', models.TextField(blank=True, null=True)),
                ('tag_3', models.TextField(blank=True, null=True)),
                ('product_for', models.CharField(blank=True, choices=[('WOMEN', 'WOMEN'), ('MEN', 'MEN'), ('BOTH', 'BOTH')], max_length=255, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_product', to='accounts.brand')),
                ('favourite', models.ManyToManyField(blank=True, default=None, related_name='favourite', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_product', to='accounts.store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_product', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('reviews', models.CharField(blank=True, max_length=255, null=True)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_product', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_product_review', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('p_image', models.ImageField(upload_to='media/')),
                ('order_img', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(choices=[('FAVOURITE', 'FAVOURITE'), ('UNFavourite', 'UNFAVOURITE')], default='UNFAVOURITE', max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_product', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

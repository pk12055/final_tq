from django.db import models
from django.contrib.postgres.fields import ArrayField

from shared.models import BaseTimeStampModel
from shared.constants import (
    Favouritechoice, QuantityType, SaleType, CategoryType, productFor
)


class Product(BaseTimeStampModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_product')
    store = models.ForeignKey('accounts.Store', on_delete=models.CASCADE, related_name='store_product', null=True)
    brand = models.ForeignKey('accounts.Brand', on_delete=models.CASCADE, related_name='brand_product')
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_pic = models.ImageField(null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    product_category = models.CharField(max_length=255, choices=CategoryType.CATEGORYTYPE, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    remaining_size_and_quantity = models.CharField(max_length=255, null=True, blank=True)
    product_color = ArrayField(models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)
    product_material = models.CharField(max_length=255, null=True, blank=True)
    product_designer = models.CharField(max_length=255, null=True, blank=True)
    product_size_and_quantity = models.CharField(max_length=255, null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    favourite = models.ManyToManyField('accounts.User', default=None, blank=True, related_name='favourite')
    product_sale_type = models.CharField(max_length=255, choices=SaleType.SALETYPE, null=True, blank=True)
    product_sale_amount = models.IntegerField(null=True, blank=True)
    tag_1 = models.TextField(null=True, blank=True)
    tag_2 = models.TextField(null=True, blank=True)
    tag_3 = models.TextField(null=True, blank=True)
    product_for = models.CharField(max_length=255, choices=productFor.PRODUCTFOR, null=True, blank=True)
    product_size = ArrayField(models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)
    product_quantity = ArrayField(models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)

    def __str__(self):
        return str(self.product_name)

    @property
    def num_favourite(self):
        return self.favourite.all().count()


class Favourite(BaseTimeStampModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='favourite_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favourite_product')
    value = models.CharField(max_length=20, default='UNFAVOURITE', choices=Favouritechoice.FAVOURITECHOICE)

    def __str__(self):
        return str(self.product.id)


class ProductReview(BaseTimeStampModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_product_review')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')
    reviews = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.product.id)


class ProductImage(BaseTimeStampModel):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    p_image = models.ImageField(upload_to='media/')
    order_img = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name 


class ProductVariations(BaseTimeStampModel):
    product = models.ForeignKey(Product, related_name='product_variation', on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    product_pic = models.ImageField(null=True, blank=True)
    product_pic_1 = models.ImageField(null=True, blank=True)
    product_pic_2 = models.ImageField(null=True, blank=True)
    product_pic_3 = models.ImageField(null=True, blank=True)
    product_pic_4 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.color 
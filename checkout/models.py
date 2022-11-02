from django.db import models

from shared.models import BaseTimeStampModel
from shared.constants import AddressType


class CartProduct(BaseTimeStampModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bag_user')
    bag_product = models.ForeignKey('product.Product', related_name='bad_produt', on_delete=models.CASCADE, null=True)
    is_bag = models.BooleanField(default=False)
    size = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)
    total_payable = models.FloatField(default=0)


    def __str__(self):
        return str(self.bag_product.id)


class BillingAddress(BaseTimeStampModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_billing_addresses')
    billing_product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='product_billing_addresses')
    email = models.EmailField(unique=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    is_same_as_delivery = models.BooleanField(default=False)
    address_type = models.CharField(max_length=255, choices=AddressType.ADDRESSTYPE, default=AddressType.home)

    def __str__(self):
        return self.user.email


class Checkout(BaseTimeStampModel):
    user =  models.ForeignKey('accounts.User', related_name="user_payment", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name="product_payment", on_delete=models.CASCADE)
    number_of_item = models.IntegerField(default=1)
    amount = models.FloatField(default=0, blank=True, null=True)
    transaction_token = models.CharField(max_length=500)


    def __str__(self):
        return str(self.user)


class UserOrder(BaseTimeStampModel):
    user =  models.ForeignKey('accounts.User', related_name="order_user", on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', related_name="order_product", on_delete=models.CASCADE)
    is_product_delivered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product.id)

from django.contrib import admin

from checkout.models import CartProduct, BillingAddress, UserOrder, Checkout
# Register your models here.


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['is_bag', 'bag_product']
    raw_id_fields = ['bag_product']


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'is_same_as_delivery', 'user', 'billing_product']
    raw_id_fields = ['user', 'billing_product']


class UserOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'is_product_delivered']
    raw_id_fields = ['user', 'product']


admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(Checkout)
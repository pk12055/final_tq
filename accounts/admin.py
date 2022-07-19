from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import (
    User, Address, BrandInsight, Brand, Store, StoreImage, BrandFollow, StoreFollow,
    BrandCategory, WhoWeAre, Country, State, BrandStyle, Category
)
# Register your models here.


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'user_type', 'profile_pic', 'is_email_verified','code']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'dob')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('User Profile', {
            'classes': ('wide',),
            'fields': ('profile_pic', 'user_type', 'brand_name', 'country', 'city', 'is_email_verified','code')
        }),
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'user', 'country']


class BrandInsightAdmin(admin.ModelAdmin):
    list_display = ['brand', 'shops_count', 'items_sold_count']
    raw_id_fields = ['brand']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['user', 'brand_name', 'brand_address']
    raw_id_fields = ['user']


class StoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'shop_name', 'shop_type', 'shop_address']
    raw_id_fields = ['user']


class StoreImageAdmin(admin.ModelAdmin):
    list_display = ['store', 'name', 'file', 'order_img']
    raw_id_fields = ['store']


class BrandFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'brand', 'value']
    raw_id_fields = ['user', 'brand']


class StoreFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'value']
    raw_id_fields = ['user', 'store']


class BrandCategoryAdmin(admin.ModelAdmin):
    list_display = ['brand', 'main_pic_1', 'main_pic_2']
    raw_id_fields = ['brand']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['brand', 'main_pic_1', 'main_pic_2', 'first_main_text', 'second_main_text']
    raw_id_fields = ['brand']


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(BrandInsight, BrandInsightAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(StoreImage, StoreImageAdmin)
admin.site.register(BrandFollow, BrandFollowAdmin)
admin.site.register(StoreFollow, StoreFollowAdmin)
admin.site.register(BrandCategory, BrandCategoryAdmin)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(WhoWeAre)
admin.site.register(BrandStyle)
admin.site.register(Category, CategoryAdmin)
from django.contrib import admin

from product.models import ProductReview, Product, Favourite, ProductImage, ProductVariations


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'reviews', 'rating']
    raw_id_fields = ['user', 'product']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'brand', 'product_name', 'product_price', 'product_size', 'product_color', 'product_material']
    raw_id_fields = ['user', 'store', 'brand']


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'value']
    raw_id_fields = ['user', 'product']


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'p_image']
    raw_id_fields = ['product']


class ProductVariationsAdmin(admin.ModelAdmin):
    list_display = ['product', 'color']
    raw_id_fields = ['product']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductVariations, ProductVariationsAdmin)
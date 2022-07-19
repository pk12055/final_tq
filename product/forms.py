from django import forms
from django.forms import ModelForm

from product.models import Product, ProductReview, ProductImage, ProductVariations


class AddProductForm(ModelForm):

    class Meta:
        fields = (
            'product_name', 'product_price', 'product_description', 'product_color', 'product_material',
            'tag_3', 'tag_2', 'tag_1', 'product_category',
            'product_pic', 'product_size_and_quantity'
        )
        model = Product


class ProductReviewForm(forms.ModelForm):
    """
    This from is used to save the ProductReview Information.
    """

    class Meta:
        model = ProductReview
        fields = ('product', 'reviews', 'rating')


class ProductImageForm(forms.ModelForm):
    """
    This from is used to save the ProductReview Information.
    """

    class Meta:
        model = ProductImage
        fields = ('p_image',)


class ProductVariationsForm(forms.ModelForm):
    """
    This from is used to save the ProductReview Information.
    """

    class Meta:
        model = ProductVariations
        fields = '__all__'

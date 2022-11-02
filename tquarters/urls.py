"""tquarters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, re_path, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_view
from product import views as products_view
from checkout import views as checkouts_view


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    re_path(r'^admin/', admin.site.urls),

    # accounts url:
    re_path(r'^$', accounts_view.homepage, name='homepage'),
    re_path(r'^sign-up/$', accounts_view.signup, name='signup'),
    re_path(r'^brand-signup/$', accounts_view.brand_signup, name='brand_signup'),
    re_path(r'^reset-link-sent/$', accounts_view.reset_link_sent, name='reset_link_sent'),
    re_path(r'^login/$', accounts_view.login_user, name='login'),
    re_path(r'^logout/$', accounts_view.logout_user, name='logout'),
    re_path(r'^email-validation/', accounts_view.email_validation, name='email_validation'),
    re_path(r'^verify/email/(?P<key>[\w-]+)$', accounts_view.verify_email, name='verify_email'),
    re_path(r'^resend-email/$', accounts_view.resend_email, name='resend_email'),
    re_path(r'^forgot-password/$', accounts_view.forgot_password, name='forgot_password'),
    re_path(r'^reset-password$', accounts_view.reset_password, name='reset-password'),
    re_path(r'^accounts/$', accounts_view.account, name='account'),
    re_path(r'^update-password/$', accounts_view.update_password, name='update_password'),
    re_path(r'^get_address/$', accounts_view.get_address, name='get_address'),
    re_path(r'^upload-image/$', accounts_view.upload_image, name='upload-image'),
    re_path(r'^remove-image/$', accounts_view.remove_image, name='remove-image'),
    re_path(r'^send-referral-alert/$', accounts_view.send_referral_alert, name='send_referral_alert'),
    re_path(r'^categories/$', accounts_view.categories, name='categories'),
    re_path(r'^bussiness/$', accounts_view.bussiness, name='bussiness'),
    re_path(r'^get-in-touch/(?P<key>[\w-]+)$', accounts_view.get_in_touch, name='get_in_touch'),
    re_path(r'^main-search/$', accounts_view.main_search, name='main_search'),
    re_path(r'^get_sub_info/$', accounts_view.get_sub_info, name="get_sub_info"),
    re_path(r'^upload-brand-image/$', accounts_view.upload_brand_image, name='upload-brand-image'),
    re_path(r'^contact-us-form/$', accounts_view.contact_us_view, name='contact_us_view'),

    # custom shop urls:
    re_path(r'^brand-homepage-edit/(?P<key>[\w-]+)$', accounts_view.brand_homepage, name='brand_homepage_edit'),
    re_path(r'^brand_style/$', accounts_view.brand_style, name='brand_style'),
    re_path(r'^brand-category-edit/(?P<key>[\w-]+)$', accounts_view.brand_category, name='brand_category_edit'),
    re_path(r'^brand-sale-edit/(?P<key>[\w-]+)$', accounts_view.brand_sale, name='brand_sale_edit'),
    re_path(r'^who-we-are-edit/(?P<key>[\w-]+)$', accounts_view.who_we_are, name='who_we_are_edit'),
    re_path(r'^brand-category/(?P<key>[\w-]+)$', accounts_view.brand_detail_category, name='brand_detail_category'),
    re_path(r'^brand-sale/(?P<key>[\w-]+)$', accounts_view.brand_detail_sale, name='brand_detail_sale'),
    re_path(r'^who-we-are/(?P<key>[\w-]+)$', accounts_view.brand_who_we_are, name='brand_who_we_are'),
    re_path(r'^brand-homepage/(?P<key>[\w-]+)/$', accounts_view.brand_detail_homepage, name='brand_detail_homepage'),

    # brand urls:
    re_path(r'^brand-detail/(?P<key>[\w-]+)/$', accounts_view.brand_detail, name='brand_detail'),
    re_path(r'^brand-list/$', accounts_view.brand_list, name='brand_list'),
    re_path(r'^followbrand/$', accounts_view.follow_brand, name='follow_brand'),
    re_path(r'^brand-filter/$', accounts_view.brand_filter, name='brand_filter'),


    re_path(r'^brand-filter/$', accounts_view.brand_filter, name='brand_filter'),

    # store urls:
    re_path(r'^add-store/$', accounts_view.add_store, name='add_store'),
    re_path(r'^add-brand-store/$', accounts_view.add_brand_store, name='add_brand_store'),
    re_path(r'^store-list/$', accounts_view.store_list, name='store_list'),
    re_path(r'^store-filter/$', accounts_view.store_filter, name='store_filter'),
    re_path(r'^follow-store/$', accounts_view.follow_store, name='follow_store'),

    # checkouts urls:
    re_path(r'^checkout-login-user/(?P<key>[\w-]+)$', checkouts_view.checkout_login_user, name='checkout_login_user'),
    re_path(r'^checkout-signup/(?P<key>[\w-]+)$', checkouts_view.checkout_signup, name='checkout_signup'),
    re_path(r'^bill-pay/$', checkouts_view.bill_pay, name="bill_pay"),
    re_path(r'^checkout/(?P<key>[\w-]+)$', checkouts_view.checkout, name='checkout'),
    re_path(r'^add-to-bag/(?P<key>[\w-]+)/$', checkouts_view.add_to_bag, name='add_to_bag'),
    re_path(r'^cart/$', checkouts_view.cart, name='cart'),
    re_path(r'^billing-address/(?P<key>[\w-]+)/$', checkouts_view.billing_address, name='billing_address'),
    re_path(r'^remove-cart/(?P<key>[\w-]+)/$', checkouts_view.remove_cart, name='remove_cart'),

    # product urls:
    re_path(r'^product/edit-product/(?P<key>[\w-]+)$', products_view.edit_product, name='edit_product'),
    re_path(r'^product/add-product/(?P<key>[\w-]+)/$', products_view.add_product, name='add_product'),
    re_path(r'^product-list/$', products_view.product_list, name='product_list'),
    re_path(r'^product/filter-product/$', products_view.products_filter, name='products_filter'),
    re_path(r'^favourite/$', products_view.favourite, name='favourite'),
    re_path(r'^product/product-detail/(?P<key>[\w-]+)/$', products_view.product_detail, name='product_detail'),
    re_path(r'^add-more-product-img/$', products_view.product_img, name='product_img'),
    re_path(r'^productimage-delete/$', products_view.productimage_delete, name="productimage_delete"),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
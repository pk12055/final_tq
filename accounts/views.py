import uuid
import json
import datetime
from datetime import timedelta
from django.utils import timezone
import random
import string
import stripe

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from itertools import chain
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from shared.constants import SizeType

from accounts.forms import (
    SignUpForm, LoginForm, UpdatePasswordForm, UserInfoForm, AddressForm,
    StoreInfoForm, BrandInfoForm, BrandCategoryForm, WhoWeAreForm, CategoryForm
)

from accounts.models import (
    User, PasswordRecover, Address, BrandInsight, Brand, Store,
    StoreImage, BrandFollow, StoreFollow, BrandCategory,
    WhoWeAre, State, City, Country, BrandStyle, Category
)

from checkout.models import UserOrder
from product.models import Product, ProductReview

from shared.mailing import email_verify_request, referral_request, contact_us

stripe.api_key = settings.STRIPE_KEYS['API_KEY']


def signup(request):
    """
    This function is used to register the user.
    """

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        # Create new user and login.
        if form.is_valid():
            user_obj = User.objects.create(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                user_type=request.POST['user_type']
            )
            user_obj.set_password(form.cleaned_data['password'])
            user_obj.save()

            login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')

            if user_obj.user_type == "Brand":
                return redirect('brand_signup')

            return redirect('account')

        return render(request, 'accounts/signup.html', {'form': form, 'join': 'join'})
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'join': 'join'})


def login_user(request):
    """
    Function is used to login the user.
    """

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if user is not None:
                auth_login(request, user)
                messages.success(request, "You are logged in successfully!")

                return redirect("account")
            else:
                form.add_error('email', 'Email or Password is wrong')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context=context)


@login_required
def logout_user(request):
    """
    Function is used to logout the user.
    """

    logout(request)
    return redirect(reverse('login'))


@login_required
def email_validation(request):
    """
    This function is used to check the user email address to verify.
    """

    if not request.user.is_email_verified:
        return render(request, "accounts/email_validation.html", {"check_user": True})
    else:
        return redirect("/")


def verify_email(request, key):
    """
    This function will be use to verify the email of the user.
    """

    # Check user verify link is valid or not.
    if User.objects.filter(code=key).exists():
        user = User.objects.get(code=key)
        user.is_email_verified = True
        user.save()
        messages.success(request, "Your email has been verified successfully!")
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("/")

    messages.error(request, "This link is not valid. Please login, resend and verify your email again!")
    return redirect('login')


@login_required
def resend_email(request):
    """
    This function will use to resend the email for email verifaction.
    """

    # Generate uinque id for email verifaction link.
    request.user.code = uuid.uuid4().hex[:10]
    request.user.save()

    # Resend email verifaction link to the user.
    email_verify_request(request.user.email, request.user.get_email_verify_link())

    messages.success(request, "We have resent you an email, please verify your email address to complete registration")
    return redirect('email_validation')


def forgot_password(request):
    """
    This function will be use to send the link to user for creating a new password.
    """

    if request.method == 'POST':
        email = request.POST.get('email').lower()

        # Check email if exist or not.
        if not User.objects.filter(email__iexact=email).exists():
            messages.error(request, "This Email address Doesn't Exist, please enter valid email address.")
            return render(request, 'accounts/forgot_password.html')

        user = User.objects.get(email__iexact=email)
        PasswordRecover.objects.create(user=user)
        messages.success(request, "Please check your email for the reset password link.")
        request.session['password_reset_email'] = email
        return redirect('reset_link_sent')

    return render(request, 'accounts/forgot_password.html')


def reset_password(request):
    """
    This function will use to reset the password of the user.
    """

    if request.method == 'POST':

        # Check password recovery link is valid and save the new password.
        if PasswordRecover.objects.filter(code=request.GET.get('verify'), is_used=False).exists():
            recover = PasswordRecover.objects.get(code=request.GET.get('verify'))

            user = recover.user
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()

            # Update password recover code as used.
            recover.is_used = True
            recover.save()
            messages.success(request, "Your password is changed successfully, Please Login.")
            return redirect('login')
        else:
            messages.error(request, "Please resend reset password link and try again.")

    return render(request, 'accounts/reset_password.html')


def homepage(request):
    """
    This function will be used to update the information of the user.
    """

    products = Product.objects.all().order_by('-created')
    product_review = ProductReview.objects.all()
    brands = Brand.objects.all().order_by('-created')

    no_products = False

    if not products:
        no_products = True

    products_list = products.distinct()
    paginator = Paginator(products_list, 8)
    page = int(request.GET.get("page", 1))
    products = paginator.page(page)

    if request.is_ajax():
        data = render_to_string(
            'product/product_filter.html', {'products': products[:3]}, request=request)

        response = {
            'success': True,
            'data': data,
            'next_page': page + 1,
            'has_next': products.has_next(),
            'home': 'home',
            'product_review': product_review,
            'brands': brands[:2]
        }
        return HttpResponse(json.dumps(response))
    else:
        context = {
            'next_page': page + 1,
            'has_next': products.has_next(),
            'no_products': no_products,
            'products': products[:3],
            'media_url': settings.MEDIA_URL,
            'home': 'home',
            'product_review': product_review,
            'brands': brands[:2]
        }
        return render(request, 'home.html', context=context)


@login_required
def account(request):
    """
    This function will be used to update the information of the user.
    """

    user = request.user
    user_shops = Store.objects.filter(user=user)
    product_list = UserOrder.objects.filter(user=user, is_product_delivered=True).order_by('created')
    favourite_products = Product.objects.filter(favourite=request.user.id).order_by('id')

    products = dict()
    for i in product_list:
        month = i.created.strftime("%B %Y")
        if month not in products:
            products[month] = []
        products[month].append(i)

    form = UserInfoForm(instance=request.user)
    response = {
        "status": False,
        "errors": []
    }

    if request.method == 'POST' and request.POST.get('action') == 'add':
        address_form = AddressForm(data=request.POST)

        if address_form.is_valid():
            if request.POST.get('is_parent'):
                address = Address.objects.filter(user=user, is_parent=True)
                for add in address:
                    add.is_parent = False
                    add.save()
            address_form.save()

            response = {
                "status": True,
                "message": 'Address added successfully.'
            }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('action') == 'remove':
        address_id = request.POST.get('address_id')
        Address.objects.get(id=address_id).delete()

        response = {
            "status": True,
            "message": 'Address deleted successfully.'
        }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('action') == 'edit':
        address_obj = Address.objects.get(id=request.POST.get('address_id'))
        address_form = AddressForm(data=request.POST, instance=address_obj)

        if address_form.is_valid():
            if request.POST.get('is_parent'):
                address = Address.objects.filter(user=user, is_parent=True)
                for add in address:
                    add.is_parent = False
                    add.save()
            address_form.save()

            response = {
                "status": True,
                "message": 'Address change successfully.'
            }

        return HttpResponse(json.dumps(response))

    if request.method == 'POST':
        response = {
            "status": False,
            "errors": []
        }
        form = UserInfoForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            response = {
                "status": True,
                "message": 'Profile information has been saved successfully.'
            }

        return HttpResponse(json.dumps(response))

    active_tab = request.GET.get('tab')

    context = {
        'user': user,
        'media_url': settings.MEDIA_URL,
        # 'profile_tab': True,
        'form': form,
        'user_address': user.user_addresses.order_by('-created'),
        'user_shops': user_shops,
        'products': products,
        'favourite_products': favourite_products,
        'active_tab': active_tab if active_tab else 'info'
    }
    return render(request, 'accounts/profile.html', context=context)


@login_required
def get_address(request):
    if request.method == 'POST':
        obj_id = request.POST.get('address_id')
        address_obj = Address.objects.get(id=obj_id)
        response = {
            "status": True,
            "city": address_obj.city,
            "country": address_obj.country,
            "state": address_obj.state,
            "zip_code": address_obj.zip_code,
            "address_type": address_obj.address_type
        }

        return HttpResponse(json.dumps(response))


@login_required
def update_password(request):
    """
    Function is used for changing the password of the logged in user.
    """

    user = request.user
    response = {
        "status": False,
        "errors": []
    }
    if request.method == 'POST':
        update_password_form = UpdatePasswordForm(data=request.POST, user=request.user or None)

        # Check user old password is valid or not.
        if not user.check_password(request.POST.get('old_password')):
            response = {
                "status": False,
                "error": "Old password is Invalid."
            }

        elif update_password_form.is_valid():

            # It sets the new password of user's account.
            new_pass = update_password_form.cleaned_data['new_password']
            user.set_password(new_pass)

            user.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            response = {
                "status": True,
                "message": "Password has been changed successfully."
            }
        # messages.success(request, "Password has been changed successfully.")

        return HttpResponse(json.dumps(response))


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_service(request):
    return render(request, 'terms_service.html')


@login_required
def brand_signup(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get("profile_pic")
        user.profile_pic = image
        user.brand_name = request.POST.get('brand_name')
        user.save()

        brand_obj = Brand.objects.get(user=user)
        who_we_are_obj = WhoWeAre.objects.get(user=user)
        who_we_are_obj.brand.brand_name = request.POST.get('brand_name')
        who_we_are_obj.save()

        brand_obj.brand_name = request.POST.get('brand_name')
        brand_obj.save()

        if image:
            brand_obj.branc_pic = image
            brand_obj.save()

        # brand_category = BrandCategory.objects.get(brand=brand_obj)
        # BrandCategory.objects.create(
        #     brand=brand_obj
        # )

        # Category.objects.create(
        #     brand=brand_obj
        # )

        brand_style = BrandStyle.objects.get(brand=brand_obj)
        brand_style.brand=brand_obj
        brand_style.site_background='#ffffff'
        brand_style.main_color='#808080'
        brand_style.background_color_2nd='#EFEFEF'
        brand_style.top_nav_background='#ffffff'
        brand_style.save()
        
        # BrandStyle.objects.create(
        #     brand=brand_obj,
        #     site_background='#ffffff',
        #     main_color='#808080',
        #     background_color_2nd='#EFEFEF',
        #     top_nav_background='#ffffff'
        # )

        return redirect('email_validation')

    return render(request, 'accounts/brand_signup.html')


def reset_link_sent(request):
    """
        This function will be use to resend forget password mail.
        """
    if request.method == 'POST':
        email = request.session.get('password_reset_email')
        # Check email if exist or not.
        if not User.objects.filter(email__iexact=email).exists():
            messages.error(request, "This Email address Doesn't Exist, please enter valid email address.")
            return render(request, 'accounts/reset_link_sent.html')

        user = User.objects.get(email__iexact=email)
        PasswordRecover.objects.create(user=user)
        messages.success(request, "Please check your email for the reset password link.")
        return redirect('reset_link_sent')
    return render(request, 'accounts/reset_link_sent.html')


@csrf_exempt
def upload_image(request):
    myfile = request.FILES['images']
    user = request.user
    user.profile_pic = myfile
    user.save()
    filename = user.profile_pic
    uploaded_file_url = filename.name
    res = {"image_name": uploaded_file_url}
    return JsonResponse(res, safe=False)


@csrf_exempt
def upload_brand_image(request):
    myfile = request.FILES['images']
    user = request.user
    brand_obj = Brand.objects.get(user=user)
    brand_obj.branc_pic = myfile
    brand_obj.save()
    filename = brand_obj.branc_pic
    uploaded_file_url = filename.name
    res = {"image_name": uploaded_file_url}
    return JsonResponse(res, safe=False)


@csrf_exempt
def remove_image(request):
    user = request.user
    user.profile_pic = ''
    user.save()
    res = {}
    return JsonResponse(res, safe=False)


def store_list(request):
    """
    This function is used to show all the list of seller
    """

    user = request.user
    store_list = Store.objects.all().order_by('-created')
    store_state = Store.objects.values('shop_state').distinct()
    store_country = Store.objects.values('shop_country').distinct()
    store_city = Store.objects.values('shop_city').distinct()

    no_stores = False

    if not store_list:
        no_stores = True

    store_list = store_list.distinct()
    paginator = Paginator(store_list, 2)
    page = int(request.GET.get("page", 1))
    stores = paginator.page(page)

    if request.is_ajax():
        data = render_to_string(
            'store/store_card.html', {'stores': stores}, request=request)

        response = {
            'success': True,
            'data': data,
            'next_page': page + 1,
            'has_next': stores.has_next()
        }
        return HttpResponse(json.dumps(response))
    else:
        context = {
            'next_page': page + 1,
            'has_next': stores.has_next(),
            'no_stores': no_stores,
            'stores': stores,
            'store_state': store_state,
            'store_country': store_country,
            'store_city': store_city,
            'store_list': 'store_list'
        }
    return render(request, 'store/store_list.html', context)


@login_required
def add_store(request):
    """
    This function is used to add the store
    """

    user = request.user
    brand_obj = Brand.objects.get(user=user)
    store_form = StoreInfoForm()
    response = {
        "status": False,
        "errors": []
    }

    if request.method == 'POST' and request.POST.get('shop_action') == 'add':
        store_form = StoreInfoForm(request.POST, request.FILES)

        if store_form.is_valid():
            store_form = store_form.save(commit=False)
            store_form.user = user
            store_form.shop_brand = brand_obj
            store_form.save()

            response = {
                "status": True,
                "message": 'Shop added successfully.'
            }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('shop_action') == 'remove':
        shop_id = request.POST.get('store_id')
        Store.objects.get(id=shop_id).delete()

        response = {
            "status": True,
            "message": 'Shop deleted successfully.'
        }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('shop_action') == 'edit':
        store_form_obj = Store.objects.get(id=request.POST.get('store_id'))
        response = {
            "status": True,
            'shop_city': store_form_obj.shop_city,
            'shop_zip_code': store_form_obj.shop_zip_code,
            'shop_state': store_form_obj.shop_state,
            'shop_country': store_form_obj.shop_country,
            'shop_type': store_form_obj.shop_type,
            'shop_name': store_form_obj.shop_name,
            'shop_description': store_form_obj.shop_description
        }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('shop_action') == 'edit_save':
        store_form_obj = Store.objects.get(id=request.POST.get('store_id'))
        store_form = StoreInfoForm(data=request.POST, instance=store_form_obj)

        if store_form.is_valid():
            store_form.save()

            response = {
                "status": True,
                "message": 'Shop change successfully.'
            }

        return HttpResponse(json.dumps(response))

    context = {
        'store_form': store_form,
        'errors': store_form.errors,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def add_brand_store(request):
    """
    This function is used to add the store
    """

    user = request.user
    store_form = StoreInfoForm()
    response = {
        "status": False,
        "errors": []
    }

    if request.method == 'POST' and request.POST.get('brand_shop_action') == 'add':
        store_form = StoreInfoForm(request.POST)
        if store_form.is_valid():
            store_form = store_form.save(commit=False)
            store_form.user = user
            store_form.save()

            response = {
                "status": True,
                "message": 'Shop added successfully.'
            }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('shop_action') == 'remove':
        shop_id = request.POST.get('brand_store_id')
        Store.objects.get(id=shop_id).delete()

        response = {
            "status": True,
            "message": 'Shop deleted successfully.'
        }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('brand_shop_action') == 'edit':
        store_form_obj = Store.objects.get(id=request.POST.get('brand_store_id'))
        store_form = StoreInfoForm(data=request.POST, instance=store_form_obj)
        response = {
            "status": True,
            'brand_shop_city': store_form_obj.shop_city,
            'brand_shop_zip_code': store_form_obj.shop_zip_code,
            'brand_shop_state': store_form_obj.shop_state,
            'brand_shop_country': store_form_obj.shop_country,
            'brand_shop_type': store_form_obj.shop_type,
            'brand_shop_name': store_form_obj.shop_name
        }

        return HttpResponse(json.dumps(response))

    elif request.method == 'POST' and request.POST.get('brand_shop_action') == 'edit_save':
        store_form_obj = Store.objects.get(id=request.POST.get('brand_store_id'))
        store_form = StoreInfoForm(data=request.POST, instance=store_form_obj)

        if store_form.is_valid():
            store_form.save()

            response = {
                "status": True,
                "message": 'Shop change successfully.'
            }

        return HttpResponse(json.dumps(response))

    context = {
        'store_form': store_form,
        'errors': store_form.errors,
    }
    return render(request, 'accounts/profile.html', context)


def brand_list(request):
    """
    This function is used to show all the list of brand
    """

    user = request.user
    brands = Brand.objects.all().order_by('-created')
    brand_state = Brand.objects.values('brand_state').distinct()
    brand_country = Brand.objects.values('brand_country').distinct()
    brand_city = Brand.objects.values('brand_city').distinct()

    products = Product.objects.all().order_by('-created')

    no_brands = False

    if not brands:
        no_brands = True

    brand_list = brands.distinct()
    paginator = Paginator(brand_list, 2)
    page = int(request.GET.get("page", 1))
    brands = paginator.page(page)

    if request.is_ajax():
        data = render_to_string(
            'brand/brand_card.html', {'brands': brands, 'products': products}, request=request)

        response = {
            'success': True,
            'data': data,
            'next_page': page + 1,
            'has_next': brands.has_next()
        }
        return HttpResponse(json.dumps(response))
    else:
        context = {
            'next_page': page + 1,
            'has_next': brands.has_next(),
            'no_brands': no_brands,
            'brands': brands,
            'brand_state': brand_state,
            'brand_country': brand_country,
            'brand_city': brand_city,
            'products': products,
            'brand_list': 'brand_list'
        }
        return render(request, 'brand/brand_list.html', context)


def brand_detail(request, key):
    """
    This function is used to show the detail view of a brand
    """

    brand_obj = Brand.objects.get(id=key)
    brand_insight = BrandInsight.objects.get(brand=brand_obj)
    context = {
        'info_form': brand_obj,
        'brand_id': key,
        'brand_insight': brand_insight
    }
    return render(request, "brand/brand_detail.html", context)


def send_referral_alert(request):
    """
    This function is used to send emails to referral emails
    """

    if request.is_ajax():
        email = request.GET.get('referral', '')
        email = list(email.split(","))
        referral_request(email)
        response = {'status': True}
    return HttpResponse(json.dumps(response), content_type='application/json')


def categories(request):
    """
    This function is used render categories page
    """

    user = request.user
    product_review = ProductReview.objects.all()
    products = Product.objects.all().order_by('-created')
    context = {
        'categories': 'categories',
        'products': products,
        'product_review': product_review
    }
    return render(request, "categories.html", context)


@login_required
def brand_homepage(request, key):
    """
    This function is used render brand_homepage page
    """

    user = request.user
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    brandcat_form = BrandCategoryForm()
    cat_obj = None
    brandcat_obj = None
    product_list = Product.objects.filter(user=user)[:5]
    if BrandCategory.objects.filter(brand=brand_obj):
        brandcat_obj = BrandCategory.objects.get(brand=brand_obj)
        brandcat_form = BrandCategoryForm(instance=brandcat_obj)
        cat_obj = Category.objects.get(brand=brand_obj)

    if request.method == 'POST':
        brandcat_form = BrandCategoryForm(request.POST, request.FILES, instance=brandcat_obj)
        if brandcat_form.is_valid():
            brandcat_form.save()
            messages.success(request, 'Details edited Successfully!')
            return redirect('brand_detail_homepage', key=key)

    context = {
        'brand_obj': brand_obj,
        'edit': 'edit',
        'edit_item': 'edit_item',
        'product_detail': 'product_detail',
        'edit_mode': 'edit_mode',
        'brand_header1': 'brand_header1',
        'include_sale': 'include_sale',
        'product_list': product_list,
        'brandcat_obj': brandcat_obj,
        'brand_footer': 'brand_footer',
        'brandcat_obj': brandcat_obj,
        'brand_style': brand_style,
        'cat_obj': cat_obj,
        'brand_sidebar': 'brand_sidebar'
    }

    return render(request, "brand/brand_homepage.html", context)


def bussiness(request):
    """
    This function is used to show the detail view of a Product
    """

    context = {
        'bussiness': 'bussiness'
    }
    return render(request, "accounts/myprofile/bussiness.html", context)


def brand_filter(request):
    """
    This function is used to filter out the brands
    """

    if request.is_ajax():
        brands = Brand.objects.all().order_by('-created')
        brand_name = request.GET.get('brand_name', '')
        brand_address = request.GET.get('brand_address', '')
        brand_country = request.GET.get('brand_country', '')
        brand_state = request.GET.get('brand_state', '')
        brand_city = request.GET.get('brand_city', '')
        sort = request.GET.get('sort', '')

        if sort == 'low_rating':
            brands = brands.order_by('rating')

        if sort == 'high_rating':
            brands = brands.order_by('-rating')

        if brand_name:
            brands = brands.filter(brand_name__icontains=brand_name)

        if brand_address:
            brands = brands.filter(brand_address=brand_address)

        if brand_country:
            brands = brands.filter(brand_country__iexact=brand_country)

        if brand_state:
            brands = brands.filter(brand_state__iexact=brand_state)

        if brand_city:
            brands = brands.filter(brand_city__iexact=brand_city)

        brand_list = brands.distinct()
        paginator = Paginator(brand_list, 2)
        page = int(request.GET.get("page", 1))
        brands = paginator.page(page)

        products = Product.objects.all().order_by('-created')


        context = render_to_string('brand/brand_card.html', {
            'brands': brands, 'products': products,

        }, request=request)

        response = {
            'context': context,
            'success': True,
            'next_page': page + 1,
            'has_next': brands.has_next()
        }
        return HttpResponse(json.dumps(response), content_type="application/json")


def store_filter(request):
    """
    This function is used to filter out the stores
    """

    if request.is_ajax():
        stores = Store.objects.all().order_by('-created')

        store_name = request.GET.get('store_name', '')
        store_address = request.GET.get('store_address', '')
        store_country = request.GET.get('store_country', '')
        store_state = request.GET.get('store_state', '')
        store_city = request.GET.get('store_city', '')

        sort = request.GET.get('sort', '')

        if sort == 'low_rating':
            stores = stores.order_by('rating')

        if sort == 'high_rating':
            stores = stores.order_by('-rating')

        if store_name:
            stores = stores.filter(shop_name__icontains=store_name)

        if store_address:
            stores = stores.filter(shop_address=store_address)

        if store_country:
            stores = stores.filter(shop_country__iexact=store_country)

        if store_state:
            stores = stores.filter(shop_state__iexact=store_state)

        if store_city:
            stores = stores.filter(shop_city__iexact=store_city)

        store_list = stores.distinct()
        paginator = Paginator(store_list, 2)
        page = int(request.GET.get("page", 1))
        stores = paginator.page(page)

        context = render_to_string('store/store_card.html', {
            'stores': stores,
        }, request=request)

        response = {
            'context': context,
            'success': True,
            'next_page': page + 1,
            'has_next': stores.has_next()
        }
        return HttpResponse(json.dumps(response), content_type="application/json")


def follow_brand(request):
    user = request.user
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
        brand_obj = Brand.objects.get(id=brand_id)

        if user in brand_obj.follower_count.all():
            brand_obj.follower_count.remove(user)
        else:
            brand_obj.follower_count.add(user)

        follower_count, created = BrandFollow.objects.get_or_create(user=user, brand_id=brand_id)

        if created:
            if follower_count.value == 'UNFOLLOW':
                follower_count.value == 'FOLLOW'
            else:
                follower_count.value == 'UNFOLLOW'

    return redirect('brand_list')


def follow_store(request):
    user = request.user
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        store_obj = Store.objects.get(id=store_id)

        if user in store_obj.store_follower.all():
            store_obj.store_follower.remove(user)
        else:
            store_obj.store_follower.add(user)

        store_follower, created = StoreFollow.objects.get_or_create(user=user, store_id=store_id)

        if created:
            if store_follower.value == 'UNFOLLOW':
                store_follower.value == 'FOLLOW'
            else:
                store_follower.value == 'UNFOLLOW'

    return redirect('store_list')


def brand_category(request, key):
    user = request.user
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    product_review = ProductReview.objects.all()
    product_list = Product.objects.filter(user=user)[:5]
    who_we_are_obj = WhoWeAre.objects.get(brand=brand_obj)
    products = Product.objects.all().order_by('-created')[:4]
    cat_obj = Category.objects.get(brand=brand_obj)
    cat_form = CategoryForm(instance=cat_obj)

    if request.method == 'POST':
        cat_form = CategoryForm(request.POST, request.FILES, instance=cat_obj)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, 'Details edited Successfully!')
            return redirect('brand_detail_homepage', key=key)

    context = {
        'brand_obj': brand_obj,
        'categories': 'categories',
        'products': products,
        'edit': 'edit',
        'product_detail': 'product_detail',
        'edit_mode_category': 'edit_mode_category',
        'product_review': product_review,
        'brand_header1': 'brand_header1',
        'product_list': product_list,
        'who_we_are_obj': who_we_are_obj,
        'brand_footer': 'brand_footer',
        'cat_obj': cat_obj,
        'brand_style': brand_style,
        'category_sidebar': 'category_sidebar'
    }
    return render(request, "brand_category.html", context)


def brand_sale(request, key):
    user = request.user
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    products = Product.objects.filter(user=user)
    product_list = Product.objects.filter(user=user)[:5]
    who_we_are_obj = WhoWeAre.objects.get(brand=brand_obj)
    cat_obj = Category.objects.get(brand=brand_obj)

    context = {
        'brand_obj': brand_obj,
        'edit': 'edit',
        'product_detail': 'product_detail',
        'product_list': product_list,
        'edit_mode_sale': 'edit_mode_sale',
        'sales': 'sales',
        'brand_header1': 'brand_header1',
        'products': products,
        'who_we_are_obj': who_we_are_obj,
        'brand_footer': 'brand_footer',
        'brand_style': brand_style,
        'cat_obj': cat_obj,
        'sale_sidebar': 'sale_sidebar'
    }
    return render(request, "brand_sale.html", context)


def who_we_are(request, key):
    user = request.user
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    who_we_are_obj = WhoWeAre.objects.get(brand=brand_obj)
    who_we_are_form = WhoWeAreForm(instance=who_we_are_obj)
    product_list = Product.objects.filter(user=user)[:5]
    cat_obj = Category.objects.get(brand=brand_obj)

    if request.method == 'POST':
        who_we_are_form = WhoWeAreForm(request.POST, request.FILES, instance=who_we_are_obj)
        if who_we_are_form.is_valid():
            who_we_are_form.save()
            messages.success(request, 'Details edited Successfully!')
            return redirect('brand_who_we_are', key=key)

    context = {
        'brand_obj': brand_obj,
        'edit': 'edit',
        'edit_item': 'edit_item',
        'product_detail': 'product_detail',
        'edit_mode_who': 'edit_mode_who',
        'who': 'who',
        'brand_header1': 'brand_header1',
        'product_list': product_list,
        'who_we_are_obj': who_we_are_obj,
        'brand_footer': 'brand_footer',
        'brand_style': brand_style,
        'cat_obj': cat_obj,
        'who_sidebar': 'who_sidebar'
    }

    return render(request, "who_we_are.html", context)


def brand_detail_homepage(request, key):
    context = {}
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    if request.user.is_authenticated:
        user = request.user
        if user == brand_obj.user:
            if not user.is_email_verified:
                return redirect('email_validation')

    brand_obj.visit = brand_obj.visit + 1
    brand_obj.save()
    if BrandCategory.objects.filter(brand=brand_obj).exists():
        category_obj = BrandCategory.objects.get(brand=brand_obj)
    else:
        category_obj = {}

    products = Product.objects.all().order_by('-created')[:3]
    product_review = ProductReview.objects.all()
    context = {
        'brand_header_detail': 'brand_header_detail',
        'brand_obj': brand_obj,
        'category_obj': category_obj,
        'products': products,
        'product_review': product_review,
        'include_sale': 'include_sale',
        'brand_style': brand_style,
        'more_width': 'more_width'
    }
    return render(request, "brand_detail/brand_detail_homepage.html", context)


def brand_detail_category(request, key):
    context = {}
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    product_review = ProductReview.objects.all()
    products = Product.objects.all().order_by('-created')

    cat_obj = Category.objects.get(brand=brand_obj)
    context = {
        'brand_obj': brand_obj,
        'products': products,
        'categories': 'categories',
        'product_review': product_review,
        'cat_obj': cat_obj,
        'brand_style': brand_style,
        'more_width': 'more_width'
    }
    return render(request, "brand_detail/brand_detail_category.html", context)


def brand_detail_sale(request, key):
    context = {}
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    product_list = Product.objects.filter(is_sale=True).order_by('-created')
    product_designer = Product.objects.values('product_designer').distinct()
    product_category = Product.objects.values('product_category').distinct()
    product_size = SizeType.SIZETYPE
    product_color = Product.objects.values('product_color').distinct()
    product_material = Product.objects.values('product_material').distinct()

    time_threshold = timezone.now() - timedelta(days=30)
    search = request.GET.get('value', '')

    if search == 'all':
        product_list = product_list

    if search == 'new':
        product_list = product_list.filter(created__lte=time_threshold)

    if search and search != 'all' and search != 'new':
        product_list = product_list.filter(product_sale_amount__lte=search)

    product_review = ProductReview.objects.all()

    product_list = product_list.distinct()
    paginator = Paginator(product_list, 12)
    page = int(request.GET.get("page", 1))
    products = paginator.page(page)

    context = {
        'brand_obj': brand_obj,
        'products': products,
        'next_page': page + 1,
        'has_next': products.has_next(),
        'sales': 'sales',
        'product_review': product_review,
        'brand_style': brand_style,
        'product_designer': product_designer,
        'product_category': product_category,
        'product_size': product_size,
        'product_material': product_material,
        'product_color': product_color
    }
    return render(request, "brand_detail/brand_detail_sale.html", context)


def brand_who_we_are(request, key):
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None
    who_we_are_obj = WhoWeAre.objects.get(brand=brand_obj)

    context = {
        'brand_obj': brand_obj,
        'who': 'who',
        'who_we_are_obj': who_we_are_obj,
        'brand_style': brand_style,
        'more_width': 'more_width'
    }
    return render(request, "brand_detail/brand_who_we_are.html", context)


def get_in_touch(request, key):
    """
    This function will render the get_in_touch page.
    """
    context = {}
    brand_obj = Brand.objects.get(id=key)
    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.get(brand=brand_obj)
    else:
        brand_style = None

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_value = request.POST.get('message', '')

        message = 'Dear Admin,\n You have received a query from {}, with email address {} for {}'.format(name, email,
                                                                                                         message_value)

        if name and email:
            contact_us([settings.DEFAULT_CONTACT_EMAIL], message, email, name)
            messages.success(request, 'Your form has been submitted successfully, you will be contacted shortly!')
            return redirect('brand_detail_homepage', key=key)

    return render(request, 'get_in_touch.html',
                  {'brand_obj': brand_obj, 'contact': 'contact', 'brand_style': brand_style})


def main_search(request):
    """
    This function will render the get_in_touch page.
    """

    product_list = Product.objects.all().order_by('-created').distinct()
    brand_list = Brand.objects.all().order_by('-created').distinct()
    shop_list = Store.objects.all().order_by('-created').distinct()

    if request.method == 'GET':
        main_search = request.GET.get('main_search', '')

        if main_search:
            product_list = product_list.filter(product_name__icontains=main_search)
            brand_list = brand_list.filter(brand_name__icontains=main_search)
            shop_list = shop_list.filter(shop_name__icontains=main_search)

        combined_list = list(chain(product_list, brand_list, shop_list))

        # combined_list = list(set(combined_list))
        paginator = Paginator(combined_list, 12)
        page = int(request.GET.get("page", 1))
        combined_data = paginator.page(page)

        if request.is_ajax():
            data = render_to_string('global_search_card.html', {'combined_data': combined_data}, request=request)

            response = {
                'success': True,
                'data': data,
                'next_page': page + 1,
                'has_next': combined_data.has_next()
            }
            return HttpResponse(json.dumps(response))
        else:
            context = {
                'next_page': page + 1,
                'has_next': combined_data.has_next(),
                'combined_data': combined_data
            }

    return render(request, 'filtered_data.html', context)


def get_sub_info(request):
    """
    ajax call for state, city
    """
    obj_id = request.GET.get('obj_id')
    sc_type = request.GET.get('type')  # State, City, District
    rndr_str = '<option value="">-Select-</option>'
    if sc_type == 'state':
        objects = State.objects.filter(country__name=obj_id)
    elif sc_type == 'city':
        objects = City.objects.filter(state__name=obj_id, district__isnull=True)

    for sc in objects:
        rndr_str += '<option value="{}">{}</option>'.format(sc.name, sc.name)
    return HttpResponse(rndr_str)


@csrf_exempt
def brand_style(request):
    user = request.user
    brand_obj = Brand.objects.get(user=user)
    site_background = request.GET.get('site_background', '')
    main_color = request.GET.get('main_color', '')
    texts_color = request.GET.get('texts_color', '')
    top_nav_text = request.GET.get('top_nav_text', '')
    top_nav_background = request.GET.get('top_nav_background', '')
    background_color_2nd = request.GET.get('background_color_2nd', '')

    if request.method == 'GET':
        if not BrandStyle.objects.filter(brand=brand_obj):
            obj = BrandStyle.objects.create(brand=brand_obj)
        else:
            obj = BrandStyle.objects.get(brand=brand_obj)
        if obj:
            if site_background:
                obj.site_background = site_background

            if main_color:
                obj.main_color = main_color

            if texts_color:
                obj.texts_color = texts_color

            if site_background:
                obj.site_background = site_background

            if top_nav_background:
                obj.top_nav_background = top_nav_background

            if background_color_2nd:
                obj.background_color_2nd = background_color_2nd
            obj.save()

    response = {
        "status": True,
        "message": 'Address added successfully.'
    }

    return HttpResponse(json.dumps(response))


def contact_us_view(request):
    """
    This function will render the get_in_touch page.
    """
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message_value = request.POST.get('message', '')

        message = 'Dear Admin,\n You have received a query from {}, with email address {} for {}'.format(name, email, message_value)
        message_user = 'Your form has been submitted successfully, you will be contacted shortly!'
        if name and email:
            contact_us([settings.DEFAULT_CONTACT_EMAIL], message, email, name)
            contact_us([email], message_user, settings.DEFAULT_CONTACT_EMAIL, name)
            messages.success(request, 'Your form has been submitted successfully, you will be contacted shortly!')
            return redirect('homepage')

    return render(request, 'contact_us.html', {'contact': 'contact'})

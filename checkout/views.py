import json
import random
import string
import ast
import stripe

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse

from accounts.models import User, Address
from checkout.forms import BillingAddressForm, CheckoutSignUpForm
from checkout.models import CartProduct, UserOrder, Checkout
from product.models import Product, ProductReview

from accounts.forms import (
    SignUpForm, LoginForm
)

stripe.api_key = settings.STRIPE_KEYS['API_KEY']


def checkout(request, key):
    user_addresses = None

    if request.user.is_authenticated:
        user_addresses = request.user.user_addresses.order_by('-created')

    product_obj = CartProduct.objects.get(bag_product=key)
    context = {
    'product_obj': product_obj,
    "STRIPE_PUBLISH_KEY": settings.STRIPE_PUBLISH_KEY,
    'user_address': user_addresses,
    'user_addres_count': len(user_addresses),
    'delevery': 'delevery'
    }
    return render(request, 'checkout.html', context)


def add_to_bag(request, key):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.get(id=3)
    response = {'status': False}
    if request.is_ajax():
        product_obj = Product.objects.get(id=key)
        CartProduct.objects.get_or_create(
            user = user,
            bag_product = product_obj,
            is_bag = True,
            size=request.GET.get('size'),
            quantity=request.GET.get('quantity'),
            total_price=product_obj.product_price * int(request.GET.get('quantity')),
            total_payable=(product_obj.product_price * int(request.GET.get('quantity')))+5
        )
        response = {'status': True}
    return HttpResponse(json.dumps(response), content_type='application/json')



def billing_address(request, key):

    user = request.user
    product_obj = CartProduct.objects.get(id=key)
    billing_form = BillingAddressForm()

    if request.method == 'POST':
        billing_form = BillingAddressForm(data=request.POST)

        if billing_form.is_valid():
            obj = billing_form.save(commit=False)
            obj.user = user
            obj.billing_product = product_obj.bag_product
            obj.address = Address.objects.filter(user=user).first()
            obj.save()

            # return redirect('checkout', key)

    context = {
        'product_obj': product_obj,
        'billing_form': billing_form,
        'billing': 'billing',
        "STRIPE_PUBLISH_KEY": settings.STRIPE_PUBLISH_KEY,
    }
    return render(request, 'checkout.html', context)


def checkout_signup(request, key):
    """
    This function is used to register the user.
    """

    if request.user.is_authenticated:
        return redirect("/")

    product_obj = Product.objects.get(id=key)

    if request.method == "POST":
        form = CheckoutSignUpForm(request.POST)
        # Create new user and login.
        if form.is_valid():
            user_obj = User.objects.create(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email']
            )
            letters = string.ascii_lowercase
            password = ''.join(random.choice(letters) for i in range(8))

            user_obj.set_password(password)
            user_obj.save()
            bag_products = CartProduct.objects.filter(user=3)
            for prod in bag_products:
                prod.user = user_obj
                prod.save()

            login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')

            return redirect("checkout", key)

        return render(request, 'checkout.html', {'form': form, 'product_obj':product_obj})
    else:
        form = CheckoutSignUpForm()
    return render(request, 'checkout.html', {'form': form, 'product_obj':product_obj})


def checkout_login_user(request, key):
    """
    Function is used to login the user.
    """

    if request.user.is_authenticated:
        return redirect("/")

    product_obj = Product.objects.get(id=key)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if user is not None:
                auth_login(request, user)
                messages.success(request, "You are logged in successfully!")

                bag_products = CartProduct.objects.filter(user=3)
                print(bag_products)
                for prod in bag_products:
                    prod.user = user
                    prod.save()
                return redirect("checkout", key)
            else:
                form.add_error('email', 'Email or Password is wrong')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'product_obj': product_obj
    }
    return render(request, 'checkout.html', context=context)


def cart(request):

    product_review = ProductReview.objects.all()

    if request.user.is_authenticated:
        user = request.user
    else:
        messages.error(request, "Please login first!!")
        return redirect('login')

    products = Product.objects.all().order_by('-created')[:3]

    product_obj = CartProduct.objects.filter(user=user, is_bag=True)

    context = {
        'product_review': product_review,
        'products': products,
        'product_obj': product_obj
    }
    return render(request, 'cart.html', context)


def bill_pay(request):
    card = request.POST.get('stripeToken')
    product_id = request.GET.get('product_id')

    cart_product = CartProduct.objects.get(id=product_id)
    if card != '':
        total_amount = cart_product.total_payable
        try:
            charge = stripe.Charge.create(
                amount=int(total_amount*100),
                currency="usd",
                source=card,
                description="product order"
            )

            result = charge.id
            purchase = Checkout.objects.create(user= request.user,
                                                   product=cart_product.bag_product,
                                                   amount=total_amount,
                                                   transaction_token=charge.id)
            UserOrder.objects.get_or_create(
                user=request.user,
                product=cart_product.bag_product,
                is_product_delivered=True
            )
            a = ast.literal_eval(cart_product.bag_product.remaining_size_and_quantity)
            b = a[cart_product.size]
            c = int(a[cart_product.size]) - cart_product.quantity
            a.update({cart_product.size: c})

            cart_product.bag_product.remaining_size_and_quantity = a
            cart_product.bag_product.save()
            cart_product.delete()

            print('~~~~~~~~~~~~~ purchased by stripe ~~~~~~~~~~~~~~~')

        except Exception as e:
            print(e, '@@@@@ Error in contract_add()')

    context = {
        'product_obj': cart_product,
        'confirmation': 'confirmation',
    }
    return render(request, 'checkout.html', context)


def remove_cart(request, key):
    cart_product = CartProduct.objects.get(id=key)
    cart_product.delete()
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.get(id=1)

    products = Product.objects.all().order_by('-created')[:3]

    product_obj = CartProduct.objects.filter(user=user, is_bag=True)

    context = {
        'products': products,
        'product_obj': product_obj
    }
    return render(request, 'cart.html', context)

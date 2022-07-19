import json
import datetime
from datetime import timedelta
from django.utils import timezone
import stripe
import ast

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage

from accounts.models import User, Brand, BrandStyle, BrandCategory, Category
from product.forms import AddProductForm, ProductReviewForm, ProductImageForm
from product.models import Product, ProductReview, ProductImage

from shared.constants import SizeType

stripe.api_key = settings.STRIPE_KEYS['API_KEY']


def product_list(request):
    """
    This function is used to show all the list of product
    """
    user = request.user
    product_list = Product.objects.all().order_by('-created')
    product_designer = Product.objects.values('product_designer').distinct()
    product_category = Product.objects.values('product_category').distinct()
    product_size = SizeType.SIZETYPE
    product_color = Product.objects.values('product_color').distinct()
    product_material = Product.objects.values('product_material').distinct()
    sort_by = request.GET.get('order_by', 'low_price').strip()
    flag = request.GET.get('flag', 'ALL')
    category = request.GET.getlist('catagory[]')
    design = request.GET.getlist('design[]')
    size = request.GET.getlist('size[]')
    color = request.GET.getlist('color[]')
    material = request.GET.getlist('material[]')
    product_min_price = request.GET.get('product_min_price', '')
    product_max_price = request.GET.get('product_max_price', '')


    no_products = False

    if not product_list:
        no_products = True

    time_threshold = timezone.now() - timedelta(days=30)

    if flag == 'WOMEN':
        # product_list = product_list.filter(product_for__iexact=flag)
        product_list = product_list

    if flag == 'MEN':
        # product_list = product_list.filter(product_for__iexact=flag)
        product_list = product_list

    if flag == 'All':
        # product_list = product_list
        product_list = product_list

    if flag == 'NEW':
        product_list = product_list.filter(created__gte=time_threshold)

    if flag != 'ALL' and flag != 'NEW' and flag != 'MEN' and flag != 'WOMEN'and flag is not None:
        product_list = product_list.filter(product_category__iexact=flag)

    if sort_by == 'low_price':
        product_list = product_list.order_by("product_price")
    elif sort_by == 'high_price':
        product_list = product_list.order_by("-product_price")
    # elif sort_by == 'low_rating':

    #     product_list = product_list.order_by('low_rating')
    # elif sort_by == 'hight_rating':
    #     product_list = product_list.order_by('hight_rating')

    product_review = ProductReview.objects.all()
    product_list = product_list.distinct()
    if category:
        product_list = product_list.filter(product_category__in=category)

    if design:
        product_list = product_list.filter(product_designer__in=design)

    if size:
        product_list = product_list.filter(product_size__contained_by=size)

    if color:
        product_list = product_list.filter(product_color__contained_by=color)

    if material:
        product_list = product_list.filter(product_material__in=material)

    if product_min_price and product_max_price:
        product_list = product_list.filter(product_price__gte=product_min_price, product_price__lte=product_max_price)

    # paginator = Paginator(product_list, 12)
    page = int(request.GET.get("page", 1))

    paginator = Paginator(product_list, 4)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.is_ajax():
        context = {
            'products': products,
            'has_next': products.has_next()
        }
        data = render_to_string(
            'product_filter.html', context, request=request)

        response = {
            'success': True,
            'data': data,
            # 'next_page': page+1,
            # 'has_next': products.has_next()
        }
        return HttpResponse(json.dumps(response))
    else:

        context = {
            'products': products,
            'product_designer': product_designer,
            'product_material': product_material,
            'product_color': product_color,
            'product_size': product_size,
            'product_category': product_category,
            'next_page': page+1,
            'has_next': products.has_next(),
            'no_products': no_products,
            'flag': flag,
            'product_review': product_review,
            'page': page
        }
    return render(request, "product_list.html", context=context)


def products_filter(request):
    """
    This function is used to filter out the products based on different criteriaa
    """

    if request.is_ajax():
        products = Product.objects.all().order_by('-created')

        product_category = request.GET.get('product_category', '')
        product_size = request.GET.get('product_size', '')
        product_designer = request.GET.get('product_designer', '')
        product_color = request.GET.get('product_color', '')
        product_min_price = request.GET.get('product_min_price', '')
        product_max_price = request.GET.get('product_max_price', '')
        product_material = request.GET.get('product_material', '')
        product_review = ProductReview.objects.all()

        sort = request.GET.get('sort', '')

        if product_category:
            products = products.filter(product_category=product_category)

        if product_size:
            products = products.filter(product_size=product_size)

        if product_designer:
            products = products.filter(product_designer=product_designer)

        if product_color:
            products = products.filter(product_color=product_color)

        if product_min_price and product_max_price:
            products = products.filter(product_price__gte=product_min_price, product_price__lte=product_max_price)

        if product_material:
            products = products.filter(product_material=product_material)

        if sort == 'low_price':
            products = products.order_by('product_price')

        if sort == 'high_price':
            products = products.order_by('-product_price')

        if sort == 'low_rating':
            products = ProductReview.objects.all().order_by('rating')

        if sort == 'hight_rating':
            products = ProductReview.objects.all().order_by('-rating')

        product_list = products.distinct()
        paginator = Paginator(product_list, 25)
        page = int(request.GET.get("page", 1))
        products = paginator.page(page)

        context = render_to_string('product_filter.html', {
            'products': products,
            'product_review': product_review
        }, request=request)

        response = {
            'context': context,
            'success': True,
            # 'next_page': page+1,
            # 'has_next': products.has_next()
        }
        # return HttpResponse(json.dumps(response), content_type="application/json")
        return JsonResponse(response)

def favourite(request):
    user = request.user
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_obj = Product.objects.get(id=product_id)

        if user in product_obj.favourite.all():
            product_obj.favourite.remove(user)
        else:
            product_obj.favourite.add(user)

    return redirect('product_list')


@login_required
def add_product(request, key):
    """
    This function is used to add the product
    """
    user = request.user
    brand_obj = Brand.objects.get(user=user)
    product_form = AddProductForm()
    brand = Brand.objects.get(id=key)

    if BrandStyle.objects.filter(brand=brand).exists():
        brand_style = BrandStyle.objects.get(brand=brand)
    else:
        brand_style = None

    if request.method == "POST":
        product_pic = request.FILES.get("product_pic")
        product_form = AddProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            obj = product_form.save(commit=False)
            obj.user = user
            obj.brand = brand
            obj.is_sale = True
            obj.product_pic = product_pic
            obj.product_size = request.POST.getlist('product_size')
            obj.product_quantity = request.POST.getlist('product_quantity[]')
            obj.remaining_size_and_quantity = dict(zip(request.POST.getlist('product_size'), request.POST.getlist('added_product_quantity')))
            obj.product_color = request.POST.getlist('product_color[]')
            obj.product_size_and_quantity = dict(zip(request.POST.getlist('product_size'), request.POST.getlist('added_product_quantity')))

            res = {request.POST.getlist('product_size')[i]: request.POST.getlist('added_product_quantity')[i] for i in range(len(request.POST.getlist('product_size')))}

            obj.save()

            file_list = request.POST.getlist('uploded_id[]')[:-1]

            # create objects for new images
            for img in file_list:
                ProductImage.objects.create(product=obj, name=img, p_image=img)

            messages.success(request, "Product added successfully!")
            return redirect('brand_detail_sale', key)
        else:
            product_form = AddProductForm()

    context = {
        'product_form': product_form,
        'errors': product_form.errors,
        'brand_obj': brand_obj,
        'edit': 'edit',
        'product_detail': 'product_detail',
        'add_product': 'add_product',
        'edit_mode_product': 'edit_mode_product',
        'brand_header1': 'brand_header1',
        'brand_style': brand_style,
        'product_sidebar': 'product_sidebar',
        'errors': product_form.errors
    }
    return render(request, 'product_profile.html', context)


def product_detail(request, key):
    product_obj = Product.objects.get(id=key)
    brand_obj = product_obj.brand

    if BrandStyle.objects.filter(brand=brand_obj).exists():
        brand_style = BrandStyle.objects.filter(brand=brand_obj)
    else:
        brand_style = None

    if ProductImage.objects.filter(product=key).exists():
        img_obj = ProductImage.objects.filter(product=key)
    else:
        img_obj = {}

    if product_obj.remaining_size_and_quantity:
        remaining_size_and_quantity = ast.literal_eval(product_obj.remaining_size_and_quantity)
    else:
        remaining_size_and_quantity = None

    context = {
        'product_detail': 'product_detail',
        'product_obj': product_obj,
        'img_obj': img_obj,
        'brand_obj': brand_obj,
        'brand_style': brand_style,
        'remaining_size_and_quantity': remaining_size_and_quantity,
        'range': zip(img_obj, ['1', '2', '3', '4'])
    }
    return render(request, "brand_product_detail.html", context)


@csrf_exempt
def product_img(request):
    myfile = request.FILES['images']
    file_id = request.POST['uid']
    fs = FileSystemStorage()
    extension = myfile.name.split('.')
    filename = fs.save(datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")+myfile.name.rsplit('.', 1)[0].replace(" ", "_")[0:50]+'.'+extension[-1].lower(), myfile)
    uploaded_file_url = fs.url(filename)
    res = {"status":True, "image_url": uploaded_file_url,"image_name": uploaded_file_url.split('/')[-1], 'uid':file_id}
    return JsonResponse(res, safe=False)


@csrf_exempt
def productimage_delete(request):
    image_name = request.POST.get('image_name')
    product = request.POST.get('product')

    a = ProductImage.objects.filter(name=image_name)
    for i in a:
        print(i)
        i.delete()

    if not ProductImage.objects.filter(name=image_name):
        try:
            delete_file(image_name)
        except Exception:
            pass
    return HttpResponse('')


@login_required
def edit_product(request, key):

    product_obj = Product.objects.get(id=key)
    product_form = AddProductForm(instance=product_obj)
    product_img = ProductImage.objects.filter(product=product_obj)
    user = request.user
    brand_obj = Brand.objects.get(user=user)
    brandcat_obj = BrandCategory.objects.get(brand=brand_obj)
    cat_obj = Category.objects.get(brand=brand_obj)
    brand_style = BrandStyle.objects.get(brand=brand_obj)

    if request.method == 'POST':
        if request.FILES.get("product_pic"):
            product_pic = request.FILES.get("product_pic")
        else:
            product_pic = product_obj.product_pic

        product_form = AddProductForm(request.POST, request.FILES, instance=product_obj)
        if product_form.is_valid():
            obj = product_form.save(commit=False)
            obj.user = user
            obj.brand = brand_obj
            obj.is_sale = True
            obj.product_pic = product_pic
            obj.product_size = request.POST.getlist('product_size')
            obj.product_quantity = request.POST.getlist('product_quantity[]')
            obj.product_color = request.POST.getlist('product_color[]')
            obj.remaining_size_and_quantity = dict(zip(request.POST.getlist('product_size'), request.POST.getlist('added_product_quantity')))
            obj.product_size_and_quantity = dict(zip(request.POST.getlist('product_size'), request.POST.getlist('added_product_quantity')))
            obj.save()

            file_list = request.POST.getlist('uploded_id[]')
            print(file_list, 'l')
            file_list = [i for i in file_list if i]

            # create objects for new images
            for img in file_list:
                if not ProductImage.objects.filter(product=obj, name=img, p_image=img).exists():
                    print('kjhjjgh')
                    ProductImage.objects.create(product=obj, name=img, p_image=img)

            messages.success(request, 'Product details edited Successfully!')
            return redirect("product_detail", key=key)

    context = {
        'product_form': product_form,
        'brand_obj': brand_obj,
        'edit_item': 'edit_item',
        'brand_header1': 'brand_header1',
        'add_product': 'add_product',
        'product_img': product_img,
        'brandcat_obj': brandcat_obj,
        'cat_obj': cat_obj,
        'brand_style': brand_style,
        'edit_mode_product': 'edit_mode_product',
        'product_sidebar': 'product_sidebar',
        'product_img': product_img
    }

    return render(request, 'product_profile.html', context=context)

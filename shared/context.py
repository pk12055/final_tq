from django.conf import settings

from accounts.models import Brand, Country, WhoWeAre, BrandCategory


def base_context(request):
    """
    This function will return site_url and default image
    """

    brand = None
    who_we_are_obj = None

    if request.user.is_authenticated:
        user = request.user
        if user and user.user_type == 'Brand':
            if Brand.objects.filter(user=user):
                brand = Brand.objects.get(user=user)
                who_we_are_obj = WhoWeAre.objects.get(brand=brand)

    return {
	    'default_image': '/static/images/default.png',
        'brand_header_id': brand,
        'countries': Country.objects.all(),
        'who_we_are_obj': who_we_are_obj
    }


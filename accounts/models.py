import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.contrib.postgres.fields import ArrayField

from shared.models import BaseTimeStampModel
from shared.managers import UserManager
from shared.constants import (
    UserType, AddressType, StoreType, SizeType, Followchoice, WHO_WE_ARE_PARA_1,
    WHO_WE_ARE_PARA_2, WHO_WE_ARE_PARA_3, SHOP_DESCRIPTION
)

from shared.mailing import email_verify_request, password_reset_request


class User(AbstractUser, BaseTimeStampModel):
    """
    This model stores the information of an user.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    user_type = models.CharField(max_length=255, choices=UserType.USERTYPE)
    dob = models.DateField(null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_email_verify_link(self):
        return '{}/verify/email/{}'.format(settings.BASE_URL, self.code)

    def save(self, *args, **kwargs):
        if self.pk and self.user_type == "Brand":
            if not Brand.objects.filter(user=self):
                brand_obj = Brand.objects.create(
                    user=self
                )
                WhoWeAre.objects.create(
                    user=self,
                    brand=brand_obj
                )
                # BrandCategory.objects.create(brand=brand_obj)
                # BrandStyle.objects.create(brand=brand_obj)
                # Category.objects.create(brand=brand_obj)
        super().save(*args, **kwargs)


class PasswordRecover(BaseTimeStampModel):
    """
    This model is used to store the password recovery link with an expiration date time.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='password_recover')
    code = models.CharField(max_length=64)
    is_used = models.BooleanField(default=False)
    expiration = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Password Recovery'
        verbose_name_plural = 'Password Recoveries'

    def __str__(self):
        return self.user.email

    @staticmethod
    def get_expiration():
        return timezone.now() + timezone.timedelta(hours=12)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.expiration = PasswordRecover.get_expiration()
            PasswordRecover.objects.filter(user=self.user).delete()

            self.code = get_random_string()
            super().save(*args, **kwargs)
            password_reset_request(self.user.email, self.get_recovery_link())
        elif self.is_used is True:
            self.delete()
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.expiration > timezone.now() and not self.is_used

    def get_recovery_link(self):
        return '{}/reset-password?verify={}'.format(settings.BASE_URL, self.code)


class Address(BaseTimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    address = models.TextField()
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=255, choices=AddressType.ADDRESSTYPE, default=AddressType.home)
    is_parent = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


def create_user_metadata(sender, instance, created, **kwargs):
    if created:
        if instance.email:

            # Generate uinque id.
            instance.code = uuid.uuid4().hex[:10]
            instance.save()
            email_verify_request(instance.email, instance.get_email_verify_link())

        # Set username.
        if not instance.username:
            instance.username = instance.email
            instance.save()


class Brand(BaseTimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_brands')
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    branc_pic = models.ImageField(null=True, blank=True)
    brand_address = models.TextField(null=True, blank=True)
    brand_country = models.CharField(max_length=255, null=True, blank=True)
    brand_state = models.CharField(max_length=255, null=True, blank=True)
    brand_city = models.CharField(max_length=255, null=True, blank=True)
    brand_zip_code = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    visit = models.IntegerField(null=True, blank=True, default=0)
    follower_count = models.ManyToManyField(User, default=None, blank=True, related_name='brand_follower')
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.brand_name)

    @property
    def num_follower(self):
        return self.follower_count.all().count()


class Store(BaseTimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_shops')
    shop_brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='shop_brand', null=True)
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    last_edited = models.DateTimeField(null=True, blank=True)
    shop_type = models.CharField(max_length=255, choices=StoreType.STORETYPE)
    shop_description = models.TextField(null=True, blank=True, default=SHOP_DESCRIPTION)
    shop_address = models.TextField(null=True, blank=True)
    shop_country = models.CharField(max_length=255, null=True, blank=True)
    shop_state = models.CharField(max_length=255, null=True, blank=True)
    shop_city = models.CharField(max_length=255, null=True, blank=True)
    shop_zip_code = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    store_follower = models.ManyToManyField(User, default=None, blank=True, related_name='store_followers')
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.shop_name)

    @property
    def num_follower(self):
        return self.store_follower.all().count()


class StoreImage(BaseTimeStampModel):
    store = models.ForeignKey(Store, related_name='store_images', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='media/', null=True, verbose_name="")
    order_img = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.store.shop_name, self.name)

    @property
    def extension(self):
        types = ["png", "gif", "jpg", "jpeg"]
        image_file = True
        if self.file:
            extension = self.file.url.split('.')
            if not extension[-1].lower() in types:
                image_file = False
        return image_file


class BrandFollow(BaseTimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='follower_brand')
    value = models.CharField(max_length=20, default='UNFOLLOW', choices=Followchoice.FOLLOWCHOICE)

    def __str__(self):
        return self.brand


class StoreFollow(BaseTimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_follower_user')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='follower_store')
    value = models.CharField(max_length=20, default='UNFOLLOW', choices=Followchoice.FOLLOWCHOICE)

    def __str__(self):
        return str(self.store)


class BrandInsight(BaseTimeStampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_insight')
    follower_count = models.IntegerField(default=0)
    total_items_count = models.IntegerField(default=0)
    items_sold_count = models.IntegerField(default=0)
    monthly_earning = models.IntegerField(default=0)
    shops_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.brand)


class BrandCategory(BaseTimeStampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_category')
    main_pic_1 = models.ImageField(null=True, blank=True)
    main_pic_2 = models.ImageField(null=True, blank=True)
    normal_pic_1 = models.ImageField(null=True, blank=True)
    normal_pic_2 = models.ImageField(null=True, blank=True)
    normal_pic_3 = models.ImageField(null=True, blank=True)
    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return str(self.brand) 


class Country(BaseTimeStampModel):
    sortname = models.CharField(max_length=3)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'


class State(BaseTimeStampModel):
    name = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(BaseTimeStampModel):
    """
    cities do not have district
    districts have district as parent city
    """
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.ForeignKey("City", blank=True, null=True, related_name='districts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class WhoWeAre(BaseTimeStampModel):
    user = models.ForeignKey(User, related_name="who_we_are_user", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name="who_we_are_brand", on_delete=models.CASCADE)
    para_1 = models.TextField(null=True, blank=True, default=WHO_WE_ARE_PARA_1)
    para_2 = models.TextField(null=True, blank=True, default=WHO_WE_ARE_PARA_2)
    para_3 = models.TextField(null=True, blank=True, default=WHO_WE_ARE_PARA_3)
    pic = models.ImageField(null=True, blank=True)
    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return str(self.brand.id)


class BrandStyle(BaseTimeStampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_style')
    site_background = models.CharField(max_length=30, null=True, blank=True)
    main_color = models.CharField(max_length=30, null=True, blank=True)
    texts_color = models.CharField(max_length=30, null=True, blank=True)
    background_color_2nd = models.CharField(max_length=30, null=True, blank=True)
    top_nav_background = models.CharField(max_length=30, null=True, blank=True)
    top_nav_texts = models.CharField(max_length=30, null=True, blank=True)
    parallax_effect = models.BooleanField(default=False)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.site_background)


class Category(BaseTimeStampModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_homecategory')
    main_pic_1 = models.ImageField(null=True, blank=True)
    main_pic_2 = models.ImageField(null=True, blank=True)
    first_main_text = models.TextField(null=True, blank=True, default='1st Main Category')
    second_main_text = models.TextField(null=True, blank=True, default='2nd Main Category')
    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return str(self.brand) 


post_save.connect(create_user_metadata, sender=User)
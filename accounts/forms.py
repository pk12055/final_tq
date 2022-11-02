from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm

from accounts.models import (
    User, Address, Store, Brand, BrandCategory, WhoWeAre, Category
)


class SignUpForm(forms.Form):

    first_name = forms.CharField(required=True, widget=forms.TextInput(
                                attrs={'class': 'form-control q-form-control', 'required': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control q-form-control', 'required': 'required'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
                            attrs={'class': 'form-control q-form-control', 'required': 'required'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
                            {'class': 'form-control q-form-control', 'required': 'required'}))

    # check use email exist or not.
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()

        if 'email' in cleaned_data:
            cleaned_data['email'] = cleaned_data['email'].lower()

            try:
                existing_user = User.objects.get(email__iexact=cleaned_data['email'])
                if existing_user:
                    self.add_error('email', "This email is already registered.")
            except:
                pass


class LoginForm(forms.Form):
    """
    This from is used to Login the User.
    """

    email = forms.EmailField(required=True, widget=forms.TextInput(
                            attrs={'class': 'form-control q-form-control', 'required': 'required'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
                            {'class': 'form-control q-form-control', 'required': 'required'}))

    # check Email or Password is valid.
    def clean(self, *args, **kwargs):
        cleaned_data = super(LoginForm, self).clean()

        if 'email' in cleaned_data:
            cleaned_data['email'] = self.cleaned_data['email'].lower()

            if not User.objects.filter(email__iexact=cleaned_data['email']).exists():
                self.add_error('email', 'Email or Password is wrong')
            else:
                try:
                    user = User.objects.get(email=cleaned_data['email'])
                    if not user.check_password(cleaned_data['password']):
                        self.add_error('email', 'Email or Password is wrong')
                except:
                    self.add_error('email', 'Email or Password is wrong')

        return cleaned_data


class UpdatePasswordForm(forms.Form):
    """
    This from is used to change the user password.
    """

    old_password = forms.CharField(required=True, widget=forms.PasswordInput(
                                attrs={'autocomplete': 'off', 'class': 'form-control q-form-control'}))
    new_password = forms.CharField(required=True, widget=forms.PasswordInput(
                                attrs={'autocomplete': 'off', 'class': 'form-control q-form-control'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'off', 'class': 'form-control q-form-control'}))

    def __init__(self, user, data=None):
        self.user = user
        super(UpdatePasswordForm, self).__init__(data=data)

    # Check new password and confirm password match.
    def clean(self, *args, **kwargs):
        cleaned_data = super(UpdatePasswordForm, self).clean()

        if 'new_password' and 'confirm_password' in cleaned_data:
            if not cleaned_data['new_password'] == cleaned_data['confirm_password']:
                self.add_error('confirm_password', 'Passwords does not match!')

        return cleaned_data

    # Check old password is valid.
    def clean_old_password(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()

        if not self.user.check_password(cleaned_data['old_password']):
            self.add_error('old_password', 'Invalid password!')

        return cleaned_data


class UserInfoForm(forms.ModelForm):
    """
    This from is used to save the User Information.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'dob', 'country', 'city')


class StoreInfoForm(forms.ModelForm):
    """
    This from is used to save the Store Information.
    """

    class Meta:
        model = Store
        fields = ('shop_name', 'shop_type', 'shop_description', 'shop_address', 'shop_country', 'shop_state', 'shop_city', 'shop_zip_code')


class BrandInfoForm(forms.ModelForm):
    """
    This from is used to save the Brand Information.
    """

    class Meta:
        model = Brand
        fields = ('brand_name', 'brand_address', 'brand_country', 'brand_state', 'brand_city', 'brand_zip_code')


class BrandCategoryForm(forms.ModelForm):
    """
    This from is used to save the ProductReview Information.
    """

    class Meta:
        model = BrandCategory
        fields = ('main_pic_1', 'main_pic_2', 'normal_pic_1', 'normal_pic_2', 'normal_pic_3', 'is_draft')


class AddressForm(forms.ModelForm):
    """docstring for AddressForm"""
    class Meta:
        model = Address
        fields = '__all__'


class WhoWeAreForm(forms.ModelForm):

    class Meta:
        model = WhoWeAre
        fields = ('para_1', 'para_2', 'para_3', 'pic', 'is_draft')


class CategoryForm(forms.ModelForm):
    """
    This from is used to save the ProductReview Information.
    """

    class Meta:
        model = Category
        fields = ('main_pic_1', 'main_pic_2', 'first_main_text', 'second_main_text', 'is_draft')

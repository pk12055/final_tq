from django import forms
from django.forms import ModelForm

from checkout.models import BillingAddress


class BillingAddressForm(forms.ModelForm):

    class Meta:
        model = BillingAddress
        fields = ('first_name', 'last_name', 'dob')


class CheckoutSignUpForm(forms.Form):

    email = forms.EmailField(required=True, widget=forms.TextInput(
                            attrs={'class': 'form-control q-form-control', 'required': 'required'}))

    # check use email exist or not.
    def clean(self):
        cleaned_data = super(CheckoutSignUpForm, self).clean()

        if 'email' in cleaned_data:
            cleaned_data['email'] = cleaned_data['email'].lower()

            try:
                existing_user = User.objects.get(email__iexact=cleaned_data['email'])
                if existing_user:
                    self.add_error('email', "This email is already registered.")
            except:
                pass

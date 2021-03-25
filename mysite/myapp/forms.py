from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


# create class here
class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['total_amount', 'payment_status']

    def clean_customer_name(self):
        input_cust_name = self.cleaned_data['customer_name']
        if len(input_cust_name.strip()) == 0:
            raise ValidationError("Please enter a customer name")
        return input_cust_name

    def clean_customer_address(self):
        input_cust_address = self.cleaned_data['customer_address']
        if len(input_cust_address.strip()) == 0:
            raise ValidationError("Please enter a customer address")
        return input_cust_address

    def clean_customer_email(self):
        input_cust_email = self.cleaned_data['customer_email']
        validate = EmailValidator("Please enter a valid email")
        validate(input_cust_email)
        return input_cust_email

    def clean_customer_mobile(self):
        input_customer_mobile = self.cleaned_data['customer_mobile']
        if input_customer_mobile is None or len(input_customer_mobile) < 10 or len(input_customer_mobile) > 10:
            raise ValidationError("Please enter a customer mobile")
        return input_customer_mobile

    
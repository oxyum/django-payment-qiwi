
from django import forms

class CreateBillForm(forms.Form):
    amount = forms.DecimalField(max_digits=7, decimal_places=2)
    phone = forms.RegexField(regex=r'^\d{10}$', max_length=10, min_length=10)

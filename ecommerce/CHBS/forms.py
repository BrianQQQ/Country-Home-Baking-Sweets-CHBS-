from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(label="Full Name", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    number = forms.CharField(label="Phone Number", max_length=15)
    instruction = forms.CharField(label="Special Instructions", max_length=500)

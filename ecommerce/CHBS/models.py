# Author: Taiwo Akinlabi
#Code sourced from : https://www.youtube.com/watch?v=obZMr9URmVI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=2
from django.db import models
from django.contrib.auth.models import User
from decimal import *
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



# Customer model contains customer field names and property 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = PhoneNumberField(default=False, null=True)

    def __str__(self):
        return str(self.name)

# Product model contains product field names and property 
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    special = models.BooleanField(default=False, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self) -> str:
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# Order model contains order field names and property 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) 
        return round(total, 2)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        tax = sum([item.get_total for item in orderitems])* Decimal(0.13)
        total = sum([item.get_total for item in orderitems]) + tax
        return round(total, 2)
    
    @property
    def get_cart_tax(self):
        orderitems = self.orderitem_set.all()
        tax = sum([item.get_total for item in orderitems])*Decimal(0.13)
        return round(tax, 2)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

 # OrderItems model contains orderItems field names and property    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True,  blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return round(total, 2)

# Shipping model contains shipping field names and property   
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    province = models.CharField(max_length=200, null=False)
    postalcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.address
    
    

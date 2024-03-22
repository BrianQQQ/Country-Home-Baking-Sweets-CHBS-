# Author: Taiwo Akinlabi
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from decimal import *
import datetime
from .models import *
import json

#Code sourced from : https://www.youtube.com/watch?v=obZMr9URmVI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=2

# gets cookieCart data as json, loops throught the cart items & returns it as a dictionary
def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'get_cart_tax':0, 'get_cart_subtotal':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            
            product = Product.objects.get(id=i)
            subtotal = (product.price * cart[i]['quantity'])
            tax = round(subtotal * Decimal(0.13),2)
            total = round(subtotal + tax, 2)
            
            order['get_cart_subtotal'] += subtotal
            order['get_cart_tax'] += tax
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)

        except:
            pass  
    return {'items':items, 'order':order, 'cartItems':cartItems}

# get the cart data for both authenticated and unauthenticated users and returns its as a dictionary
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
       cookieData = cookieCart(request)
       cartItems = cookieData['cartItems']
       order = cookieData['order']
       items = cookieData['items']
    return {'items':items, 'order':order, 'cartItems':cartItems}

# processes the guest's order and returns the customer's info, order & order items 
def guestOrder(request, data):
    print("user is not logged in")
    print('COOKIES', request.COOKIES)
    # grabs all user data from the form 
    name = data['form']['name']
    phone = data['form']['phone']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    #querys or creates a user 
    customer, created = Customer.objects.get_or_create(
        phone=phone,
        email=email,
    )
    
    customer.name = name
    # saves a user to the database
    customer.save()

    #querys or creates the user order
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    
    return customer, order, items
# Author: Taiwo Akinlabi
#Code sourced from : https://www.youtube.com/watch?v=obZMr9URmVI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=2
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from decimal import *
import datetime
from .models import *
import json
from .utils import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.

# view function for the homepage returns the page request, urls and context dictonary containing 
# The context dictonary contains values that can retrived from the database
def homepage(request):
    products  = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    context = {'products':products, 'order':order}
    return render(request, 'CHBS/homepage.html', context)

# view function for the cart page returns the page request, urls and context dictonary
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'CHBS/cart.html', context)

# view function for the menu page returns the page request, urls and context dictonary
def menu(request):
    products  = Product.objects.all()
    context = {'products':products}
    return render(request, 'CHBS/menu.html', context)

# view function for the contact page returns the page request, urls and context dictonary
def contact(request):
    context = {}
    return render(request, 'CHBS/contact.html', context)

# view function for the checkout page returns the page request, urls and context dictonary
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems,}
 
    return render(request, 'CHBS/checkout.html', context)

# view function for the update_item page that update the cart anytim an item is removed or added for authenticated users
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete() 
    return JsonResponse('item was updated', safe=False)

# view function for the process_order page that processes both authenticated and unauthenticated users order and sends and email to the client 
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        context = {'items':items,'order':order, 'customer':customer, }
        #holds email message in a html template then reders it as a string
        template = render_to_string('chbs/email_template.html', context)

        #email format and infomation 
        email = EmailMessage(
            'Subject',
            template,
            settings.EMAIL_HOST_USER,
            ['akin0045@algonquinlive.com'],
        )

        email.fail_silently=False
        # sends email
        email.send()

    else:
        customer, order, items = guestOrder(request, data)
        context = {'items':items,'order':order, 'customer':customer, }
         #holds email message in a html template then reders it as a string
        template = render_to_string('chbs/email_template.html', context)
                #email format and infomation 
        email = EmailMessage(
            'NEW ORDER:',
            template,
            settings.EMAIL_HOST_USER,
            ['akin0045@algonquinlive.com'],
        )

        email.fail_silently=False
        email.send()
    
    total = round(Decimal(data['form']['total']), 2)
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            province=data['shipping']['province'],
            postalcode=data['shipping']['postal'],
        )

    print(request.body)

    return JsonResponse('Payment complete!', safe=False)
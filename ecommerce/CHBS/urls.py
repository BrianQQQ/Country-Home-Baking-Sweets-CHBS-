# Author: Taiwo Akinlabi
from django.urls import path
from CHBS import views

# TEMPALTE TAGGING
app_name = 'chbs'

# named urls to their respestive views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('cart/', views.cart, name='cart'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')

]
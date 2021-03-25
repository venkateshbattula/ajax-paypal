from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('showproducts', showproducts, name='showproducts'),
    path('addtocart/<int:id>', addtocart, name='addtocart'),
    path('empty_cart/', empty_cart, name='empty_cart'),
    path('view_cart', view_cart, name='view_cart'),
    path('process_payment', process_payment, name='process_payment'),
    path('payment_done', payment_done, name='payment_done'),
    path('payment_cancelled', payment_cancelled, name='payment_cancelled')

]

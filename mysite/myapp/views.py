from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db.models import Sum
from .forms import *

# Create your views here.


def index(request):
    return HttpResponse('<h1> welcome to ajax project</H1>')


def showproducts(request):
    products = Products.objects.all()
    return render(request, 'myapp/showproducts.html',  {'products': products})


def addtocart(request, id):
    current_cart = request.session.get('cart', None)
    if current_cart is None:
        request.session['cart'] = [id]
        message = 'Product has been added to cart'
    elif id not in current_cart:
        request.session['cart'].append(id)
        request.session.modified = True
        message = 'Product has been added to cart'
    else:
        message = 'Product is already in cart'
    return HttpResponse(message)


def empty_cart(request):
    current_cart = request.session.get('cart', None)
    message = ''
    if current_cart == None:
        message = 'Cart already empty'
    else:
        del request.session['cart']
        message = 'Cart is empty now'
    return HttpResponse(message)


def view_cart(request):
    current_cart = request.session.get('cart', None)
    message = ''
    if current_cart == None:
        message = 'your cart is empty'
        return render(request, 'myapp/view_cart.html', {'message': message})
    else:
        message = 'your cart has following products'
        cart_products = Products.objects.filter(pk__in=current_cart)
        total_price = Products.objects.filter(pk__in=current_cart).aggregate(Sum('price'))
        order_form = OrderForm()
        return render(request, 'myapp/view_cart.html', {'message': message,
                                                        'cart_products': cart_products,
                                                        'total_price': total_price,
                                                        'order_form': order_form
                                                        })
    # return render(request, 'myapp/empty_cart.html', {'message': message})


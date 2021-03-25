from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.db.models import Sum
from .forms import *
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def empty_cart(request):
    current_cart = request.session.get('cart', None)
    message = ''
    if current_cart is None:
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
        if request.method == "POST":
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = Orders()
                order.customer_name = request.POST['customer_name']
                order.customer_address = request.POST['customer_address']
                order.customer_email = request.POST['customer_email']
                order.customer_mobile = request.POST['customer_mobile']
                order.total_amount = total_price['price__sum']
                order.save()
                latest_order_id = Orders.objects.latest('id')
                for product in cart_products:
                    ord = OrderDetails()
                    ord.price = product.price
                    ord.name = product.product
                    ord.order_id = latest_order_id.id
                    ord.save()
                del request.session['cart']
                request.session['order_id'] = latest_order_id.id
                request.session['order_price'] = str(total_price['price__sum'])
                return redirect('process_payment')
            else:
                return render(request, 'myapp/view_cart.html', {'message': message,
                                                                'cart_products': cart_products,
                                                                'total_price': total_price,
                                                                'order_form': order_form
                                                                })
        order_form = OrderForm()
        return render(request, 'myapp/view_cart.html', {'message': message,
                                                        'cart_products': cart_products,
                                                        'total_price': total_price,
                                                        'order_form': order_form
                                                        })
    # return render(request, 'myapp/empty_cart.html', {'message': message})


def process_payment(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': request.session['order_price'],
        'item_name': 'Order #' + str(request.session['order_id']),
        'invoice': str(request.session['order_id']),
        'currency_code': 'INR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'myapp/payment_cancelled.html', {'order_amount': request.session['order_price'],
                                                            'form': form})


@csrf_exempt
def payment_done(request):
    orderobj = Orders.objects.get(pk=request.session['order_id'])
    orderobj.payment_status = True
    orderobj.save()
    del request.session['order_id']
    del request.session['order_price']
    return render(request, 'myapp/process_payment.html')


@csrf_exempt
def payment_cancelled(request):
    Orders.objects.delete(pk=request.session['order_id'])
    return render(request, 'myapp/payment_cancelled.html')


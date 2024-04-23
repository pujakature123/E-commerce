from django.shortcuts import redirect, render, HttpResponseRedirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class Home(View):
    def get(self, request):
        categories = Category.get_all_categories()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.filter_product_by_category_id(category_id)
        else:
            products = Product.get_all_products()
        return render(request, template_name='index.html', context={"products": products, "categories": categories})

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('home')


class Signup(View):
    def get(self, request):
        return render(request, template_name='signup.html')

    def post(self, request):
        data = request.POST
        first_name = data.get('fname')
        last_name = data.get('lname')
        email = data.get('email')
        mobile_no = data.get('mobile')
        password = data.get('password')
        Customer.objects.create(first_name=first_name, last_name=last_name,
                                email=email, mobile_no=mobile_no, password=make_password(password))

        # Sent email after new user registration
        # subject = 'Welcome to Quick Shopp'
        # message = f'Hi {first_name}, /n thank you for registering in Quick Shopp.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [email ]
        # send_mail( subject, message, email_from, recipient_list )

        customer = Customer.objects.get(email=email)
        request.session['customer_name'] = customer.first_name
        request.session['customer_id'] = customer.id
        request.session['email'] = customer.email
        return redirect('home')


class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        error_message = None
        return render(request, template_name='login.html', context={'error': error_message})

    def post(self, request):
        error_message = None
        logged_email = request.POST.get('email')
        logged_password = request.POST.get('password')
        try:
            customer = Customer.objects.get(email=logged_email)
            if customer:
                checked_password = check_password(
                    logged_password, customer.password)
                if checked_password == True:
                    request.session['customer_name'] = customer.first_name
                    request.session['customer_id'] = customer.id
                    request.session['email'] = customer.email
                    if Login.return_url:
                        return HttpResponseRedirect(Login.return_url)
                    else:
                        Login.return_url = None
                        return redirect('home')
                error_message = 'Invalid Password entered...!'
        except Customer.DoesNotExist:
            error_message = 'Invalid Email Id entered...!'
        return render(request, template_name='login.html', context={'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self, request):
        if request.session.get("cart"):
            prod_id = list(request.session.get("cart").keys())
            products = Product.get_products_by_ids(prod_id)
        else:
            request.session['cart'] = {}
            products = None
        return render(request, template_name='cart.html', context={"products": products})


class Checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        contact_no = request.POST.get('phone_no')
        customer_id = request.session.get('customer_id')
        customer_name = request.session.get('customer_name')
        customer_email = request.session.get('email')
        customer = Customer.objects.get(id=customer_id)
        cart = request.session.get('cart')
        products = Product.get_products_by_ids(list(cart.keys()))
        print('Mobile no:-',type(contact_no),contact_no)
        for product in products:
            Orders.objects.create(product=product,
                                  customer=customer, quantity=cart.get(
                                      str(product.id)),
                                  price=product.price, address=address,
                                  mobile_no=contact_no)

        # Sent email after placed order
        # subject = 'Your Order has been placed'
        # message = f'Hi {customer_name}, /n Your order has been placed successfully. /n Your consignment will be deliver at your place in 4-5 working day. /n Thank You..!'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [customer_email ]
        # send_mail( subject, message, email_from, recipient_list )

        request.session['cart'] = {}
        return redirect('cart')


class PlacedOrders(View):
    def get(self, request):
        customer_id = request.session.get('customer_id')
        orders = Orders.get_order_by_customer(customer_id)
        return render(request, template_name='order.html', context={'orders':orders})

from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import render
from .models import Order, OrderItem, Product
from .serializers import *
#for restframework usage as respones instead of json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#for or, and in filters
from django.db.models import Q
import datetime
#for email
from django.core.mail import send_mass_mail
from django.conf import settings

# Create your views here.
def _requestUser(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        shippingtotal = order.get_cart_total + 200


        productitems=[]
        gettotal = []
        carttotal = order.get_cart_total
        for i in items:
            gettotal.append(i.get_total)
            productitems.append(i.product)

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartitems = order['get_cart_items']

        shippingtotal = 0

        carttotal = 0
        productitems=[]
        gettotal = []

        for i in cart:
            cartitems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            carttotal = order['get_cart_total']

            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imagefront':product.imagefront,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)

            productitems=[]
            gettotal = []
            for i in items:
                productitems.append(i['product'])
                gettotal.append(i['get_total'])

        shippingtotal = order['get_cart_total'] + 200

    dic = {'items':items, 'productitems':productitems, 'gettotal':gettotal, 'carttotal':carttotal, 'order':order, 'cartitems':cartitems, 'stotal': shippingtotal}
    return dic

def index(request):
    function = _requestUser(request)
    cartitems = function['cartitems']
    products = Product.objects.all()
    productbymen = Product.objects.filter(subcategory = 'men')
    productbywomen = Product.objects.filter(subcategory = 'women')
    params = {'product':products, 'men': productbymen, 'women': productbywomen, 'cartitems':cartitems}
    return render(request, 'home/index.html', params)

def allproducts(request):
    products = Product.objects.all()
    length = len(products)
    params = {'allproduct': products, 'len':length}
    return render(request, 'home/allproducts.html', params)

def catproducts(request, cat):
    catproducts = Product.objects.filter(subcategory = cat ) | Product.objects.filter(category = cat )
    length = len(catproducts)
    params = {'len':length, 'catproducts':catproducts, 'cat':cat}
    return render(request, 'home/catproducts.html', params)

def tracker(request):
    return render(request, 'home/tracker.html')

def cart(request):
    function = _requestUser(request)
    carttotal = function['carttotal']
    params = {'carttotal': carttotal}
    return render(request, 'home/cart.html', params)

def search(request):
    if 'q' in request.GET:
        keyword = request.GET['q']
        if keyword: #if not blank
            products = Product.objects.filter(Q(name__icontains=keyword) | Q(shortdescription__icontains=keyword))
    length = len(products)
    params = {'allproduct':products, 'len':length}
    return render(request, 'home/allproducts.html',params)

def productview(request, pname):
    products = Product.objects.all()
    productbyname = Product.objects.get(name = pname)
    params = {'product': productbyname, 'allproduct': products}
    return render(request, 'home/productview.html', params)

def checkout(request):
    function = _requestUser(request)
    return render(request, 'home/checkout.html', function)

def quickview(request, pname):
    productbyname = Product.objects.get(name = pname)
    params = {'product': productbyname}
    return render(request, 'home/quickview.html', params)

def dashboard(request):
    order = Order.objects.all()
    orderitems = OrderItem.objects.all()
    address = ShippingAddress.objects.all()
    params = {'order':order, 'orderitems': orderitems, 'address':address}
    return render(request, 'home/dashboard.html', params)
# def about(request):
#     return render(request, 'home/index.html')

# def contact(request):
#     return render(request, 'home/index.html')



# apis
def header_cart(request):
    function = _requestUser(request)
    cartitems = function['cartitems']
    carttotal = function['carttotal']

    cartItems = [cartitems, carttotal]
    return JsonResponse(cartItems, safe = False)

@api_view(['GET'])
def cart_page(request):
    function = _requestUser(request)
    productitems = function['productitems']
    items = function['items']
    carttotal = function['carttotal']
    gettotal = function['gettotal']
    cartitems = function['cartitems']

    productserializer = ProductSerializer(productitems, many=True)
    itemserializer = ItemsSerializer(items, many=True)
    if carttotal == 0:
        shippingtotal = 0
    else:
        shippingtotal = carttotal + 200
    dic = {'cartitems':cartitems, 'productitems': productserializer.data, 'orderitems':itemserializer.data, 'gettotal':gettotal, 'carttotal': carttotal, 'total': shippingtotal}
    return Response(dic)

def updateItem(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartitems = order['get_cart_items']

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action  ==  'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse(cartitems, safe = False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)

    else:
        name = data['shippingform']['name']
        email = data['shippingform']['email']

        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartitems = order['get_cart_items']
        carttotal = 0


        for i in cart:
            cartitems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            carttotal = order['get_cart_total']


            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imagefront':product.imagefront,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)

        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        order = Order.objects.create(customer=customer,complete=False)

        for i in items:
            product = Product.objects.get(id=i['product']['id'])
            orderItem = OrderItem.objects.create(
                 product=product,
                 order= order,
                 quantity=i['quantity']
            )

    total = int(data['shippingform']['total'])
    order.transaction_id = transaction_id

    if total == (order.get_cart_total + 200):
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
        customer = customer,
        order = order,
        name = data['shippingform']['name'],
        email = data['shippingform']['email'],
        address = data['shippingform']['address'],
        city = data['shippingform']['city'],
        state = data['shippingform']['state'],
        zipcode = data['shippingform']['zip'],
        phone = data['shippingform']['phone'],
    )

    #for email purpose
    address = ShippingAddress.objects.all()
    orderitem = OrderItem.objects.all()
    final1 = 'Order Id = '+str(order.id)+'\nOrder Transaction Id = '+str(order.transaction_id)+'\
            \nOrder Items = '
    sendingMailtoCustomer = ''

    for j,i in enumerate(orderitem):
        if  order.id == i.order.id:
            final1 += str(i.product.name)+' ('+str(i.quantity)+')'
            if j + 1 != len(orderitem):
                final1 += '\n\t\t\t'
    for i in address:
        if  order.id == i.order.id:
            final1 += '\n\nShipping Address :- \n'+str(i.name)+'\n'+str(i.email)+', '+str(i.phone)+'\
                \n'+str(i.address)+'\n'+str(i.city)+', '+str(i.state)+', '+str(i.zipcode)
            sendingMailtoCustomer = str(i.email)

    mail1 = ('Order from Ecommerce Site', 'Order is as following:-\n\n'+final1+'', settings.EMAIL_HOST_USER, ['muqrrab041@gmail.com'])
    mail2 = ('Order from Ecommerce Site', 'Thanks for your order at Muqrrab Site.\n\nPlease keep ready exact '+str(total)+' amount at delivery day.\n\nYour order will be deliver in 3-5 working days.\n\n\n\nThanks\n\nRegards: Muhammad Muqrrab', settings.EMAIL_HOST_USER, [sendingMailtoCustomer])

    send_mass_mail((mail1, mail2), fail_silently=False)

    # send_mail(
    # 'Order from Ecommerce Site',
    # 'Order is as following:-\n\n'+final1+'',
    # settings.EMAIL_HOST_USER,
    # ['muqrrab041@gmail.com'],
    # fail_silently=False,
    # )


    return JsonResponse('Payment Complete', safe=False)
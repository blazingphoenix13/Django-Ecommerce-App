from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *

def home(request):
    totalitem=0
    topwears = Product.objects.filter(category='TW')
    bottomwears = Product.objects.filter(category='BW')
    mobiles = Product.objects.filter(category='M')
    laptops = Product.objects.filter(category='L')
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    context ={'tw':topwears,'bw':bottomwears,'mob':mobiles,'lap':laptops,'totalietm':totalitem}
    return render(request, 'app/home.html',context)


def product_detail(request,pk):
    prod = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(Q(product=prod.id) & Q(user=request.user)).exists()
    context= {'prod':prod,'item_already_in_cart':item_already_in_cart}
    return render(request, 'app/productdetail.html',context)


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    print(product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
    # if request.user.is_authenticated:
    #     user = request.user
    #     cart = Cart.objects.filter(user=user)
    #     context = {cart:'cart'} 
    # context = context
    # return render(request, 'app/addtocart.html',context)
    # return HttpResponseRedirect('/cart')
    
@login_required
def show_cart(request):
    amt,shipping_amt,total_amt = 0.0,70,0.0
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        context = {'cart':cart}    
        cart_product= [i for i in Cart.objects.all() if i.user==user]
        print(cart_product)
        print(context)
        if cart_product:
            for i in cart_product:
                tempamt = i.quantity * i.product.discounted_price
                amt += tempamt
                total_amt = amt + shipping_amt 
            # context = {'cart':cart,'total_amt':total_amt,'amt':amt} 
            return render(request,'app/addtocart.html',{'cart':cart,'total_amt':total_amt,'amt':amt})
        else:
            return render(request,'app/emptycart.html')



def plus_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']   # data fetched from ajax call
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity += 1
        c.save()
        amt,shipping_amt,total_amt = 0.0,70,0.0
        cart_product= [i for i in Cart.objects.all() if i.user==request.user]
        # print(cart_product)
        # print(context)
        for i in cart_product:
            tempamt = i.quantity * i.product.discounted_price
            amt += tempamt
        data = {'quantity': i.quantity, 'amount':amt, 'totalamount':amt+ shipping_amt} 
        return JsonResponse(data)  # this data is send to JS file after success


def minus_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']   # data fetched from ajax call
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity -= 1
        c.save()
        amt,shipping_amt,total_amt = 0.0,70,0.0
        cart_product= [i for i in Cart.objects.all() if i.user==request.user]
        # print(cart_product)
        # print(context)
        for i in cart_product:
            tempamt = i.quantity * i.product.discounted_price
            amt += tempamt
        data = {'quantity': i.quantity, 'amount':amt, 'totalamount': amt + shipping_amt }
        return JsonResponse(data)  # this data is send to JS file after success


def remove_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']   # data fetched from ajax call
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.delete()
        amt,shipping_amt,total_amt = 0.0,70,0.0
        cart_product= [i for i in Cart.objects.all() if i.user==request.user]
        # print(cart_product)
        # print(context)
        for i in cart_product:
            tempamt = i.quantity * i.product.discounted_price
            amt += tempamt
        data = {'amount':amt, 'totalamount': amt + shipping_amt }
        return JsonResponse(data)  # this data is send to JS file after success




@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

# @method_decorator(login_required,name="dispatch")
@login_required
def profile(request):
    form = CustomerProfileForm()
    if request.method=='POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congrats! Profile updated successfully')
    context={'form':form,'active':'btn-primary'}
    return render(request, 'app/profile.html',context)

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    context={'add':add,'active':'btn-primary'}
    return render(request, 'app/address.html',context)

@login_required
def orders(request):
    user = request.user
    order_placed = OrderPlaced.objects.filter(user=user)
    context = {'op':order_placed}
    return render(request, 'app/orders.html',context)

# def change_password(request):
#     return render(request, 'app/changepassword.html')


def mobile(request,data=None):
    if data==None:
        mob = Product.objects.filter(category='M')
    elif data=='Samsung' or data=='Micromax' or data=='Google':
        mob = Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mob = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mob = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    context = {'mob':mob}
    return render(request, 'app/mobile.html',context)

# def login(request):
#     return render(request, 'app/login.html')


def customerregistration(request):
    form = CustomerRegistrationForm()
    if request.method=='POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congrats! Registered Successfully')
            form.save()
    context = {'form' :form}
    return render(request, 'app/customerregistration.html',context)


# def checkout(request):
#     return render(request, 'app/checkout.html')
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amt,shipping_amt,total_amt = 0.0,70,0.0
    cart_product= [i for i in Cart.objects.all() if i.user==request.user]
        # print(cart_product)
        # print(context)
    if cart_product:
        for i in cart_product:
            tempamt = i.quantity * i.product.discounted_price
            amt += tempamt
        total_amt = amt + shipping_amt
    context = {'add':add,'cart':cart_items,'total_amt':total_amt}
    return render(request, 'app/checkout.html',context)


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')  # fetching radio button using its name parameter from checkout.html
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for i in cart:
        OrderPlaced(user=user, customer=customer, product=i.product,quantity= i.quantity).save()
        i.delete() 
    return redirect('/orders')
from django.shortcuts import render,redirect,HttpResponse
from app.models import Category,Product,Contact_us,Order,Brand
from django.contrib.auth import authenticate,login
from app.models import UserCreateForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def Master(request):
    return render(request,'master.html')

def Index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')

    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by("-id")

    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by("-id")

    else:
        product = Product.objects.all()

    context = {"Name":"Home",
               'category':category,
               'product':product,
               'brand':brand,
               }
    return render(request, 'index.html',context)
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # new_user = authenticate(
            #     uername = form.cleaned_data['username'],
            #     password = form.cleaned_data['password1'])
            login(request,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
    context = {"Name":"Signup",
        'form': form,
    }
    return render(request,'registration/signup.html',context)
#Add To Cart
@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")

@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/accounts/login/")
def cart_detail(request):
    context={"Name":"Login"}
    return render(request, 'cart/cart_detail.html',context)

def Contact_Page(request):
    if request.method == 'POST':
        contact = Contact_us(
            name = request.POST.get('name'),
            email= request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
    context = {"Name":"Contact Us"}
    return render(request,'contact.html',context)

def CheckOut(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        uid=request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)

        for i in cart:
            a = int(cart[i]['price'])
            b= cart[i]['quantity']
            total = a*b
            order = Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                total = total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')

    # return HttpResponse('Check Out Page')

def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user = user)
    context = {'order':order,"Name":"Orders"}
    return render(request,'order.html',context)

def Product_Page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    categoryID = request.GET.get('category')
    brandID = request.GET.get('brand')

    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by("-id")
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by("-id")
    else:
        product = Product.objects.all()

    context={
        'category':category,
        'brand':brand,
        'product':product,
        "Name":"Products"
    }
    return render(request,'product.html',context)

def Product_Detail(request,id):
    product=Product.objects.filter(id=id).first()
    context={
            'product':product,"Name":Product.objects.get(id=id)
    }
    return render(request,'product_detail.html',context)
def Search(request):
    query = request.GET["query"]
    product=Product.objects.filter(name__icontains=query)

    context={"Name":"Search",
        'product':product,
    }
    return render(request,'search.html',context)
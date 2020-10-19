from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from order.models import ShopCart, ShopCartForm
from product.models import Category, Product, Images, Comment


# Create your views here.
def index(request):
    return HttpResponse("Order Page is up and running")


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User session information

    checkproduct = ShopCart.objects.filter(product_id=id)
    # Check product in shopcart
    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart

    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # update shop cart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Product is added to shopcart')
        return HttpResponseRedirect(url)

    else:  # This not comes from product detail page
        if control == 1:  # update shop cart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:  # Insert to Shop cart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
    }

    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Product deleted successfully")
    return HttpResponseRedirect("/shopcart")

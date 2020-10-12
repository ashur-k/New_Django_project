from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from home.models import Setting, ContactForm, ContactMessage
from product.models import Category, Product
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    page = "home"
    context = {
        'setting': setting,
        'page': page,
        'category': category
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {
            'setting': setting,
        }
    return render(request, 'about.html', context)


def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # Create relation with model
            data.name = form.cleaned_data['name']  # Get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message has ben sent.")

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {
        'setting': setting,
        'form': form,
    }
    return render(request, 'contactus.html', context)


def category_products(request, id, slug):
    products = Product.objects.filter(category_id=id)
   
    return HttpResponse(products)

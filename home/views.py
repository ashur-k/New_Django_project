import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from home.models import Setting, ContactForm, ContactMessage, FAQ
from product.models import Category, Product, Images, Comment, Variants

from home.forms import SearchForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


# Create your views here.
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    products_latest = Product.objects.all().order_by('-id')[:4]
    products_picked = Product.objects.all().order_by('?')[:4]

    page = "home"
    context = {
        'setting': setting,
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        'category': category,
    }
    return render(request, 'index.html', context)


def aboutus(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {
            'setting': setting,
            'category': category,
        }
    return render(request, 'about.html', context)


def contactus(request):
    category = Category.objects.all()
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
        'category': category,
    }
    return render(request, 'contactus.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)

    context = {
        'products': products,
        'category': category,
        'catdata': catdata,
    }

    return render(request, 'category_products.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {
                'products': products,
                'query': query,
                'category': category,
            }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title + " > " + rs.category.title
            results.append(product_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, id, slug):
    query = request.GET.get('q')

    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    print(product.averageview)

    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
    }

    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color: ' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant = Variants.objects.get(id=variants[0].id)

        context.update({
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'query': query,
                        })
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        'category': category,
        'faq': faq,
    }
    return render(request, 'faq.html', context)

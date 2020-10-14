from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from product.models import CommentForm, Comment, Category, Product, Images


# Create your views here.
def index(request):
    return HttpResponse('<h1>My Product App</h1><hr>')


def addcomment(request, id):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)    
    comments = Comment.objects.filter(product_id=id, status='True')

    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent.")

    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
    }

    return render(request, 'product_detail.html', context)

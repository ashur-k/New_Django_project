from django.shortcuts import render


# Create your views here.
def index(request):
    university = "something"
    dept = "some department"
    context = {
        'university': university,
        'department': dept
    }
    return render(request, 'index.html', context)

from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'message': 'hello'
    }
    return render(request, 'index.html', context)
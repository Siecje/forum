from django.shortcuts import render
from dequorum.models import Category


def home(request):
    categories = Category.objects.all()

    return render(request, 'drew/home.html', {'categories': categories})
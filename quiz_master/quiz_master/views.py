from django.shortcuts import render


def home(request, category_slug=None):
    return render(request, 'home.html',)

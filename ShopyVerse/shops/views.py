from django.shortcuts import render
from django.urls import reverse
from .models import ProductDetails
from math import ceil

# Create your views here.
def index(request):
    products = ProductDetails.objects.all()
    n = len(products)
    print(n)
    nSlides = n//4 + ceil((n/4)-(n//4))
    param = {
        'no_of_slides': nSlides,
        'product': products,
        'range': range(1, nSlides)
    }

    return render(request, "shops/index.html", param)

def products(request):
    return render(request, "shops/product.html")

def shop(request):
    return render(request, "shops/shop.html")

def contacts(request):
    return render(request, "shops/contact.html")

def cart(request):
    return render(request, "shops/cart.html")

def loginPage(request):
    # login_url = reverse('login')
    return render(request, "shops/login.html")

def signupPage(request):
    return render(request, "shops/signup.html")

def checkout(request):
    return render(request, "shops/checkout.html")
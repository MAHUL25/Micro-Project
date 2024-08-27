from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "shops/index.html")

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
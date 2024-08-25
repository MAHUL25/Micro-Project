from django.shortcuts import render

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
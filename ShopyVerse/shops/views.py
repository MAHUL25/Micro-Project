from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse
from .models import ProductDetails, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from math import ceil
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

products = ProductDetails.objects.all()
# n = len(products)
n = 10
nSlides = n//4 + ceil((n/4)-(n//4))
param = {
    'no_of_slides': nSlides,
    'product': products,
    'range': range(1, nSlides)
}

name='login'
# Create your views here.
def index(request):
    return render(request, "shops/index.html", param)

def products(request, p_id):
    print(p_id)
    product = ProductDetails.objects.get(pk=p_id)
    print(product)
    return render(request, "shops/product.html", {'product': product})

def shop(request):
    return render(request, "shops/shop.html", param)

def contacts(request):
    return render(request, "shops/contact.html")

def cart(request):
    return render(request, "shops/cart.html")

def loginPage(request):
    # login_url = reverse('login')
    if request.method == 'POST':
        print("hello")
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)

        try:
            user = CustomUser.objects.get(username=username)
            hashedpassword = user.password
            print(hashedpassword)  # This returns the hashed password
        except CustomUser.DoesNotExist:
            return render(request, "shops/login.html") 

        #user = authenticate(request, username=username, password=password)
        if check_password(password, hashedpassword):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = render(request, "shops/index.html")
            response.set_cookie('access_token', access_token, httponly=True, samesite='Strict')
            response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Strict')
            access_token = request.COOKIES.get('access_token')
            refresh_token = request.COOKIES.get('refresh_token')
            print(access_token)
            print(refresh_token)

            return render(request, "shops/profile.html",  {'username': username, 'email':user.email}) 
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, "shops/login.html") 
        
    # login_url = reverse('login')
    return render(request, "shops/login.html")

def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username,email,password)

        # Validate input (basic validation)
        if not username or not email or not password:
            return render(request, 'shops/signup.html', {'error': 'All fields are required'})
        
        try:
            # Create the user with hashed password
            user = CustomUser(
                username=username,
                email=email,
                password=make_password(password)  # Hashing the password
            )
            print(password,'hi1')
            user.save()
            print('hi2')    

            refresh = RefreshToken.for_user(user) #creates a new JWT refresh token for the specified user
            access_token = str(refresh.access_token)  
            refresh_token = str(refresh)

            response = render(request, "shops/login.html")
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)

            #login(request, user)
            return render(request, "shops/profile.html",  {'username': username, 'email':email}) 
        except ValidationError as e:
            return render(request, 'shops/signup.html', {'error': str(e)})
    return render(request, "shops/signup.html")

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({'message': f'Hello, {user.username}!'})

def profile(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    print(access_token)
    print(refresh_token, "hello")
    username = "new user"
    email = "newuser@gmail.com"
    return render(request, "shops/profile.html", {'username': username, 'email': email})

def addProduct(request):
    return render(request, "shops/addproduct.html")

def checkout(request):
    return render(request, "shops/checkout.html")
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import ProductDetails, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from math import ceil
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from rest_framework.authtoken.models import Token

# products = ProductDetails.objects.all()
User = get_user_model()
# param = {
#     'no_of_slides': nSlides,
#     'product': products,
#     'range': range(1, nSlides)
# }

total = 0

# Create your views here.
def index(request):
    products = ProductDetails.objects.all()
    username = request.user.username
    print(username, "hello")
    if username == "":
        username = "New User"
    context = {'products': products, 'username': username}
    return render(request, "shops/index.html", context)

def logout_view(request):
    logout(request)  # This will log out the user and clear the session
    print("logout")
    response = redirect('shops:index')  # Redirect to a specific page after logout
    # Optionally, clear any JWT tokens if you're using JWT for session management
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def products(request, p_id):
    print(p_id)
    product = ProductDetails.objects.get(pk=p_id)
    print(product)
    username = request.user.username
    if username == "":
        username = "New User"
    context = {'product': product, 'username': username}
    return render(request, "shops/product.html", context)

def shop(request):
    products = ProductDetails.objects.all()
    username = request.user.username
    if username == "":
        username = "New User"
    context = {'products': products, 'username': username}
    return render(request, "shops/shop.html", context)

def contacts(request):
    username = request.user.username
    if username == "":
        username = "New User"
    return render(request, "shops/contact.html",{'username': username})

def cart(request):
    global total
    username = request.user.username
    if username == " ":
        username = "New User"
    return render(request, "shops/cart.html",{'total': total, 'username': username})

def loginPage(request):
    # login_url = reverse('login')
    if request.method == 'POST':
        # import json
        # data = json.loads(request.body)
        # username = data.get('username')
        # password = data.get('password')
        print("hello")
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        try:
            user = CustomUser.objects.get(username=username)
            hashedpassword = user.password
            print(hashedpassword)  # This returns the hashed password
        except CustomUser.DoesNotExist:
            return render(request, "shops/login.html") 

        #user = authenticate(request, username=username, password=password)
        if check_password(password, hashedpassword):
            refresh = RefreshToken.for_user(user)
            # print(refresh)
            response = render(request, "shops/index.html")
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response.set_cookie('access_token', access_token, httponly=True, samesite='Strict', max_age=3600)  # 1 hour expiry
            response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Strict', max_age=86400)  # 1 day expiry
            at = request.COOKIES.get('access_token')
            rt = request.COOKIES.get('refresh_token')
            print("hello",rt)
            if user.address == "":
                address = "Edit Address"
            else:
                address = user.address
            # return JsonResponse({
            #     'access_token': access_token,
            #     'refresh_token': refresh_token
            # })
            return render(request, "shops/profile.html",  {'username': username, 'email':user.email, 'address': address}) 
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, "shops/login.html") 
        
    # login_url = reverse('login')
    return render(request, "shops/login.html")

def editprofile(request):
    if request.method == 'POST':
        print("hello")
        # Example of how to handle the form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        print(username,email,address)
        # Assuming the user is logged in and we want to update their profile
        user = CustomUser.objects.get(username=username)        
        print(user)

        # Optionally check if the username in the form is the same as the logged-in user
        user.email = email
        user.address = address
        user.save()
        if user.address == "":
            address = "Edit Address"
        else:
            address = user.address
        print(address)

    # Handle GET request or display the form
    return render(request, "shops/profile.html",{'username': username, 'email':email, 'address':address})

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
            # auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            print("hi3")
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response = redirect('shops:index')  # Redirect after signup
            response.set_cookie('access_token', access_token, httponly=True, samesite='Strict')
            response.set_cookie('refresh_token', refresh_token, httponly=True, samesite='Strict')
            return render(request, "shops/profile.html",  {'username': username, 'email':email, 'address': 'Edit Address'}) 
        except ValidationError as e:
            return render(request, 'shops/signup.html', {'error': str(e)})
    return render(request, "shops/signup.html")

# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         return Response({'message': f'Hello, {user.username}!'})

def profile(request):
    print("hello")
    user = CustomUser.objects.get(username=request.user.username)
    if user.address == "":
        address = "Edit Address"
    else:
        address = user.address
    print(address)
    return render(request, "shops/profile.html", {'username': request.user.username if request.user else "new user", 'email': request.user.email if request.user else "newuser@gmail.com", 'address':address})

def addProduct(request):
    if request.method=="POST":
        product_id = request.POST.get('pid')
        product_name = request.POST.get('pname')
        display_name = request.POST.get('DisplayName')
        category = request.POST.get('Category')
        discounted_price = request.POST.get('DiscountedPrice')
        actual_price = request.POST.get('ActualPrice')
        rating = request.POST.get('Rating')
        about_product = request.POST.get('about')
        product_image = request.FILES.get('image')

        product = ProductDetails(
            product_id = product_id,
            product_name = product_name,
            display_name = display_name,
            category = category,
            discounted_price = int(discounted_price),
            actual_price = int(actual_price),
            rating = float(rating),
            about_product = about_product,
            image = product_image
        )
        product.save()
        messages.success(request, "Product uploaded successfully")
        return render(request, "shops/addproduct.html")
    
    username = request.user.username
    if username == "":
        username = "New User"

    return render(request, "shops/addproduct.html",{'username': username})

def checkout(request):
    return render(request, "shops/checkout.html")

def product_function(request, p_id):
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'add_to_cart':
            product = ProductDetails.objects.get(pk=p_id)
            if request.method == 'POST':
                global total
                total += product.discounted_price
                return render(request, "shops/cart.html", {
                    'total': total,
                    'username': request.user.username if request.user else "new user"
                })
        elif action == 'buy_now':
            # Handle buying now
            pass
        elif action == 'delete':
            product = ProductDetails.objects.get(pk=p_id)
            if request.method == 'POST':
                product.delete()
                return render(request, "shops/shop.html")  # Redirect to a success page or another view
    return render(request, "shops/product.html")
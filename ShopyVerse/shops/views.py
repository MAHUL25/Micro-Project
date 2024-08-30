from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import ProductDetails, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from math import ceil
from django.shortcuts import render, redirect
from django.contrib.auth import logout
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
from django.shortcuts import render

products = ProductDetails.objects.all()
User = get_user_model()
# n = len(products)
n = 10
nSlides = n//4 + ceil((n/4)-(n//4))
param = {
    'no_of_slides': nSlides,
    'product': products,
    'range': range(1, nSlides)
}

# Create your views here.
def index(request):
    username = request.user.username
    print(username, "hello")
    if username == "":
        username = "New User"
    context = {'param': param, 'username': username}
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
    context = {'param': param, 'username': username}
    return render(request, "shops/product.html", context)

def shop(request):
    username = request.user.username
    if username == "":
        username = "New User"
    context = {'param': param, 'username': username}
    return render(request, "shops/shop.html", context)

def contacts(request):
    username = request.user.username
    if username == "":
        username = "New User"
    return render(request, "shops/contact.html",{'username': username})

def cart(request):
    username = request.user.username
    if username == "":
        username = "New User"
    return render(request, "shops/cart.html",{'username': username})

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            try:
                # Authenticate the user using the access_token
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(access_token)
                request.user = jwt_auth.get_user(validated_token)
            except:
                request.user = None

        return None

# Example of refreshing token logic
def refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = JsonResponse({'access_token': access_token})
            response.set_cookie('access_token', access_token, httponly=True, samesite='Strict')
            return response
        except:
            return JsonResponse({'error': 'Invalid refresh token'}, status=401)
    else:
        return JsonResponse({'error': 'Refresh token not provided'}, status=400)

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

# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         return Response({'message': f'Hello, {user.username}!'})

def profile(request):
    return render(request, "shops/profile.html", {'username': request.user.username if request.user else "new user", 'email': request.user.email if request.user else "newuser@gmail.com"})

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
from django.urls import path
from . import views

app_name = "shops"
urlpatterns = [
    path("", views.index, name="index"),
    path("product/<str:p_id>", views.products, name="products"),
    path("shop/", views.shop, name="shop"),
    path("contact-us/", views.contacts, name="contact"),
    path("cart/", views.cart, name="cart"),
    path("login/", views.loginPage, name="login"),
    path("signup/", views.signupPage, name="signup"),
    path("checkout/", views.checkout, name="checkout"),
    path("profile/", views.profile, name="profile"),
    path("add-product/", views.addProduct, name="addProduct"),
    path('logout/', views.logout_view, name='logout')
]
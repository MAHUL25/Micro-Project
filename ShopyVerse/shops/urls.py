from django.urls import path
from . import views

app_name = "shops"
urlpatterns = [
    path("", views.index, name="index"),
    path("/product", views.products, name="products"),
    path("/shop", views.shop, name="shop"),
    path("/contact-us", views.contacts, name="contact"),
    path("/cart", views.cart, name="cart"),
]
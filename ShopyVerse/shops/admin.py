from django.contrib import admin
from .models import ProductDetails, CustomUser

# Register your models here.
admin.site.register(ProductDetails)
admin.site.register(CustomUser)
from django.db import models
import uuid

# Create your models here.
class ProductDetails(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True)
    product_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=100, default="")
    category = models.CharField(max_length=100, default="")
    discounted_price = models.IntegerField(default=0)
    actual_price = models.IntegerField(default=0)
    rating = models.FloatField(max_length=5, default=0)
    about_product = models.CharField(max_length=250, default="")
    image = models.ImageField(upload_to='shops/images', default="")

    def __str__(self):
        return self.product_name
    

class CustomUser(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=36)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=90)  # Use EmailField for email addresses
    password = models.CharField(max_length=128)
    address = models.CharField(max_length=100, default="")


    def __str__(self):
        return self.username
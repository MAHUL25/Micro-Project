from django.db import models

# Create your models here.
class ProductDetails(models.Model):
    product_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="")
    discounted_price = models.IntegerField(default=0)
    actual_price = models.IntegerField(default=0)
    rating = models.FloatField(max_length=5, default=0)
    about_product = models.CharField(max_length=250, default="")
    image = models.ImageField(upload_to='shops/images', default="")

    def __str__(self):
        return self.product_name
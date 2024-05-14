from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()

class Product(models.Model):
    division_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    image_path = models.CharField(max_length=255, blank=True, null=True, default="")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    recommended = models.BooleanField()
    

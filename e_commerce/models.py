from django.db import models
from django.contrib.auth.models import User

# run this to update the database
# python manage.py migrate --run-syncdb
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()



class Product(models.Model):
    division_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    recommended = models.BooleanField()




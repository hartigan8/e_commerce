from django.db import models


# run this to update the database
# manage.py migrate --run-syncdb
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

class Product(models.Model):
    division_name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.division_name} - {self.department_name} - {self.class_name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    recommended = models.BooleanField()

    def __str__(self):
        return f"{self.user.name} - {self.product.division_name} - {self.rating}"


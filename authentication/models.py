from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
class CustomUser(models.Model):
    business_name = models.CharField(max_length=255, blank=True)
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    best_selling_products = models.TextField(blank=True)

    def __str__(self):
        return self.email
'''    
class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.amount} units"
    
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
    
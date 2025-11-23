from django.db import models

# Create your models here.
class CustomUser(models.Model):
    business_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    best_selling_products = models.TextField(blank=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Sales(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"
    
class Expense(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
    
class Profit(models.Model):
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Net Profit: {self.net_profit}"
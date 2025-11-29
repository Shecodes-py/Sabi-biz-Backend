from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PAYMENT_METHOD(models.TextChoices):
    CASH = 'CASH', 'Cash'
    BANK_TRANSFER = 'BANK TRANSFER', 'Bank Transfer'
    DEBIT_CARD = 'DEBIT CARD', 'Debit Card'

class Sales(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_mtd = models.CharField(max_length=20, choices=PAYMENT_METHOD.choices, default=PAYMENT_METHOD.CASH)

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
    
from django.db import models
from django.conf import settings

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('SALE', 'Sale'),
        ('EXPENSE', 'Expense'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True) # e.g., "Rent", "Inventory"
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}: {self.amount} - {self.description}"
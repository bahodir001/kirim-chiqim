from django.db import models
from users.models import CustomUser

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('transport', 'Yo‘l harajatlari'),
        ('taxes', 'Soliqlar'),
        ('health', 'Salomatlik'),
        ('entertainment', 'Ko‘ngilochar'),
        ('other', 'Boshqa')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('currency', 'Valyuta')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.expense_type} - {self.amount}"

from django.db import models
from users.models import CustomUser

class Income(models.Model):
    INCOME_TYPE_CHOICES = [
        ('salary', 'Oylik'),
        ('advance', 'Avans'),
        ('business', 'Biznes')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('currency', 'Valyuta')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='incomes')
    income_type = models.CharField(max_length=10, choices=INCOME_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.income_type} - {self.amount}"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    """Model for transaction categories"""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#6C63FF')  # Hex color for chart
    icon = models.CharField(max_length=10, default='💰')  # Emoji icon
    is_income = models.BooleanField(default=False)  # True for income categories, False for expense categories
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Model for financial transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} - ${self.amount} ({self.transaction_type})"
    
    @property
    def signed_amount(self):
        """Return amount with proper sign for expenses"""
        return -abs(self.amount) if self.transaction_type == 'expense' else abs(self.amount)

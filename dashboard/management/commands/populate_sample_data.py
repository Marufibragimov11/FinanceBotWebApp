from django.core.management.base import BaseCommand
from dashboard.models import Category, Transaction
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories...')
        
        # Create categories
        categories_data = [
            # Income categories
            {'name': 'Salary', 'color': '#4CAF50', 'icon': '💰', 'is_income': True},
            {'name': 'Freelance', 'color': '#2196F3', 'icon': '💼', 'is_income': True},
            {'name': 'Investment', 'color': '#FF9800', 'icon': '📈', 'is_income': True},
            
            # Expense categories
            {'name': 'Food & Dining', 'color': '#F44336', 'icon': '🍽️', 'is_income': False},
            {'name': 'Transportation', 'color': '#9C27B0', 'icon': '🚗', 'is_income': False},
            {'name': 'Entertainment', 'color': '#E91E63', 'icon': '🎬', 'is_income': False},
            {'name': 'Utilities', 'color': '#607D8B', 'icon': '⚡', 'is_income': False},
            {'name': 'Shopping', 'color': '#795548', 'icon': '🛍️', 'is_income': False},
            {'name': 'Healthcare', 'color': '#3F51B5', 'icon': '🏥', 'is_income': False},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        self.stdout.write('Creating sample transactions...')
        
        # Create sample transactions
        transactions_data = [
            # Income transactions
            {'name': 'Monthly Salary', 'amount': Decimal('3500.00'), 'category': 'Salary', 'type': 'income'},
            {'name': 'Freelance Project', 'amount': Decimal('850.00'), 'category': 'Freelance', 'type': 'income'},
            {'name': 'Stock Dividends', 'amount': Decimal('120.50'), 'category': 'Investment', 'type': 'income'},
            {'name': 'Bonus Payment', 'amount': Decimal('500.00'), 'category': 'Salary', 'type': 'income'},
            
            # Expense transactions
            {'name': 'Grocery Shopping', 'amount': Decimal('85.50'), 'category': 'Food & Dining', 'type': 'expense'},
            {'name': 'Gas Station', 'amount': Decimal('45.00'), 'category': 'Transportation', 'type': 'expense'},
            {'name': 'Netflix Subscription', 'amount': Decimal('15.99'), 'category': 'Entertainment', 'type': 'expense'},
            {'name': 'Electric Bill', 'amount': Decimal('120.00'), 'category': 'Utilities', 'type': 'expense'},
            {'name': 'Coffee Shop', 'amount': Decimal('4.50'), 'category': 'Food & Dining', 'type': 'expense'},
            {'name': 'Clothing Store', 'amount': Decimal('89.99'), 'category': 'Shopping', 'type': 'expense'},
            {'name': 'Doctor Visit', 'amount': Decimal('150.00'), 'category': 'Healthcare', 'type': 'expense'},
            {'name': 'Restaurant Dinner', 'amount': Decimal('65.00'), 'category': 'Food & Dining', 'type': 'expense'},
            {'name': 'Uber Ride', 'amount': Decimal('12.50'), 'category': 'Transportation', 'type': 'expense'},
            {'name': 'Movie Tickets', 'amount': Decimal('24.00'), 'category': 'Entertainment', 'type': 'expense'},
            {'name': 'Water Bill', 'amount': Decimal('45.00'), 'category': 'Utilities', 'type': 'expense'},
        ]
        
        # Create transactions with dates spread over the last month
        base_date = datetime.now() - timedelta(days=30)
        
        for i, trans_data in enumerate(transactions_data):
            # Spread transactions over the last 30 days
            transaction_date = base_date + timedelta(days=random.randint(0, 30))
            
            Transaction.objects.get_or_create(
                name=trans_data['name'],
                amount=trans_data['amount'],
                category=categories[trans_data['category']],
                transaction_type=trans_data['type'],
                defaults={
                    'date': transaction_date,
                    'description': f'Sample {trans_data["type"]} transaction'
                }
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write(f'Created {len(categories)} categories and {len(transactions_data)} transactions.')

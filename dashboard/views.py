from django.shortcuts import render
from django.db.models import Sum, Q
from .models import Transaction, Category
from decimal import Decimal
import json


# Create your views here.

def main_dashboard(request):
    """
    Main dashboard view that renders the dashboard page with real data from the database.
    """
    # Calculate total income and expenses
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    total_expenses = Transaction.objects.filter(transaction_type='expense').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    # Calculate current balance
    current_balance = total_income - total_expenses

    # Get recent transactions (latest 5)
    recent_transactions = Transaction.objects.all()[:5]

    # Prepare recent transactions data for template
    recent_transactions_data = []
    for transaction in recent_transactions:
        recent_transactions_data.append({
            'name': transaction.name,
            'amount': float(transaction.signed_amount),
            'type': transaction.transaction_type,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category': transaction.category.name,
            'icon': transaction.category.icon,
        })

    # Get analytics data for the donut chart
    # Group expenses by category
    expense_categories = Transaction.objects.filter(transaction_type='expense').values(
        'category__name', 'category__color'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Prepare analytics data for JavaScript
    analytics_data = {}
    for category in expense_categories:
        category_name = category['category__name']
        category_total = float(category['total'] or 0)
        analytics_data[category_name] = {
            'amount': category_total,
            'color': category['category__color']
        }

    # Keep upcoming payments as hardcoded for now (as requested)
    upcoming_payments = [
        {'name': 'Netflix', 'amount': 15.99, 'date': '2024-01-15'},
        {'name': 'Spotify', 'amount': 9.99, 'date': '2024-01-20'},
        {'name': 'Gym Membership', 'amount': 49.99, 'date': '2024-01-25'},
    ]

    context = {
        'balance': float(current_balance),
        'upcoming_payments': upcoming_payments,
        'income': float(total_income),
        'expenses': float(total_expenses),
        'recent_transactions': recent_transactions_data,
        'analytics_data': json.dumps(analytics_data),
    }

    return render(request, 'index.html', context)

from datetime import date
from django.shortcuts import render
from .calculator import get_outstanding_invoices, get_monthly_totals


def dashboard(request):
    today = date.today()
    if today.month == 1:
        start = date(today.year-1, 12, 1)
    else:
        start = date(today.year, today.month-1, 1)

    context = {
        'month': start.strftime('%B %Y'),
        'totals': get_monthly_totals(start.year, start.month),
        'outstanding': get_outstanding_invoices()
    }

    return render(request, 'invoices/dashboard.html', context=context)

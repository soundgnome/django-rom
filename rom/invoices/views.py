from datetime import date
from django.shortcuts import render
from .calculator import get_outstanding_invoices, get_monthly_totals


def dashboard(request):
    totals = []

    start = date.today()
    earliest = date(start.year-1, start.month, 1)

    while (start > earliest):
        if start.month == 1:
            start = date(start.year-1, 12, 1)
        else:
            start = date(start.year, start.month-1, 1)

        month = get_monthly_totals(start.year, start.month)
        if month['income']:
            month['month'] = start.strftime('%B %Y')
            totals.append(month)

    context = {
        'monthly_totals': totals,
        'outstanding': get_outstanding_invoices()
    }

    return render(request, 'invoices/dashboard.html', context=context)

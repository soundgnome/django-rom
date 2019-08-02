from datetime import date, timedelta

from django.shortcuts import render

from .calculator import get_outstanding_invoices, get_monthly_totals
from .models import Expense, Invoice


def dashboard(request):
    totals = []

    start = date.today()
    earliest = date(start.year-1, start.month, 1)

    while (start > earliest):

        month = get_monthly_totals(start.year, start.month)
        if month['income'] or month['invoiced']:
            month['month'] = start.strftime('%B %Y')
            totals.append(month)

        if start.month == 1:
            start = date(start.year-1, 12, 1)
        else:
            start = date(start.year, start.month-1, 1)

    context = {
        'monthly_totals': totals,
        'outstanding': get_outstanding_invoices()
    }

    return render(request, 'invoices/dashboard.html', context=context)


def graphs(request):

    arg = request.GET.get('end')
    end = date(*[int(x) for x in arg.split('-')]) if arg else date.today()

    arg = request.GET.get('start')
    start = date(*[int(x) for x in arg.split('-')]) if arg else date(end.year-1, end.month, 1)

    changes = {}
    for income in Invoice.objects.filter(date_received__gte=start).filter(date_received__lte=end).order_by('date_received'):
        if income.date_received in changes:
            changes[income.date_received] += income.amount
        else:
            changes[income.date_received] = income.amount

    for expense in Expense.objects.filter(date__gte=start).filter(date__lte=end).order_by('date'):
        if expense.date in changes:
            changes[expense.date] -= expense.amount
        else:
            changes[expense.date] = -expense.amount

    balance = changes[start] if start in changes else 0
    balances = [ _js_coords(start, balance) ]
    day = start
    while day < end:
        day += timedelta(days=1)
        if day in changes:
            balance += changes[day]
            balances.append(_js_coords(day, balance))

    context = {
        'start': start,
        'end': end,
        'inputs': {
            'start': start.strftime('%Y-%m-%d'),
            'end': end.strftime('%Y-%m-%d'),
        },
        'balances': '[%s]' % ','.join(balances),
    }

    return render(request, 'invoices/graphs.html', context=context)


def _js_coords(day, balance):
    return '{x:%s, y:%s}' % (day.strftime('new Date(%Y,%m,%d)'), balance)

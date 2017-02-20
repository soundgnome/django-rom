from datetime import date, timedelta
from decimal import Decimal
from django.db.models import Q, Sum
from .models import Expense, Invoice


def get_monthly_totals(year, month):
    totals = {}

    start = date(year, month, 1)
    if month == 12:
        end = date(year+1, 1, 1)
    else:
        end = date(year, month+1, 1)

    totals['income'] = _get_income_total(start, end)
    totals['invoiced'] = _get_invoiced_total(start, end)
    totals['total_expenses'] = _get_raw_total(Expense.objects, start, end)
    totals['expenses_before_tax'] = _get_raw_total(_get_filtered_expenses(tax=False), start, end)
    totals['adjusted_expenses'] = _get_adjusted_total(Expense.objects, start, end)

    return totals


def get_outstanding_invoices(since=None):
    invoices = {}
    all_outstanding = Invoice.objects.filter(date_received=None)

    aggregate = all_outstanding.aggregate(Sum('amount'))
    invoices['total_balance'] = aggregate['amount__sum'] or 0

    if since is None:
        since = date.today()
    start = since - timedelta(days=30)
    invoices['overdue'] = all_outstanding.filter(date_sent__lte=start)

    aggregate = invoices['overdue'].aggregate(Sum('amount'))
    invoices['overdue_balance'] = aggregate['amount__sum'] or 0

    return invoices


def _get_adjusted_total(expenses, start, end):
    total = Decimal('0')

    aggregate = expenses.filter(date__gte=start).filter(date__lt=end). \
                filter(month_span=1).aggregate(Sum('amount'))
    total += aggregate['amount__sum'] or 0

    if start.month >= 3:
        quarterly_start = date(start.year, start.month-2, 1)
    else:
        quarterly_start = date(start.year-1, start.month+10, 1)
    aggregate = expenses.filter(date__gte=quarterly_start).filter(date__lt=end). \
                filter(month_span=3).aggregate(Sum('amount'))
    if aggregate['amount__sum']:
        total += aggregate['amount__sum']/3

    annual_start = date(end.year-1, end.month, 1)
    aggregate = expenses.filter(date__gte=annual_start).filter(date__lt=end). \
                filter(month_span=12).aggregate(Sum('amount'))
    if aggregate['amount__sum']:
        total += aggregate['amount__sum']/12

    return total.quantize(Decimal('.01'))


def _get_filtered_expenses(tax=False):
    if tax:
        expenses = Expense.objects.filter(Q(type=Expense.Type.TAX_QUARTERLY) | Q(type=Expense.Type.TAX_ANNUAL))
    else:
        expenses = Expense.objects.exclude(type=Expense.Type.TAX_QUARTERLY).exclude(type=Expense.Type.TAX_ANNUAL)
    return expenses


def _get_income_total(start, end):
    aggregate = Invoice.objects. \
                filter(date_received__gte=start).filter(date_received__lt=end). \
                aggregate(Sum('amount'))
    return aggregate['amount__sum'] or 0


def _get_invoiced_total(start, end):
    aggregate = Invoice.objects. \
                filter(date_sent__gte=start).filter(date_sent__lt=end). \
                aggregate(Sum('amount'))
    return aggregate['amount__sum'] or 0


def _get_raw_total(expenses, start, end):
    aggregate = expenses.filter(date__gte=start).filter(date__lt=end).aggregate(Sum('amount'))
    return aggregate['amount__sum']

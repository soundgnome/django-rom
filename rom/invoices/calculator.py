from datetime import date
from django.db.models import Sum
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

    return totals


def _get_income_total(start, end):
    aggregate = Invoice.objects. \
                filter(date_received__gte=start).filter(date_received__lt=end). \
                aggregate(Sum('amount'))
    return aggregate['amount__sum']


def _get_invoiced_total(start, end):
    aggregate = Invoice.objects. \
                filter(date_sent__gte=start).filter(date_sent__lt=end). \
                aggregate(Sum('amount'))
    return aggregate['amount__sum']

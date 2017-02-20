from datetime import date
from decimal import Decimal
from django.test import TestCase
from .calculator import get_outstanding_invoices, get_monthly_totals
from .models import Client, Expense, Invoice


class CalculatorTestCase(TestCase):

    fixtures = (
        'invoices/fixtures/invoices_test.json',
    )

    def test_outstanding_invoices(self):

        invoices = get_outstanding_invoices(date(2017,2,1))
        self.assertEqual(invoices['total_balance'], 565.25)
        self.assertEqual(invoices['past_30_days'].count(), 1)
        self.assertEqual(invoices['past_30_days'].first().invoice_number, '345')


    def test_monthly_totals(self):

        totals = get_monthly_totals(2017, 1)
        self.assertEqual(totals['income'], Decimal('752.00'))
        self.assertEqual(totals['invoiced'], Decimal('682.50'))
        self.assertEqual(totals['expenses_before_tax'], Decimal('1525.92'))
        self.assertEqual(totals['total_expenses'], Decimal('4525.92'))
        self.assertEqual(totals['adjusted_expenses'], Decimal('2592.59'))


class InvoiceTestCase(TestCase):

    fixtures = (
        'invoices/fixtures/invoices_test.json',
    )

    def test_invoice_attributes(self):

        invoice = Invoice.objects.get(invoice_number='123')
        self.assertEqual(invoice.client.name, 'Roe Design')
        self.assertEqual(invoice.amount, 500)
        self.assertEqual(invoice.date_sent, date(2017,1,3))
        self.assertEqual(invoice.date_received, date(2017,1,19))
        self.assertEqual(invoice.payment_comment, 'check 9876')

        invoice = Invoice.objects.get(invoice_number='345')
        self.assertIsInstance(invoice.client, Client)
        self.assertEqual(invoice.amount, Decimal('382.75'))
        self.assertEqual(invoice.date_sent, date(2016,11,29))
        self.assertEqual(invoice.date_received, None)
        self.assertEqual(invoice.payment_comment, '')


class ExpenseTestCase(TestCase):

    fixtures = (
        'invoices/fixtures/invoices_test.json',
    )

    def test_expense_attributes(self):

        expense = Expense.objects.get(pk=1)
        self.assertEqual(expense.amount, Decimal('1325.92'))
        self.assertEqual(expense.date, date(2017,1,1))
        self.assertEqual(expense.type, Expense.Type.PERSONAL_MONTHLY)
        self.assertEqual(expense.month_span, 1)

        expense = Expense.objects.get(pk=2)
        self.assertEqual(expense.type, Expense.Type.BUSINESS_MONTHLY)
        self.assertEqual(expense.month_span, 1)

        expense = Expense.objects.get(pk=3)
        self.assertEqual(expense.type, Expense.Type.TAX_QUARTERLY)
        self.assertEqual(expense.month_span, 3)

        expense = Expense.objects.get(pk=4)
        self.assertEqual(expense.type, Expense.Type.TAX_ANNUAL)
        self.assertEqual(expense.month_span, 12)


    def test_month_span(self):

        expense = Expense.objects.get(pk=4)
        self.assertEqual(expense.type, Expense.Type.TAX_ANNUAL)
        self.assertEqual(expense.month_span, 12)

        expense.type = Expense.Type.PERSONAL_MONTHLY
        expense.save()
        self.assertEqual(expense.month_span, 1)

        expense.type = Expense.Type.TAX_QUARTERLY
        expense.save()
        self.assertEqual(expense.month_span, 3)

        expense.type = Expense.Type.BUSINESS_MONTHLY
        expense.save()
        self.assertEqual(expense.month_span, 1)

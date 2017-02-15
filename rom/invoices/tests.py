from datetime import date
from django.test import TestCase
from .models import Client, Expense, Invoice


class InvoiceTestCase(TestCase):

    def test_invoice_attributes(self):

        invoice= Invoice.objects.get(invoice_number='123')
        self.assertEqual(invoice.client.name, 'Roe Design')
        self.assertEqual(invoice.amount, 500)
        self.assertEqual(invoice.date_sent, date(2017,1,3))
        self.assertEqual(invoice.date_received, date(2017,1,19))
        self.assertEqual(invoice.payment_comment, 'check 9876')

        invoice= Invoice.objects.get(invoice_number='345')
        self.assertIsInstance(invoice.client, Client)
        self.assertEqual(invoice.amount, 382.75)
        self.assertEqual(invoice.date_sent, date(2016,11,29))
        self.assertEqual(invoice.date_received, None)
        self.assertEqual(invoice.payment_comment, '')


class ExpenseTestCase(TestCase):

    def test_expense_attributes(self):

        expense = Expense.objects.get(pk=1)
        self.assertEqual(expense.amount, 1325.92)
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

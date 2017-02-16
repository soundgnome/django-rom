from django.contrib import admin
from .models import Client, Expense, Invoice


class ExpenseAdmin(admin.ModelAdmin):
    fields = ('date', 'amount', 'type')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'amount', 'client', 'date_received')

admin.site.register(Client)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Invoice, InvoiceAdmin)

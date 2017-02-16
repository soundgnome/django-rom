from django.contrib import admin
from .models import Client, Expense, Invoice


class ExpenseAdmin(admin.ModelAdmin):
    fields = ('date', 'amount', 'type')

admin.site.register(Client)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Invoice)

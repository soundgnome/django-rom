from django.db import models
from enumfields import Enum, EnumIntegerField


class Client(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Invoice(models.Model):

    invoice_number = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    date_sent = models.DateField()
    date_received = models.DateField(blank=True, null=True)
    payment_comment = models.CharField(max_length=255, default='')

    def __str__(self):
        return 'Invoice %s' % self.invoice_number

    class Meta:
        ordering = ('date_sent',)


class Expense(models.Model):

    class Type(Enum):
        PERSONAL_MONTHLY = 0
        BUSINESS_MONTHLY = 1
        TAX_QUARTERLY = 2
        TAX_ANNUAL = 3

        class Labels:
            PERSONAL_MONTHLY = 'Personal'
            BUSINESS_MONTHLY = 'Business'
            TAX_QUARTERLY = 'Tax (quarterly)'
            TAX_ANNUAL = 'Tax (annual)'

    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    type = EnumIntegerField(Type)
    month_span = models.IntegerField(default=1)

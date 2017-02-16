# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-02-15 23:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import invoices.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('type', enumfields.fields.EnumIntegerField(enum=invoices.models.Expense.Type)),
                ('month_span', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_sent', models.DateField()),
                ('date_received', models.DateField(blank=True, null=True)),
                ('payment_comment', models.CharField(default='', max_length=255)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='invoices.Client')),
            ],
            options={
                'ordering': ('date_sent',),
            },
        ),
    ]
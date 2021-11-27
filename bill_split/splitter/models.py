from decimal import Decimal
from djmoney.models.fields import MoneyField
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    # Note for self: no need for one2many will do person.billlines_set.all() or something similar


class BillLineSection(models.Model):
    # Sections for each type of sections in the lines  aka Appetizers, Main, Drinks, etc.
    # amt is total everyone paid for in that section, regardless of groups

    name = models.CharField(max_length=200)
    total_section_amount = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')
    # TODO: add checks that total will add up to complete total in the end


class BillLines(models.Model):
    # many2one for person responsible for bill, each line is linked to only one person
    owing_person = models.ForeignKey(Person, on_delete=models.CASCADE)

    owe_amount = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # TODO: create a link to group either m2o or m2m

    # TODO: create link to bill line sections m2m?


class Bill(models.Model):
    pre_tax_total = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')
    total_cost = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')
    tax = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # TODO: make calculated field
    tax_percent = MoneyField(max_digits=6, decimal_places=2, default=0, default_currency='USD')

    # def _get_tax_percent(self):
    #     "Returns tax percent via total cost and tax"
    #     return self.total_cost - self.tax

    # person who paid for bill
    paying_person = models.ForeignKey(Person, on_delete=models.CASCADE)

    bill_sections = models.ManyToManyField(BillLineSection)


class BillGroup(models.Model):
    name = models.CharField(max_length=200, default='')

    # if the bill group has a parent group, might be NULL
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    # total amount group paid
    total_group_amount = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # TODO: need to figure how we split by sections as well, since certain groups may pay different amounts
    #       per section, ex: veggie eater apps vs meat apps, veggie main vs meat main, or even solo eaters or
    #       different groups






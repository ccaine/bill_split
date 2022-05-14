from decimal import Decimal
from djmoney.models.fields import MoneyField
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    # Note for self: no need for one2many will do person.billlines_set.all() or something similar


class BillLineSection(models.Model):
    # The "Column" of the table
    # Sections for each type of sections in the lines aka Appetizers, Main, Drinks, etc.
    # amt is total everyone paid for in that section, regardless of groups

    name = models.CharField(max_length=200)
    total_section_amount = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # TODO: check if we need this type field or we just auto create these types of sections by
    #  default and therefore will not need the type
    # Type = Custom, tip, tax, total value column
    # section_type = models.CharField()
    # TODO: add checks that total will add up to complete total in the end


class BillLines(models.Model):
    # The "Row" of the table
    # many2one for person responsible for bill, each line is linked to only one person
    owing_person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # this is the sum amount of the values in all the cells
    owe_amount = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # TODO: create a link to group either m2o or m2m

    # TODO: create link to bill line sections m2m?


class Bill(models.Model):
    # The "Table"
    sub_total = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    total_tip = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')
    total_cost = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    tax = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # TODO: make calculated field
    tax_percent = MoneyField(max_digits=6, decimal_places=2, default=0, default_currency='USD')

    # def _get_tax_percent(self):
    #     "Returns tax percent via total cost and tax"
    #     return self.total_cost - self.tax

    # person who paid for bill
    paying_person = models.ForeignKey(Person, on_delete=models.CASCADE)

    # bill_sections = models.ManyToManyField(BillLineSection)

    # Each Bill has multiple Lines > Which is done per person
    bill_lines = models.ManyToManyField(BillLines)


class BillGroup(models.Model):
    # The group of "Cells" of the table

    name = models.CharField(max_length=200, default='')

    # if the bill group has a parent group, might be NULL
    # parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)

    # total amount group paid
    total_group_amount = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='USD')

    # Reference to One BillLineSection
    # TODO: fix the null and check here if we need to create default data since we need to
    #  reference at least one bill section
    # bill_section = models.ForeignKey(BillLineSection, on_delete=models.CASCADE)
    # Reference to multiple BillLine(Person)
    bill_lines = models.ManyToManyField(BillLines)

    # TODO: need to figure how we split by sections as well, since certain groups may pay different amounts
    #       per section, ex: veggie eater apps vs meat apps, veggie main vs meat main, or even solo eaters or
    #       different groups


"""

Bill
Bill Line
Section
Group
Person

There is one Bill
    There is one person responsible for original Bill
    There is a Sub-Total
    There is a Tip amount
    There is a Tax
    There is a Final Total
    There is a Tax Percent
    
There are multiple People(lines) that need to split the Bill into Bill Lines(ROW)
    Each Bill Line is associated with one Person
    Each Bill Line has a percent tax, tip, and owe
    Owe on the Bill Line is the final amount that person owes
There are different Sections to the Bill(COLUMN) > This includes Tax, Tip, Owe amount
    The Bill Line Person can be included or not included in that Section (ex: They did not have drinks or apps)
    A group can have only 1 person
Each Section(COLUMN) can be split into Sub-Groups(CELL). 
    How to add a Group
    Button on Section > "Add Group" > Click
    Add multiple "people" > lines
    Add total for group
    Click Okay
    
    Clicking the cell for that bill Line will edit the Group
    Each cell shows the amount Total divided by the number of people in the Group


"""


from django.contrib import admin

# Register your models here.

from .models import Bill, BillLines, Person, BillLineSection, BillGroup

admin.site.register(Bill)
admin.site.register(BillLines)
admin.site.register(Person)
admin.site.register(BillGroup)
admin.site.register(BillLineSection)
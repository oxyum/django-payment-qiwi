from django.contrib import admin
from qiwi.models import Bill

class BillAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ['id', 'user', 'amount', 'phone', 'created_on', 'soap_code']
    list_filter = ['created_on']
    ordering = ['-created_on']
    search_fields = ['id', 'user', 'phone']

admin.site.register(Bill, BillAdmin)

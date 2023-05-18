from django.contrib import admin

from .models import Site_admin, Transaction, Test, Detail_canceled, Notification, Invoice
# Register your models here.

admin.site.register(Site_admin)
admin.site.register(Transaction)
admin.site.register(Test)
admin.site.register(Detail_canceled)
admin.site.register(Notification)
admin.site.register(Invoice)

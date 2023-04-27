from django.contrib import admin

from .models import Site_admin, Transaction, Test, Detail_canceled
# Register your models here.

admin.site.register(Site_admin)
admin.site.register(Transaction)
admin.site.register(Test)
admin.site.register(Detail_canceled)

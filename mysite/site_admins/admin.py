from django.contrib import admin

from .models import Site_admin, Transaction
# Register your models here.

admin.site.register(Site_admin)
admin.site.register(Transaction)
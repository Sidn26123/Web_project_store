from django.contrib import admin

from .models import Doctor, Specialties
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialties)
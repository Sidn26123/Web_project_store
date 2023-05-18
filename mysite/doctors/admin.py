from django.contrib import admin

from .models import Doctor, Specialties, MyPaient
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialties)
admin.site.register(MyPaient)
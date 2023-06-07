from django.contrib import admin
from .models import User

# admin.site.register(User)
# #Register your models here.

# #code đặt khám chuyên khoa  thông tin bác sĩ



#code đặt khám 
from .models import Patient

admin.site.register(Patient)

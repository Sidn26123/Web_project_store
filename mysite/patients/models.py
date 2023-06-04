
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from users.models import User
from datetime import date, datetime

#code bên đăng ký
# Create your models here.
from django.db import models

#code lấy thông tin xuất ra
from django.shortcuts import render

def thongtin(request):
    user = User.objects.all()
    return render(request, 'app/thongtin.html', {'user': user})

class Patient(User):
    blood_group = models.CharField(max_length = 5, default = None)
    
@receiver(pre_save, sender = Patient)
def calculate_age(sender, instance, **kwargs):
    today = datetime.today()
    age = today.year - instance.date_of_birth.year - ((today.month, today.day) < (instance.date_of_birth.month, instance.date_of_birth.day))
    instance.new_age = age
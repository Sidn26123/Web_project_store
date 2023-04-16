from django.db import models
from django.contrib.auth.backends import ModelBackend
from users.models import User
from doctors.models import Doctor, Specialties
from patients.models import Patient
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
# Create your models here.

class Site_admin(User):

    def save(self, *args, **kwargs):

        # self.date_of_birth = dob_formatted
    #super để kế thừa save lại các phần đã có trước đó
        super().save(*args, **kwargs)

#Set value mặc định cho trường inherited
# class Site_admin_web(Site_admin):
#     ad = models.ForeignKey(Site_admin, on_delete=models.CASCADE)
#     is_admin = models.BooleanField(default = True)

#     def __str__(self):
#         return self.is_admin

class Transaction(models.Model):
    appointment_state = [
        ("success", "Thành công"),
        ("failure", "Thất bại"),
        ("confirming", "Đang chờ"),
        
    ]
    medical_specialties = [
        ("nha_khoa", "Nha khoa (răng hàm mặt)"),
        ("tim_mach", "Tim mạch"),
        ("da_lieu", "Da liễu"),
        ("mat", "Mắt"),
        ("xuong_khop", "Xương khớp"),
    ]
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount_transact = models.IntegerField()
    note = models.TextField(null= True, blank = True)
    medical_specialty = models.ForeignKey(Specialties, on_delete= models.CASCADE)
    appoint_time = models.DateTimeField(auto_now= False)
    state = models.CharField(max_length = 20, choices=appointment_state)
    email = models.EmailField(null = True, blank = True)
    id_transaction = models.IntegerField(default = 1)
    def __str__(self):
        return f"{self.doctor}-{self.patient}"

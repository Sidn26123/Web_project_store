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
        ("waiting", "Đang chờ"),
        ("pending", "Đang chờ xác nhận"),
        
    ]
    medical_specialties = [
        ("nha_khoa", "Nha khoa"),
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
    medical_specialty = models.ForeignKey(Specialties, on_delete= models.CASCADE,  default='nha_khoa')
    appoint_time = models.DateTimeField(auto_now_add=True)
    complete_time = models.DateTimeField(auto_now= False, null = True, blank = True)
    state = models.CharField(max_length = 20, choices=appointment_state)
    email = models.EmailField(null = True, blank = True)
    id_transaction = models.IntegerField(default = 1)
    canceled_details = models.OneToOneField('Detail_canceled', on_delete=models.CASCADE, null = True, blank = True)
    appoint_address = models.TextField(default = "")
    def __str__(self):
        return f"{self.doctor.real_name}-{self.patient.real_name}"
    def __save__(self, *args, **kwargs):
        self.medical_specialty.name = self.specialties
        super().save(*args, **kwargs)
class Detail_canceled(models.Model):
    canceler_choices = [
        ('doctor', 'Bác sĩ'),
        ('patient', 'Bệnh nhân'),
        ('admin', 'Admin')
    ]
    id_transaction = models.CharField(max_length=50, default=None, blank = True, null = True)
    reason = models.TextField(blank = True, null = True)
    canceler = models.CharField(max_length = 20, choices = canceler_choices, default = 'patient')
    time_cancel = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id_transaction
    def __save__(self, *args, **kwargs):
        if (args[0]):
            self.canceler = args[0]
        super().save(*args, **kwargs)

class Test(models.Model):
    name = models.CharField(max_length = 100, default= None)
    age = models.IntegerField(default= 1)
    def __str__(self):
        return self.name


class Notification(models.Model):
    content = models.TextField()
    receiver_id = models.IntegerField(null = True)
    time_notice = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default = False)
    def __str__(self):
        return self.id
    
class Invoice(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount_transact = models.IntegerField()
    medical_specialty = models.ForeignKey(Specialties, on_delete= models.CASCADE,  default='nha_khoa')
    appoint_time = models.DateTimeField(auto_now= False)
    complete_time = models.DateTimeField(auto_now= False, null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    id_transaction = models.IntegerField(default = 1)
    canceled_details = models.OneToOneField('Detail_canceled', on_delete=models.CASCADE, null = True, blank = True)
    
    def __str__(self):
        return f"{self.doctor.real_name}-{self.patient.real_name}"
    def __save__(self, *args, **kwargs):
        self.medical_specialty.name = self.specialties
        super().save(*args, **kwargs)

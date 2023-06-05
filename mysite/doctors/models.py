from django.db import models
from django.conf import settings
import os
from users.models import User
from patients.models import Patient
from django.dispatch import receiver
from django.db.models.signals import pre_save
from datetime import date, datetime
from django.utils.timezone import now
# Create your models here.
class Doctor(User):
    position = models.CharField(max_length=255, null = True, blank = True)
    specialty = models.ForeignKey('Specialties', on_delete=models.CASCADE, default = 'nha_khoa')
    income = models.IntegerField(default = 0)
    money_left = models.IntegerField(default = 0)
    fee = models.IntegerField(default = 0)
    is_auth = models.BooleanField(default = False)
    available_time = models.TextField(default = "[]")
    time_per_appoint = models.IntegerField(default = 30)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
@receiver(pre_save, sender = Doctor)
def calculate_age(sender, instance, **kwargs):
    today = datetime.today()
    age = today.year - instance.date_of_birth.year - ((today.month, today.day) < (instance.date_of_birth.month, instance.date_of_birth.day))
    instance.new_age = age
class Specialties(models.Model):
    medical_specialties = [
        ("nha_khoa", "Nha khoa"),
        ("tim_mach", "Tim mạch"),
        ("da_lieu", "Da liễu"),
        ("mat", "Mắt"),
        ("xuong_khop", "Xương khớp"),
    ]
    name = models.CharField(max_length=255, choices = medical_specialties, default= "nha_khoa",  primary_key=True)
    description = models.TextField()
    avatar = models.FileField(upload_to = os.path.join(settings.MEDIA_ROOT, 'images'),default = os.path.join(settings.MEDIA_URL,"images/default.jpeg"), max_length=255)
    
    def __str__(self):
        return self.get_name_display()
class Review(models.Model):
    rate = models.FloatField()
    feedback = models.TextField()
    receiver_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, null = False, default= 1)
    sender_id = models.ForeignKey(Patient, on_delete=models.CASCADE, null = False, default = 1)
    time_feedback = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if len(self.feedback) <= 20:
            return self.feedback
        else:
            return self.feedback[:20] + "..."
    
class MyPaient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    last_time = models.DateTimeField(default= now, null = True)
    counter = models.IntegerField(default = 1)
    def __str__(self):
        return f"{self.doctor.real_name}-{self.patient.real_name}"
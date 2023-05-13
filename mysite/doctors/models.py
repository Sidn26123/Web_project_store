from django.db import models

from users.models import User
# Create your models here.
class Doctor(User):
    position = models.CharField(max_length=255, null = True, blank = True)
    specialty = models.ForeignKey('Specialties', on_delete=models.CASCADE, default = 'nha_khoa')
    rate = models.FloatField(default = 0)
    income = models.IntegerField(default = 0)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
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
    picture = models.FileField()
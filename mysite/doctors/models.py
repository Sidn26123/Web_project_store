from django.db import models

from users.models import User
# Create your models here.
class Doctor(User):
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        
class Specialties(models.Model):
    medical_specialties = [
        ("nha_khoa", "Nha khoa (răng hàm mặt)"),
        ("tim_mach", "Tim mạch"),
        ("da_lieu", "Da liễu"),
        ("mat", "Mắt"),
        ("xuong_khop", "Xương khớp"),
    ]
    name = models.CharField(max_length=255, choices = medical_specialties, default= "nha_khoa",  primary_key=True)
    description = models.TextField()
    picture = models.FileField()
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from users.models import User
from datetime import date, datetime
# Create your models here.

class Patient(User):
    blood_group = models.CharField(max_length = 5, default = None)
    
@receiver(pre_save, sender = Patient)
def calculate_age(sender, instance, **kwargs):
    today = datetime.today()
    age = today.year - instance.date_of_birth.year - ((today.month, today.day) < (instance.date_of_birth.month, instance.date_of_birth.day))
    instance.new_age = age
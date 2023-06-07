from django.contrib.auth.backends import ModelBackend
from doctors.models import Doctor
from users.models import User
class MyCustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            doctor = Doctor.objects.get(username=username)
        except Doctor.DoesNotExist:
            return None
        if password == doctor.password:
            return doctor
        
        return None

    def get_user(self, user_id):
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            return None
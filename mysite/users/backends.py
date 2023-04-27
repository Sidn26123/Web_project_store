from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.backends import ModelBackend

from site_admins.models import Site_admin

#Vì không sử dụng class User mặc định của django
#Nên cần định nghĩa lại ModelBackEnd để xác định login đúng ý 
class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Site_admin.objects.get(username=username)
            if (password == user.password):
                return user
        except Site_admin.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Site_admin.objects.get(pk=user_id)
        except Site_admin.DoesNotExist:
            return None
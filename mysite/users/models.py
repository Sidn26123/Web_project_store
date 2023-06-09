from django.db import models

from django.contrib.auth.models import AbstractUser

from datetime import datetime,date
from django.conf import settings
import os
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from django.contrib.auth.backends import ModelBackend
# Create your models here.
class User(AbstractUser):
    MAN = "man"
    WOMAN = "woman"
    THEM = "undefined"
    GENDER_CHOICES = [
        (MAN, "Nam"),
        (WOMAN, "Nữ"),
        (THEM, "Không xác định"),
    ]

    PROVINCE_CHOICES = [
        ('ho_chi_minh', 'TP. Hồ Chí Minh'),
        ('ha_noi', 'Hà Nội'),
        ('da_nang', 'Đà Nẵng'),
        ('hai_phong', 'Hải Phòng'),
        ('can_tho', 'Cần Thơ'),
        ('cao_bang','Cao Bằng'),
        ('an_giang', 'An Giang'),
        ('bac_giang', 'Bắc Giang'),
        ('bac_kan', 'Bắc Kạn'),
        ('bac_lieu', 'Bạc Liêu'),
        ('bac_ninh', 'Bắc Ninh'),
        ('ben_tre', 'Bến Tre'),
        ('binh_dinh', 'Bình Định'),
        ('binh_duong', 'Bình Dương'),
        ('binh_phuoc', 'Bình Phước'),
        ('binh_thuan', 'Bình Thuận'),
        ('ca_mau', 'Cà Mau'),
        ('cao_bang', 'Cao Bằng'),
        ('dak_lak', 'Đắk Lắk'),
        ('dak_nong', 'Đắk Nông'),
        ('dien_bien', 'Điện Biên'),
        ('dong_nai', 'Đồng Nai'),
        ('dong_thap', 'Đồng Tháp'),
        ('gia_lai', 'Gia Lai'),
        ('ha_giang', 'Hà Giang'),
        ('ha_nam', 'Hà Nam'),
        ('ha_tinh', 'Hà Tĩnh'),
        ('hai_duong', 'Hải Dương'),
        ('hau_giang', 'Hậu Giang'),
        ('hoa_binh', 'Hòa Bình'),
        ('hung_yen', 'Hưng Yên'),
        ('khanh_hoa', 'Khánh Hòa'),
        ('kien_giang', 'Kiên Giang'),
        ('kon_tum', 'Kon Tum'),
        ('lai_chau', 'Lai Châu'),
        ('lam_dong', 'Lâm Đồng'),
        ('lang_son', 'Lạng Sơn'),
        ('lao_cai', 'Lào Cai'),
        ('long_an', 'Long An'),
        ('nam_dinh', 'Nam Định'),
        ('nghe_an', 'Nghệ An'),
        ('ninh_binh', 'Ninh Bình'),
        ('ninh_thuan', 'Ninh Thuận'),
        ('phu_tho', 'Phú Thọ'),
        ('quang_binh', 'Quảng Bình'),
        ('quang_nam', 'Quảng Nam'),
        ('quang_ngai', 'Quảng Ngãi'),
        ('quang_ninh', 'Quảng Ninh'),
        ('quang_tri', 'Quảng Trị'),
        ('soc_trang', 'Sóc Trăng'),
        ('son_la', 'Sơn La'),
        ('tay_ninh', 'Tây Ninh'),
        ('thai_binh', 'Thái Bình'),
        ('thai_nguyen', 'Thái Nguyên'),
        ('thanh_hoa', 'Thanh Hóa'),
        ('thua_thien_hue', 'Thừa Thiên Huế'),
        ('tien_giang', 'Tiền Giang'),
        ('tra_vinh', 'Trà Vinh'),
        ('tuyen_quang', 'Tuyên Quang'),
        ('vinh_long', 'Vĩnh Long'),
        ('vinh_phuc', 'Vĩnh Phúc'),
        ('yen_bai', 'Yên Bái')
    ]
    real_name = models.CharField(max_length=255, verbose_name="Tên", null = True)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES, default = THEM)
    phone = models.CharField(max_length = 15, default = None, null = True, blank = True, unique= True)
    citizen_identification = models.CharField(max_length = 20, null = True, unique=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null =True)
    avatar = models.FileField(upload_to = os.path.join(settings.MEDIA_ROOT, 'images'),default = os.path.join(settings.MEDIA_URL,"images/default.jpeg"), max_length=255)
    is_admin = models.BooleanField(default = False)
    province = models.CharField(max_length = 20, choices= PROVINCE_CHOICES, default="ha_noi") 
    new_age = models.IntegerField(null = True,blank = True)
    address = models.TextField(null = True)
    account_left = models.FloatField(default = 0)
    credit_score = models.IntegerField(default = 100)
    time_join = models.DateTimeField(auto_now = True)
    email = models.EmailField(null = True, blank = True)
@receiver(pre_save, sender = User)
def calculate_age(sender, instance, **kwargs):
    today = date.today()
    if (instance.date_of_birth):
        age = today.year - instance.date_of_birth.year - ((today.month, today.day) < (instance.date_of_birth.month, instance.date_of_birth.day))
        instance.new_age = age
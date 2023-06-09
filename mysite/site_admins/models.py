from django.db import models
from django.contrib.auth.backends import ModelBackend
from users.models import User
from doctors.models import Doctor, Specialties
from patients.models import Patient
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
from django.utils.timezone import now
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
    appointment_state = [
        ("success", "Thành công"),
        ("failure", "Thất bại"),
        ("waiting", "Đang chờ"),
        ("pending", "Đang chờ xác nhận"),
        ("denied", "Đã từ chối"),
        ("appointing", "Đang khám"),
        
    ]
    medical_specialties = [
        ("xuong_khop", "Xương khớp"),
        ("than_kinh", "Thần Kinh"),
        ("tieu_hoa", "Tiêu Hóa"),
        ("tim_mach", "Tim mạch"),
        ("tai_mui_hong", "Tai Mũi Họng"),
        ("cot_song", "Cột Sống"),
        ("da_lieu", "Da Liễu"),
        ("ho_hap_phoi", "Hô Hấp - Phổi"),
        ("nha_khoa", "Nha khoa"),
    ]
    CREATOR = [
        ("doctor", "Bác sĩ"),
        ("patient", "Bệnh nhân"),
        ("admin", "Admin"),
        ("system", "Hệ thống"),
    ]

    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null = True, blank = True)
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount_transact = models.IntegerField()
    note = models.TextField(null= True, blank = True)
    medical_specialty = models.ForeignKey(Specialties, on_delete= models.CASCADE,  default='nha_khoa')
    appoint_time = models.DateTimeField(null = True, blank = True)
    complete_time = models.DateTimeField(auto_now= False, null = True, blank = True)
    state = models.CharField(max_length = 20, choices=appointment_state)
    email = models.EmailField(null = True, blank = True)
    id_transaction = models.IntegerField(default = 1)
    canceled_details = models.OneToOneField('Detail_canceled', on_delete=models.CASCADE, null = True, blank = True)
    appoint_address = models.TextField(default = "")
    creator = models.CharField(max_length = 20, default = "doctor", choices = CREATOR)
    info_patient = models.CharField(max_length = 30, null = True, blank = True)
    city = models.CharField(max_length = 30, null = True, blank = True)
    district = models.CharField(max_length = 30, null = True, blank = True)
    address = models.TextField(null = True, blank = True)



    real_name = models.CharField(max_length=255, verbose_name="Tên", null = True)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES, default = THEM)
    phone = models.CharField(max_length = 15, default = None, null = True, blank = True)
    citizen_identification = models.CharField(max_length = 20, null = True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null =True)
    province = models.CharField(max_length = 20, choices= PROVINCE_CHOICES, default="ha_noi") 
    def __str__(self):
        return f"{self.doctor.real_name}-{self.id}"
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
    title = models.TextField(null = True, blank = True)
    content = models.TextField(null = True, blank = True)
    receiver = models.CharField(max_length = 20, default = "doc,", null = True, blank = True)
    sender = models.CharField(max_length = 20, default = "ptn,", null = True, blank = True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_notice = models.DateTimeField(auto_now_add=False, null = True, default = None, blank = True)
    is_read = models.BooleanField(default = False)
    def __str__(self):
        return str(self.id)
    
class Invoice(models.Model):
    STATE = [
        ("success", "Thành công"),
        ("refund", "Hoàn tiền"),
    ]

    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount_transact = models.IntegerField()
    medical_specialty = models.ForeignKey(Specialties, on_delete= models.CASCADE,  default='nha_khoa')
    appoint_time = models.DateTimeField(auto_now= False)
    appoint_address = models.TextField(default = "")
    complete_time = models.DateTimeField(auto_now= False, null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    id_transaction = models.IntegerField(default = 1)
    canceled_details = models.OneToOneField('Detail_canceled', on_delete=models.CASCADE, null = True, blank = True)
    status = models.CharField(max_length = 20, default = "success", choices = STATE)
    show_on_doctor = models.BooleanField(default = True)
    show_on_patient = models.BooleanField(default = True)
    show_on_admin = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.doctor.real_name}-{self.patient.real_name}"
    def __save__(self, *args, **kwargs):
        self.medical_specialty.name = self.specialties
        super().save(*args, **kwargs)

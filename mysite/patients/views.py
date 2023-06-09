from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient
from site_admins.models import Site_admin, Transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
#from patients.models import Patient
#from .models import Site_admin, Transaction
#from doctors.models import Doctor
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from math import ceil
#from .forms import Login_form
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
#from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
import json
import calendar
import csv
import os
import re

from math import floor, ceil
from django.forms.models import model_to_dict

# Create your views here.
def home(request):
    context= {}
    return render(request, 'app/home.html',context)
def lienhe(request):
    context= {}
    return render(request, 'app/lienhe.html',context)
def lienhe1(request):
    context= {}
    return render(request, 'app/lienhe1.html',context)
def hdsd(request):
    context= {}
    return render(request, 'app/hdsd.html',context)
def hdsd1(request):
    context= {}
    return render(request, 'app/hdsd1.html',context)
def dangky(request):
    context= {}
    return render(request, 'app/register.html',context)
def dangnhap(request):
    context= {}
    return render(request, 'app/logindedatkham.html',context)
def tintuc(request):
    context= {}
    return render(request, 'app/tintuc.html',context)
def tintuc1(request):
    context= {}
    return render(request, 'app/tintuc1.html',context)
def thongbao(request):
    context= {}
    return render(request, 'app/thongbao.html',context)
def thongbao1(request):
    context= {}
    return render(request, 'app/thongbao1.html',context)
def chuyenkhoa(request):
    context= {}
    return render(request, 'app/chuyenkhoa.html',context)
def chuyenkhoa1(request):
    context= {}
    return render(request, 'app/chuyenkhoa1.html',context)
def home1(request):
    context= {}
    return render(request, 'app/home1.html',context)
def khieunai(request):
    context= {}
    return render(request, 'app/khieunai.html',context)
def khieunai1(request):
    context= {}
    return render(request, 'app/khieunai1.html',context)
def thongtin(request):
    context= {}
    return render(request, 'app/thongtin.html',context)
def chaomung(request):
    context= {}
    return render(request, 'app/chaomung.html',context)

#chuyên khoa
def xuongkhop(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "xuong_khop")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/xuongkhop.html',context)
def xuongkhop1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "xuong_khop")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/xuongkhop1.html',context)
def thankinh(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "than_kinh")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/thankinh.html',context)
def thankinh1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "than_kinh")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/thankinh1.html',context)
def tieuhoa(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tieu_hoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/tieuhoa.html',context)
def tieuhoa1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tieu_hoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/tieuhoa1.html',context)
def timmach(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tim_mach")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/timmach.html',context)
def timmach1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tim_mach")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/timmach1.html',context)
def taimuihong(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tai_mui_hong")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/taimuihong.html',context)
def taimuihong1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tai_mui_hong")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/taimuihong1.html',context)
def cotsong(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "cot_song")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/cotsong.html',context)
def cotsong1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "cot_song")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/cotsong1.html',context)
def dalieu(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "da_lieu")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/dalieu.html',context)
def dalieu1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "da_lieu")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/dalieu1.html',context)
def hohap(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "ho_hap")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/hohap.html',context)
def hohap1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "ho_hap")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/hohap1.html',context)
def nhakhoa(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "nha_khoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/nhakhoa.html',context)
def nhakhoa1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "nha_khoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CK/nhakhoa1.html',context)

#chuyên khoa đặt khám
def xuongkhopdk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "xuong_khop")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/xuongkhopdk.html',context)
def xuongkhopdk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "xuong_khop")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/xuongkhopdk1.html',context)
def thankinhdk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "than_kinh")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/thankinhdk.html',context)
def thankinhdk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "than_kinh")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/thankinhdk1.html',context)
def tieuhoadk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tieu_hoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/tieuhoadk.html',context)
def tieuhoadk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tieu_hoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/tieuhoadk1.html',context)
def timmachdk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tim_mach")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/timmach.html',context)
def timmachdk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tim_mach")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/timmach1.html',context)
def taimuihongdk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tai_mui_hong")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/taimuihong.html',context)
def taimuihongdk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tai_mui_hong")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/taimuihong1.html',context)
def cotsongdk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "cot_song")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/cotsong.html',context)
def cotsongdk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "cot_song")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/cotsong1.html',context)
def dalieudk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "da_lieu")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/dalieu.html',context)
def dalieudk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "da_lieu")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/dalieu1.html',context)
def hohapdk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "ho_hap")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/hohap.html',context)
def hohapdk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "ho_hap")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/hohap1.html',context)
def nhakhoadk(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "nha_khoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/nhakhoa.html',context)
def nhakhoadk1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "nha_khoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKdatkham/nhakhoa1.html',context)

#Code 5 chuyên khoa  trang home 
def xuongkhophome(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "xuong_khop")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/xuongkhophome.html',context)
def xuongkhophome1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "xuong_khop")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/xuongkhophome1.html',context)
def thankinhhome(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "than_kinh")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/thankinhhome.html',context)
def thankinhhome1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "than_kinh")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/thankinhhome1.html',context)
def tieuhoahome(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tieu_hoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/tieuhoahome.html',context)
def tieuhoahome1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tieu_hoa")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/tieuhoahome1.html',context)
def timmachhome(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tim_mach")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/timmachhome.html',context)
def timmachhome1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tim_mach")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/timmachhome1.html',context)
def taimuihonghome(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tai_mui_hong")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/taimuihonghome.html',context)
def taimuihonghome1(request):
    print("a")
    doctor = Doctor.objects.filter(specialty = "tai_mui_hong")
    print(doctor)
    context= {
        'doc': doctor,
    }
    return render(request, 'CKhome/taimuihonghome1.html',context)




#bác sĩ 
def BsXuongkhop1(request):
    context= {}
    return render(request, 'doctor/BsXuongkhop1.html',context)
def BsXuongkhop2(request):
    context= {}
    return render(request, 'doctor/BsXuongkhop2.html',context)
def BsThankinh1(request):
    context= {}
    return render(request, 'doctor/BsThankinh1.html',context)
def BsThankinh2(request):
    context= {}
    return render(request, 'doctor/BsThankinh2.html',context)
def BsTieuhoa1(request):
    context= {}
    return render(request, 'doctor/BsTieuhoa1.html',context)
def BsTieuhoa2(request):
    context= {}
    return render(request, 'doctor/BsTieuhoa2.html',context)
def BsTimmach1(request):
    context= {}
    return render(request, 'doctor/BsTimmach1.html',context)
def BsTimmach2(request):
    context= {}
    return render(request, 'doctor/BsTimmach2.html',context)
def BsTaimuihong1(request):
    context= {}
    return render(request, 'doctor/BsTaimuihong1.html',context)
def BsTaimuihong2(request):
    context= {}
    return render(request, 'doctor/BsTaimuihong2.html',context)
def BsCotsong1(request):
    context= {}
    return render(request, 'doctor/BsCotsong1.html',context)
def BsCotsong2(request):
    context= {}
    return render(request, 'doctor/BsCotsong2.html',context)
def BsDalieu1(request):
    context= {}
    return render(request, 'doctor/BsDalieu1.html',context)
def BsDalieu2(request):
    context= {}
    return render(request, 'doctor/BsDalieu2.html',context)
def BsHohapphoi1(request):
    context= {}
    return render(request, 'doctor/BsHohapphoi1.html',context)
def BsHohapphoi2(request):
    context= {}
    return render(request, 'doctor/BsHohapphoi2.html',context)
def BsNhakhoa1(request):
    context= {}
    return render(request, 'doctor/BsNhakhoa1.html',context)
def BsNhakhoa2(request):
    context= {}
    return render(request, 'doctor/BsNhakhoa2.html',context)

#code xuất thông tin bác sĩ
def thongtinBS(request, id):
    doc = Doctor.objects.get(id = id)
    print(doc)
    context= {'data': doc}
    return render(request, 'patients/thongtinBS.html',context)
#đăng nhập để đặt khám
def logindedatkham(request):
    context= {}
    return render(request, 'app/logindedatkham.html',context)
#code phần đặt khám
def datkham(request):
    context= {}
    return render(request, 'patients/datkham.html',context)
def datkham1(request):
    context= {}
    return render(request, 'patients/datkham1.html',context)

def datkhamid(request, id, time):
    doctor = Doctor.objects.get(id = id)
    doctor_dict = model_to_dict(doctor)
    doctor_dict['avatar'] = doctor.avatar.url
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'patients/success.html')
    else:
        form = PatientForm()
    context = {
        'doctor': doctor_dict,
        'doc': doctor,
        'time': time,
        'avatar': doctor.avatar.url,
        'fee': doctor.fee,
        'form': form,
    }
    return render(request, 'patients/book_appointment1.html', context)
def book_appointment(request):
    context= {}
    return render(request, 'patients/book_appointment.html',context)
def success(request):
    context= {}
    return render(request, 'patients/success.html',context)
from django.shortcuts import render, redirect
from .forms import RegistrationForm
#code đăng ký
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Gán password và lưu User vào database
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('patient:user_login')
    else:
        form = RegistrationForm()

    return render(request, 'app/register.html', {'form': form})



#code đăng nhập
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, LoginDoctorForm, LoginPatientForm

def user_login(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        instance = request.POST.get('instance')
        if instance == 'patient':
            form = LoginPatientForm(request=request, data=request.POST)
        elif instance == 'doctor':
            form = LoginDoctorForm(request=request, data=request.POST)
        if form.is_valid():
            # Lấy thông tin đăng nhập từ form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Xác thực thông tin đăng nhập
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Thực hiện đăng nhập cho user
                    login(request,user)
                    if instance == "patient":
                        return redirect('patient:home1')
                    elif instance == "doctor":
                        return redirect('doctor:dashboard')
    else:
        form = LoginForm()

    return render(request, 'app/user_login.html', {'form': form})
#from django.shortcuts import render
#from .models import User
#def thongtin(request):
 #   user = User.objects.all()
 #   return render(request, 'app/thongtin.html', {'user': user})


#code đổi mật khẩu
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ChangePasswordForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            regex = r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[.\@#$!%*#?&]).*$'

            # Kiểm tra mật khẩu cũ có đúng không
            if not request.user.check_password(old_password):
                messages.error(request, 'Mật khẩu cũ không đúng')
                return redirect('patient:change_password')
            
            # Kiểm tra mật khẩu mới và xác nhận mật khẩu
            if new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới không khớp')
                return redirect('patient:change_password')
            if not re.match(regex, new_password):
                messages.error(request, 'Mật khẩu phải chứa ít nhất 1 chữ in hoa, 1 chữ thường, không dấu, 1 ký tự đặc biệt và 1 số')
                return redirect('patient:change_password')
            # Cập nhật mật khẩu mới
            request.user.set_password(new_password)
            request.user.save()
            
            messages.success(request, 'Mật khẩu đã được thay đổi thành công')
            return redirect('patient:user_login')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'app/change_password.html', {'form': form})

#code phần đặt khám thông tin bác sĩ
from django.shortcuts import render
from .forms import PatientForm

def book_appointment1(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'patients/success.html')
    else:
        form = PatientForm()
    return render(request, 'patients/book_appointment1.html', {'form': form, 'request':request})


#code tìm kiếm bác sĩ
from django.shortcuts import render
from .forms import DoctorSearchForm
from doctors.models import Doctor

def home(request):
    form = DoctorSearchForm(request.GET or None)
    results = []

    if request.method == 'GET' and form.is_valid():
        keyword = form.cleaned_data['search_keyword']
        results = Doctor.objects.filter(real_name__icontains=keyword)

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'app/home.html', context)
#code tìm kiếm bác sĩ home1
from django.shortcuts import render
from .forms import DoctorSearchForm
from doctors.models import Doctor

def home1(request):
    form = DoctorSearchForm(request.GET or None)
    results = []

    if request.method == 'GET' and form.is_valid():
        keyword = form.cleaned_data['search_keyword']
        results = Doctor.objects.filter(real_name__icontains=keyword)

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'app/home1.html', context)


def get_time_available(request):
    id = request.GET.get('id')
    doctor = Doctor.objects.get(id=id)
    available_time = doctor.available_time
    available_time = json.loads(available_time)
    amount = doctor.time_per_appoint
    data = {
        'available_time': available_time,
        'amount': amount,
    }
    return JsonResponse(data)

def check_available_to_book(request):
    id = request.GET.get('id')
    time = request.GET.get('time')
    time_arr = time.split('-')
    day_book = datetime.strptime(time_arr[3]+'/'+ time_arr[4] + '/' + time_arr[5], '%Y/%m/%d')
    if day_book < datetime.today():
        return JsonResponse({'available': False})
    day = time_arr[0]
    time_start = time_arr[1]
    doctor = Doctor.objects.get(id=id)
    available_time = doctor.available_time
    available_time = json.loads(available_time)
    for time in available_time:
        if time['day'] == int(day):
            for t in time['time']:
                if t['time-start'] == time_start:
                    time_start_datetime = datetime.strptime(t['time-start'], '%H:%M')
                    time_end_datetime = datetime.strptime(t['time-end'], '%H:%M')
                    amount = doctor.time_per_appoint
                    count = t['count']
                    left = left = floor((floor((time_end_datetime-time_start_datetime).total_seconds()/60) - amount*count)/amount)
                    print(left)
                    if left > 0:
                        return JsonResponse({'available': True})
                    else:
                        return JsonResponse({'available': False})
    return JsonResponse({'available': False})


def save_appoint(request):
    info = {}
    if request.method == 'GET':
        return JsonResponse({'success': False})
    if request.method == 'POST':
        form = request.POST.get('formData')
        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                info[key] = value
    try:
        newest_record = Transaction.objects.latest('id')
        newest_record = newest_record.id_transaction
    except:
        newest_record = 0
    id_doc = request.POST.get('id_doctor')
    id_pat = request.POST.get('id_patient')
    print(id_doc , id_pat)
    doctor = Doctor.objects.get(id=id_doc)
    patient = Patient.obejcts.get(id=id_pat)
    time = info['time-frame'].split('-')
    errors = []
    messages = ""
    if (id_pat):
        Transaction.objects.create(doctor = doctor, patient = patient, amount_transact = doctor.fee,medical_specialty = doctor.specialty, state = "pending", id_transaction = newest_record  +1)
    else:
        Transaction.objects.create(doctor = doctor, amount_transact = doctor.fee, medical_specialty = doctor.specialty, state = "pending", id_transaction = newest_record  +1, info_patient = info, appoint_address = info['address'])
    print(info)
    return JsonResponse({'success': True})
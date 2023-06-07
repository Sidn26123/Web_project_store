from django.shortcuts import render
from django.http import HttpResponse
#
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
    context= {}
    return render(request, 'CK/thankinh.html',context)
def thankinh1(request):
    context= {}
    return render(request, 'CK/thankinh1.html',context)
def tieuhoa(request):
    context= {}
    return render(request, 'CK/tieuhoa.html',context)
def tieuhoa1(request):
    context= {}
    return render(request, 'CK/tieuhoa1.html',context)
def timmach(request):
    context= {}
    return render(request, 'CK/timmach.html',context)
def timmach1(request):
    context= {}
    return render(request, 'CK/timmach1.html',context)
def taimuihong(request):
    context= {}
    return render(request, 'CK/taimuihong.html',context)
def taimuihong1(request):
    context= {}
    return render(request, 'CK/taimuihong1.html',context)
def cotsong(request):
    context= {}
    return render(request, 'CK/cotsong.html',context)
def cotsong1(request):
    context= {}
    return render(request, 'CK/cotsong1.html',context)
def dalieu(request):
    context= {}
    return render(request, 'CK/dalieu.html',context)
def dalieu1(request):
    context= {}
    return render(request, 'CK/dalieu1.html',context)
def hohap(request):
    context= {}
    return render(request, 'CK/hohap.html',context)
def hohap1(request):
    context= {}
    return render(request, 'CK/hohap1.html',context)
def nhakhoa(request):
    context= {}
    return render(request, 'CK/nhakhoa.html',context)
def nhakhoa1(request):
    context= {}
    return render(request, 'CK/nhakhoa1.html',context)

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
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            # Lấy thông tin đăng nhập từ form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Xác thực thông tin đăng nhập
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('patient:home1')
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
            
            # Kiểm tra mật khẩu cũ có đúng không
            if not request.user.check_password(old_password):
                messages.error(request, 'Mật khẩu cũ không đúng')
                return redirect('patient:change_password')
            
            # Kiểm tra mật khẩu mới và xác nhận mật khẩu
            if new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới không khớp')
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
    return render(request, 'patients/book_appointment1.html', {'form': form})


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



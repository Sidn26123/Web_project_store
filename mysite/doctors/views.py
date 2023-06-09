from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction, Test, Notification
from patients.models import Patient
from .models import Doctor, Specialties
from users.models import User
from .forms import Login_form
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from math import ceil
from .forms import Login_form, ChangeInfoForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear,ExtractMonth, ExtractYear
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.conf import settings
import json
import calendar
import csv
import os
from django.forms.models import model_to_dict
# Create your views here.
def doctor_login_view(request):
    form = Login_form()
    if request.method == "POST":
        form = Login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            doctor = authenticate(request, username = username, password = password)
            class_name = doctor.__class__.__name__
            print(class_name)
            if doctor is not None and doctor.is_active and class_name == 'Doctor':
                login(request, doctor)
                return redirect(request.GET.get('next', '/doctor/dashboard/'))
            elif doctor is not None and doctor.is_active and class_name != 'Doctor':
                return render(request, 'doctors/login.html', {'form': form, 'error': 'Tài khoản của bạn không phải là bác sĩ'})
            elif doctor is not None and not doctor.is_active:
                form.add_error('username', 'Tài khoản của bạn đã bị khóa')
                return render(request, 'doctors/login.html', {'form': form})
        else:
            form = Login_form()
    return render(request, 'doctors/login.html', {'form': form})


@login_required(login_url = '/doctor/login')
def dashboard(request):
    doctor = Doctor.objects.get(id = request.user.id)
    context = {
        'request': request,
        'doctor': doctor,
    }
    return render(request, 'doctors/dashboard.html', context)

@login_required(login_url = '/doctor/login')
def logout_view(request):
    logout(request)
    return redirect('/doctor/login')

@login_required(login_url = '/doctor/login')
def my_patient(request):
    return render(request, 'doctors/my_patient.html')
@login_required(login_url = '/doctor/login')
def review(request):
    return render(request, 'doctors/review.html')

@login_required(login_url = '/doctor/login')
def invoice(request):
    return render(request, 'doctors/invoice.html')

@login_required(login_url = '/doctor/login')
def settings(request):
    if request.method == 'POST':
        form = ChangeInfoForm(request.POST)
        if form.is_valid():
            print(form)
    form = ChangeInfoForm()
    return render(request, 'doctors/settings_page.html', {'form': form})
@login_required(login_url = '/doctor/login')
def approving_appoint(request):
    return render(request, 'doctors/approving_appoint.html')
def get_notification(request):
    doctor_id = request.GET.get('id', None)
    notices = None
    if doctor_id is not None:
        notices = Notification.objects.filter(receiver__id = doctor_id).order_by('-time_create')
        table = []
        for notice in notices:
            notice_dict = model_to_dict(notice)
            notice['time_create'] = notice['time_create'].strftime("%d/%m/%Y %H:%M:%S")
            if notice['time_notice'] != None:
                notice['time_notice'] = notice['time_notice'].strftime("%d/%m/%Y %H:%M:%S")
            table.append(notice_dict)
        data = {
            'notices': table,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({})
    
def update_appoint_status_all(request):
    # appointments = Transaction.objects.all()
    # for appoint in appointments:
    pass

def add_notification(request):
    doctor_id = request.GET.get('id', None)
    if doctor_id is not None:
        doctor = Doctor.objects.get(id = doctor_id)
        notice = Notification.objects.create(receiver = doctor, content = 'Bạn có 1 cuộc hẹn mới bây giờ', time_create = timezone.now())
        notice.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})
    
def set_status_appointment(request):
    appoint_id = request.GET.get('appoint_id')
    status = request.GET.get('status')
    if (appoint_id == None or status == None):
        return JsonResponse({'status': 'failure'})
    appoint = Transaction.objects.get(id = int(appoint_id))
    appoint.state = status
    appoint.save()
    return JsonResponse({'status': 'success'})

def update_notification(request):
    doctor_id = request.GET.get('id', None)
    now = datetime.now()
    if doctor_id is not None:
        waiting_appoints = Transaction.objects.filter(state = 'waiting', doctor__id = doctor_id, appoint_time__date = now.date())
        content = 'Bạn có ' + str(len(waiting_appoints)) + ' cuộc hẹn hôm nay'
        doctor = Doctor.objects.get(id = doctor_id)
        receiver = f'doc,{doctor_id}'
        sender = "sys,0"
        notices = Notification.objects.create(receiver = receiver, content = content, time_create = timezone.now(), sender = sender)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})


def get_notification(request):
    doctor_id = request.GET.get('id', None)
    table = []
    count = 0
    if doctor_id is not None:
        notices = Notification.objects.filter(receiver = "doc,"+str(doctor_id)).order_by('-time_create')        
        for notice in notices:
            notice_dict = model_to_dict(notice)
            notice_dict['time_create'] = notice.time_create.strftime("%d/%m/%Y %H:%M:%S")
            if notice.time_notice != None:
                notice_dict['time_notice'] = notice.time_notice.strftime("%d/%m/%Y %H:%M:%S")
            table.append(notice_dict)
        now = datetime.now()
        notice_stat = Transaction.objects.filter(doctor__id = int(doctor_id), state = "waiting", appoint_time__date = now.date()).aggregate(count = Count('id'))
        next_appoint_count = notice_stat['count']
        data = {
            'table': json.dumps(table),
            'next_appoint_count': next_appoint_count,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({})
def test_o(request):
    
    return JsonResponse({'status': 'success'})
@login_required(login_url = '/doctor/login')
def get_doctor_info(request):
    id = request.POST.get('id')
    print(id)
    doctor = Doctor.objects.get(id = int(id))
    doctor_dict = model_to_dict(doctor)
    doctor_dict['avatar'] = doctor.avatar.url

    data = {
        'doctor': doctor_dict,
    }
    return JsonResponse(data)


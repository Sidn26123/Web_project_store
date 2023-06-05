from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction, Notification
from patients.models import Patient
from .models import Doctor, Specialties, Review
from users.models import User
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from math import ceil
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum, Case, When, F, Value, CharField, DateField, IntegerField, Avg
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear,ExtractMonth, ExtractYear, TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.conf import settings
import json
import calendar
import csv
import os
from math import floor, ceil
from django.forms.models import model_to_dict

def get_doctor(request):
    id = request.GET.get('id')
    doctor = Doctor.objects.get(id=int(id))
    doctor_dict = model_to_dict(doctor)
    doctor_dict['avatar'] = doctor.avatar.url
    return JsonResponse({'doctor': doctor_dict})

def update_doctor_info(request):
    doctor_id = request.GET.get('id')
    doctor = Doctor.objects.get(id = doctor_id)
    doctor_dict = model_to_dict(doctor)
    doctor_dict['date_of_birth'] = doctor.date_of_birth.strftime("%d/%m/%Y")
    doctor_dict['date_joined'] = doctor.date_joined.strftime("%d/%m/%Y %H:%M:%S")
    doctor_dict['last_login'] = doctor.last_login.strftime("%d/%m/%Y %H:%M:%S")
    doctor_dict['avatar'] = doctor.avatar.url
    rate = Review.objects.filter(receiver_id = doctor_id).aggregate(Avg('rate'))
    data = {
        'doctor': json.dumps(doctor_dict),
        'rate': rate,
    }
    return JsonResponse(data)

def get_earn_money(request):
    id = request.GET.get('id')
    # transact = Transaction.objects.select_related('doctor').filter(doctor__id=int(id))
    doctor = Doctor.objects.get(id=int(id))
    total = doctor.income
    data = {
        'income': total,
    }
    return JsonResponse(data)

def get_money_left(request):
    id = request.GET.get('id')
    doctor = Doctor.objects.get(id=int(id))
    data = {
        'money_left': doctor.money_left,
    }
    
    return JsonResponse(data)

def get_total_patient(request):
    id = request.GET.get('id')
    # transact = Transaction.objects.select_related('doctor').filter(doctor__id=int(id), state = "success").annotate(count = Count('doctor__id', distinct=True))
    total = Transaction.objects.select_related('doctor').filter(doctor__id = int(id), state = "success").distinct().count()

    return JsonResponse({'total': total})

def get_total_appointment(request):
    id = request.GET.get('id')
    total = Transaction.objects.select_related('doctor').filter(doctor__id = int(id), state = "success").count()
    
    return JsonResponse({'total': total})


def get_appoint_next(request):
    today = datetime.now()
    doctor_id = request.GET.get('id')
    # doctor = Doctor.objects.filter(doctor__id=int(id), state = "waiting").count()
    a_next = Transaction.objects.filter(doctor__id = doctor_id, state = "waiting").count()
    a_pending = Transaction.objects.filter(doctor__id = doctor_id, state = "pending").count()
    data = {
        'next': a_next,
        'pending': a_pending,
    }
    return JsonResponse(data)

def update_state(request):
    transact_id = request.GET.get('transact_id')
    transact = Transaction.objects.get(id = transact_id)
    state = request.GET.get('state')
    transact.state = state
    transact.save()
    return JsonResponse({'state': 'success'})

def get_rate(request):
    doctor_id = request.GET.get('id')
    rate_avg = Review.objects.filter(receiver_id=doctor_id).aggregate(rate=Avg('rate'))
    if (rate_avg['rate'] == None):
        rate_avg['rate'] = 0
    rate_amount = Review.objects.filter(receiver_id = doctor_id).count()
    data = {
        'rate': rate_avg,
        'amount': rate_amount,
    }
    return JsonResponse(data)

def get_appoint_table_data(request):
    doctor_id = request.GET.get('id')
    time = request.GET.get('time')
    today = datetime.now().date()
    time_start = today
    time_end = today
    if (time == 'today'):
        time_start = today
        time_end = today
    elif time == "coming":
        time_start = today
        time_end = today + relativedelta(days=+30)
    appoints = Transaction.objects.select_related('doctor').filter(doctor__id = doctor_id, state = "waiting", appoint_time__date__range = [time_start, time_end]).order_by('appoint_time')
    table = []
    for appoint in appoints:
        temp = [appoint.patient.avatar.url, appoint.patient.real_name]
        row = [appoint.id, temp, appoint.appoint_time.strftime("%d/%m/%Y %H:%M:%S"), appoint.appoint_address, appoint.amount_transact]
        table.append(row)
    data = {
        'table': json.dumps(table),
    }
    return JsonResponse(data)

def get_transaction_detail(request):
    transact_id = request.GET.get('id')
    transact = Transaction.objects.get(id = transact_id)
    transact_dict = model_to_dict(transact)
    transact_dict['appoint_time'] = transact.appoint_time.strftime("%d/%m/%Y %H:%M:%S")
    transact_dict['patient'] = [transact.patient.real_name,transact.patient.avatar.url]
    return JsonResponse(transact_dict)

def check_next_appoint(request):
    doctor_id = request.GET.get('id')
    now = datetime.now()
    time_start = now + relativedelta(hours = -8)

    time_s = now + relativedelta(minutes= 25)
    time_end = now + relativedelta(minutes= 30)
    transact_st = Transaction.objects.filter(doctor__id = int(doctor_id), state = "waiting", appoint_time__time__gte = time_s, appoint_time__time__lt = time_end).order_by('appoint_time').first()
    if (transact_st == None):
        return JsonResponse({'status': 'no_appoint'})
    else:
        receiver = f"doctor,{doctor_id}"
        sender = "sys,0"
        content = f"Bạn có cuộc hẹn vào lúc {transact_st.appoint_time.strftime('%H:%M:%S')} với bệnh nhân {transact_st.patient.real_name}"
        obj = Notification.objects.create(receiver = receiver, sender = sender, content = content)
        obj.save()
    data = {
        'status': 'have_appoint',
        'appoint_id': transact_st.id,
    }
    return JsonResponse((data))
    #Nếu có lịch hẹn hiện tại và trước đó không có cuộc hẹn nào khác đang diễn ra
def check_upcoming_appoint(request):
    doctor_id = request.GET.get('id')
    now = datetime.now()
    time_start = now + relativedelta(hours = -8)
    if (time_start.date() != now.date()):
        time_start = time_start + relativedelta(days=+1)
        time_start = time_start.replace(hour=0, minute=0, second=0, microsecond=0)
    transact = Transaction.objects.filter(doctor__id = int(doctor_id), state__in = ["appointing", "waiting"], appoint_time__time__gte = time_start, appoint_time__time__lt = now).order_by('-appoint_time')
    status = []
    if len(transact) == 0:
        return JsonResponse({'status': 'no_appoint'})
    id_appoint = -1
    id_appointing = -1
    for tran in transact:
        if tran.state == "waiting":
            id_appoint = tran.id
        if tran.state == "waiting" and "waiting" not in status:
            status.append("waiting")
        else:
            id_appointing = tran.id
            status.append("appointing")
    status_str = ""
    if status.count("appointing") == len(status):
        status_str = "appointing"
    elif len(status) == 2 and status.count("waiting") == 1:
        status_str = "waiting_and_appointing"
    elif len(status) == 1 and status.count("waiting") == 1:
        status_str = "waiting"
    data = {
        'status': status_str,
        'appoint_id': id_appoint,
        'appointing_id': id_appointing,
    }
    return JsonResponse((data))

def get_next_appoint_id(request):
    doctor_id = request.GET.get('id')
    now = datetime.now()
    time_start = now + relativedelta(hours = -8)
    transact_st = Transaction.objects.filter(doctor__id = doctor_id, state = "waiting", appoint_time__time__gte = now).order_by('appoint_time').first()
    if transact_st == None:
        return JsonResponse({'id': -1})
    return JsonResponse({'id': transact_st.id})


def get_period_available(request):
    id = request.GET.get('id')
    doctor = Doctor.objects.get(id = id)
    available_time = doctor.available_time
    amount = doctor.time_per_appoint
    available_time = json.loads(available_time)
    period = []
    for day in available_time:
        times = day['time']
        for a in times:
            temp = {}
            temp['time_start'] = a['time-start']
            temp['time_end'] = a['time-end']
            count = a['count']
            time_start = datetime.strptime(a['time-start'], "%H:%M")
            time_end = datetime.strptime(a['time-end'], "%H:%M")
            left = floor((floor((time_end-time_start).total_seconds()/60) - amount*count)/amount)
            temp['left'] = left
            period.append(temp)
    data = {
        'period': json.dumps(period),
    }
    return JsonResponse(data)

def update_period_available(request):
    pass
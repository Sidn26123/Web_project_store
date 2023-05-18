from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction
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
    print(doctor_dict)
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
    print(data)
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
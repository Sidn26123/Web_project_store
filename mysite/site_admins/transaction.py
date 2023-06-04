from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Site_admin, Transaction
from patients.models import Patient
from doctors.models import Doctor,Specialties
from users.models import User
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from math import ceil, floor
from .forms import Login_form
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum, Case, When, F, Value, CharField, DateField, IntegerField, DateTimeField
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear,ExtractMonth, ExtractYear, TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.conf import settings
import json
import calendar
import csv
import os

def get_transaction_data(request):
    selected_value = request.GET.get('selected_value')
    now = datetime.strptime(datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
    time_start = now
    time_end = now
    step = 0
    if selected_value == "custom":
        time_start = datetime.strptime(request.GET.get('time_start'), "%Y-%m-%d")
        time_end = datetime.strptime(request.GET.get('time_end'), "%Y-%m-%d")
        time_now = datetime.strptime(request.GET.get('time_now'), '%H:%M:%S')
        if time_start > time_end:
            time_start, time_end = time_end, time_start
    else:
        if selected_value == "3-days-next":
            time_start = now + timedelta(seconds=1)
            time_end = now + relativedelta(days = 3)
            time_end.replace(hour = 23, minute = 59, second = 59)
        
        elif selected_value == "3-days-before":
            time_end = now
            time_start = now + relativedelta(days = -3) #Lấy 5 ngày trước
            time_start.replace(hour = 00, minute = 00, second = 1) #Thời gian bắt đầu từ đầu ngày
    if selected_value != 'all':
        transactions = Transaction.objects.filter(transaction_time__range = (time_start, time_end)).select_related('doctor','patient')
    else:
        transactions = Transaction.objects.all().select_related('doctor','patient')
    data = []
    for transaction in transactions:
        trans_time = datetime.strftime(transaction.transaction_time, "%d/%m/%Y %H:%M:%S")
        temp = [transaction.id, transaction.id_transaction, transaction.doctor.real_name, transaction.patient.real_name, trans_time, transaction.medical_specialty.get_name_display(), transaction.amount_transact, transaction.get_state_display()]
        data.append(temp)
    print(data)
    data = {
        'table_data': json.dumps(data),
    }
    return JsonResponse(data)
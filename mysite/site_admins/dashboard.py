from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Site_admin, Transaction
from patients.models import Patient
from doctors.models import Doctor, Specialties
from users.models import User
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from math import ceil
from .forms import Login_form
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum, Case, When, F, Value, CharField, DateField, IntegerField
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear,ExtractMonth, ExtractYear, TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.conf import settings
import json
import calendar
import csv
import os
from math import floor, ceil


def specialities_table_data(request):
    selections = request.GET.get("selected_value")
    results = []
    cases = []
    if (selections == "this-week"):
        time_start = datetime.now().date() + relativedelta(days = -7)
        time_end = datetime.now().date() + relativedelta(days = 1)

    
    elif selections == "this-month":
        time_start = datetime.now().date() + relativedelta(months = -1)
        time_end = datetime.now().date() + relativedelta(days = 1)
    spec_top = Transaction.objects.values('medical_specialty__name')\
                .annotate(count = Count('id'))\
                .annotate(total = Sum('amount_transact'))\
                .filter(transaction_time__gte = time_start, state = 'success', transaction_time__lt = time_end)\
                .values('count', 'total', 'medical_specialty__name')\
                .order_by('total')
    data = {
        'data': list(spec_top),
        'labels': [item['medical_specialty__name'] for item in spec_top],
        'amounts': [item['total'] for item in spec_top],
        'counts': [item['count'] for item in spec_top],
    }
    return JsonResponse(data)

def specialities_income_chart_data(request):
    selections = request.GET.get("selected_value")
    results = []
    time_labels = []
    cases = []
    today = datetime.now().date()
    if (selections == "weekly"): #Xử lý dữ liệu cho tuần mode
        end_of_week = today - relativedelta(days = 7 - today.weekday()) #Lấy ngày đầu tuần để truncweek gộp nhóm tính tổng trên mỗi nhóm
        time_start = end_of_week + relativedelta(weeks = -7)
        time_end = end_of_week + relativedelta(weeks = -1)
        for i in range(0,7):
            time_labels.append(time_start + relativedelta(weeks = -i - 1)) #Lấy 8 tuần làm nhãn cho chart
            q = Q(transaction_time__date__range = [time_start + relativedelta(weeks = -(i+1)) + relativedelta(days = -6),  time_start + relativedelta(weeks = -i - 1)])
            cases.append(When(q, then = time_labels[i]))
        time_labels = time_labels[::-1]

    else:
        end_of_month = today - relativedelta(days = today.day + 1) #Lấy ngày đầu tuần để truncweek gộp nhóm tính tổng trên mỗi nhóm
        time_start = end_of_month + relativedelta(months = -7)
        time_end = end_of_month + relativedelta(months = -1)
        for i in range(0,7):
            time_labels.append(end_of_month + relativedelta(months = - i))
            temp = time_start + relativedelta(months = -i)
            day_remain = datetime.date(temp.year, (temp.month+ 1), 1) - relativedelta(days = 1)
            q = Q(transaction_time__date__range = [time_start + relativedelta(months = -i - day_remain + 1), time_start + relativedelta(months = -i)])
            cases.append(When(q, then = time_labels[i]))
        time_labels = time_labels[::-1]
        
    spec_top = Transaction.objects\
                .filter(transaction_time__date__gte = time_start, state = 'success', transaction_time__date__lt = time_end)\
                .values('medical_specialty__name')\
                .annotate(time_group = Case(*cases, default=None))\
                .values('medical_specialty__name' ,'time_group', 'transaction_time')\
                .annotate(count = Count('id'))\
                .annotate(total = Sum('amount_transact'))\
    
    data = {
        # 'labels': [time for time in time_labels],
        # 'amounts': [item['total'] for item in spec_top],
        # 'counts': [item['spec_total'] for item in spec_top],
        'data': list(spec_top),
    }
    return JsonResponse(data)

def get_spec_overview_table_data(request):
    specs = Specialties.objects.all()
    spec_labels = {spec.name: spec.get_name_display() for spec in specs}
    spec = [spec.name for spec in specs]
    query_results = Transaction.objects.select_related('medical_specialty').filter(medical_specialty__in = spec).values('medical_specialty__name', 'medical_specialty__avatar').annotate(total = Sum('amount_transact')).annotate(count = Count('id'))
    table = []
    for query_result in query_results:
        temp = [spec_labels[query_result['medical_specialty__name']], query_result['medical_specialty__avatar']]
        row = [temp, query_result['total'], query_result['count']]
        table.append(row)
    data = {
        'table': json.dumps(table),
    }
    return JsonResponse(data)
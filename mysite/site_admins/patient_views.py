from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Site_admin, Transaction
from patients.models import Patient
from doctors.models import Doctor
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




def update_overview_chart(request):
    selected_value = request.GET.get('selected_value')
    labels = []
    data = []
    today = datetime.now().date()
    step = 0
    cases = []
    if selected_value == "week":

        date_list = [today - relativedelta(days=i) for i in range(0,8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]
        #Tính trong ngày nên step = 0 để lấy range(i,i)
        step = 0
        

    elif selected_value == "month":
        date_list = [today - relativedelta(days = 4*i) for i in range(0,8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]
        #Cách 4 ngày là 1 khoảng
        step = 4

    elif selected_value == "total":
        time_begin = datetime.strptime("2023-01-01", "%Y-%m-%d").date()
        step = ceil(((today- time_begin).days)/ 8)
        date_list = [today - relativedelta(days = step*i) for i in range(0, 8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]

    elif selected_value == "weekly":
        date_list = [today - relativedelta(days = 7*i) for i in range(0,8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]
        step = 7


    #Case và When được sử dụng như if/else trong SQL
    #When định nghĩa điều kiện, Case định nghĩa các trường hợp
    for date in date_list:
        q = Q(date_joined__date__range=[date - relativedelta(days= step), date])
        #Thêm các điều kiện vào list, đảm bảo đúng kiểu When để Case có thê hoạt động bình thường
        #then: trả về date nếu điều kiện q đúng, nếu ngày trong khoảng này (đúng điều kiện) thì sẽ trả về ở nhóm này và thêm vào cases
        cases.append(When(q, then=date))
        #Khi truyền vào Case() cần >=1 đối tượng When, nếu không có thì sẽ báo lỗi
        #*cases: giải nén (unpack) list cases thành các đối tượng When để đưa vào Case()
    query = Patient.objects.annotate(date_group = Case(*cases, default=None)).values('date_group').annotate(count = Count('id'))
    # query = Patient.objects.filter(date_joined__date__in = date_list).annotate(date = TruncDate('date_joined')).values('date').annotate(count = Count('id'))
    temp = 0;
    for date in date_list:
        if query.filter(date_group = date).exists():
            data.append(query.filter(date_group = date)[0]['count'] + temp)
            temp = temp + query.filter(date_group = date)[0]['count']
        else:
            data.append(0 + temp)
    data = {
        'labels': labels,
        'data': data,
    }
    return JsonResponse(data)

def update_overview_reg_chart(request):
    selected_value = request.GET.get('selected_value')
    labels = []
    data = []
    today = datetime.now().date()
    step = 0
    cases = []
    if selected_value == "week":

        date_list = [today - relativedelta(days=i) for i in range(0,8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]
        #Tính trong ngày nên step = 0 để lấy range(i,i)
        step = 0
        

    elif selected_value == "month":
        date_list = [today - relativedelta(days = 4*i) for i in range(0,8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]
        #Cách 4 ngày là 1 khoảng
        step = 4

    elif selected_value == "total":
        time_begin = datetime.strptime("2023-01-01", "%Y-%m-%d").date()
        step = ceil(((today- time_begin).days)/ 8)
        date_list = [today - relativedelta(days = step*i) for i in range(0, 8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]

    elif selected_value == "weekly":
        date_list = [today - relativedelta(days = 7*i) for i in range(0,8)][::-1]
        labels = [label.strftime("%d/%m/%Y") for label in date_list]
        step = 7


    #Case và When được sử dụng như if/else trong SQL
    #When định nghĩa điều kiện, Case định nghĩa các trường hợp
    for date in date_list:
        q = Q(date_joined__date__range=[date - relativedelta(days= step), date])
        #Thêm các điều kiện vào list, đảm bảo đúng kiểu When để Case có thê hoạt động bình thường
        #then: trả về date nếu điều kiện q đúng, nếu ngày trong khoảng này (đúng điều kiện) thì sẽ trả về ở nhóm này và thêm vào cases
        cases.append(When(q, then=date))
        #Khi truyền vào Case() cần >=1 đối tượng When, nếu không có thì sẽ báo lỗi
        #*cases: giải nén (unpack) list cases thành các đối tượng When để đưa vào Case()
    query = Patient.objects.annotate(date_group = Case(*cases, default=None)).values('date_group').annotate(count = Count('id'))
    # query = Patient.objects.filter(date_joined__date__in = date_list).annotate(date = TruncDate('date_joined')).values('date').annotate(count = Count('id'))
    for date in date_list:
        if query.filter(date_group = date).exists():
            data.append(query.filter(date_group = date)[0]['count'])
        else:
            data.append(0)
    data = {
        'labels': labels,
        'data': data,
    }
    return JsonResponse(data)


def get_new_register_amount(request):
    gender_data = {}
    today = datetime.now().date()
    start_of_cur_month = today.replace(day=1)
    #So sánh với tháng trước (cùng số ngày với hiện taại)
    end_of_bef_month = start_of_cur_month - relativedelta(days=1)
    end_of_bef_month = end_of_bef_month.replace(day=today.day)
    start_of_bef_month = end_of_bef_month.replace(day=1)
    #Tính số lượng đăng ký trong tháng hiện tại
    query = Patient.objects.filter(date_joined__date__range=[start_of_cur_month, today]).count()
    #Tính số lượng đăng ký trong tháng trước cùng kỳ
    query_b = Patient.objects.filter(date_joined__date__range=[start_of_bef_month, end_of_bef_month]).count()
    #Tính % tăng giảm
    if (query_b == 0):
        diff = query
    else:
        diff = ((query - query_b)/query_b)*100
    
    #Truy vấn các đăng ký theo giới tính
    gender_q = Patient.objects.filter(date_joined__date__range = [start_of_cur_month, today]).values('gender').annotate(count = Count('id')).order_by('-count')
    for gender in gender_q:
        gender_data[gender['gender']] = gender['count']
    labels = [gender['gender'] for gender in gender_q]
    counts = [gender['count'] for gender in gender_q]
    # ages = {'teen': Q(new_age__lt = 18), 'adult': Q(new_age__gte = 18, new_age__lt = 60), 'old': Q(new_age__gte = 60)}
    # ages = {'new_age': (0, 18), 'new_age': (18, 60), 'new_age': (60, None)}
    age_ranges = [(0, 18), (18, 60), (60, None)]
    #Tạo các case để truy vấn và gộp nhóm theo khoảng
    cases = []
    for age_range in age_ranges:
        q = Q(new_age__gte=age_range[0])
        if age_range[1]:
            q &= Q(new_age__lt=age_range[1])
        cases.append(When(q, then=Value(age_range[0], output_field=IntegerField())))
    
    q = Patient.objects.filter(date_joined__date__range = [start_of_cur_month, today]).annotate(age_range=Case(*cases, default=Value(None, output_field=IntegerField()))).values('age_range').annotate(count=Count('id')).order_by('age_range')
    age_q = Patient.objects.filter(date_joined__date__range = [start_of_cur_month, today]).annotate(age_group = Case(*cases, default = None)).values('age_group').annotate(count = Count('id')).order_by('-count')
    age_labels = []
    age_label = ["Teen", "Adult", "Old"]
    age_data = {}
    for age in age_q:
        if (age['age_group'] == 0):
            age_labels.append('Teen')
        elif (age['age_group'] == 18):
            age_labels.append('Adult')
        else:
            age_labels.append('Old')
        age_data[age['age_group']] = age['count']
    for age in age_label:
        if age not in age_labels:
            age_labels.append(age)
    age_count = [age['count'] for age in age_q]
    data = {
        'gender': gender_data,
        'labels': labels,
        'counts': counts,
        'amount': query,
        'percent_diff': diff,
        'age': age_data,
        'age_labels': age_labels,
        'age_count': age_count,
    }
    return JsonResponse(data)

def get_account_status(request):
    patient_status = Patient.objects.values('is_active').annotate(count = Count('id')).all().values('is_active','count').order_by('-count')
    status = []
    amounts = []
    for st in patient_status:
        if (st['is_active'] == True):
            status.append("Đang hoạt động")
        elif (st['is_active'] == False):
            status.append("Bị khóa/xóa")
        amounts.append(st['count'])
    data = {
        'labels': status,   
        'amounts': amounts,
    }
    return JsonResponse(data)
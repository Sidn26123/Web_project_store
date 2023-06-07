from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Site_admin, Transaction
from patients.models import Patient
from doctors.models import Doctor, Review
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
    start_of_bef_month = end_of_bef_month.replace(day=1)
    end_of_bef_month = start_of_bef_month + relativedelta(days = today.day)
    #Tính số lượng đăng ký trong tháng hiện tại
    query = Patient.objects.filter(date_joined__date__range=[start_of_cur_month, today]).count()
    #Tính số lượng đăng ký trong tháng trước cùng kỳ
    query_b = Patient.objects.filter(date_joined__date__range=[start_of_bef_month, end_of_bef_month]).count()
    #Tính % tăng giảm
    if (query_b == 0):
        diff = query
    else:
        diff = ((query - query_b)/query_b)
    
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

def get_patient_table(request):
    #../?gender=man&gender=woman&province=Binh_thuan
    #Lấy các key có trong url gender, province
    url_params = request.GET.keys()
    #Luu trữ toàn bộ cặp key-value có trong url
    url_param_values = []
    #Duyệt để đẩy cặp key-value vào url_param_values
    for key in url_params:
        param_list = request.GET.getlist(key)
        for param in param_list:
            url_param_values.append([key, param])
            
    query = Q()
    query_temp = Q()
    sort = ""
    gender_conditions = []
    province_conditions = []
    age_conditions = []
    age = (0,0)
    #Duyệt các phần tử để thêm vào query
    for key, value in url_param_values:
        if key == "gender":
            gender_conditions.append(value)
        elif key == "province":
            province_conditions.append(value)
        elif key == "sort_by":
            sort = value
        elif key == "search_query":
            query &= Q(real_name__icontains = value)
        elif key == "age-start":
            age[1] = int(value)
        elif key == "age-end":
            age[1] = int(value)
        elif key == "age":
            age_conditions.append(value)
            # if value == "teen":
            #     query |= Q(new_age__lt = 19)
            # elif value == "adult":
            #     query |= Q(new_age__range = (20,59))
            # elif value == "elderly":
            #     query |= Q(new_age__gte = 60)
    for condition in gender_conditions:
        query_temp |= Q(gender = condition)
    if (query):
        query &= query_temp
    else:
        query = query_temp
    query_temp = Q()
    
    for condition in province_conditions:
        query_temp |= Q(province = condition)
        
    if (query_temp):
        query &= query_temp
        query_temp = Q()
    
    for condition in age_conditions:
        if condition == "teen":
            query_temp |= Q(new_age__lt = 19)
        elif condition == "adult":
            query_temp |= Q(new_age__range = (20,59))
        elif condition == "elderly":
            query_temp |= Q(new_age__gte = 60)
    if query_temp:
        query &= query_temp
    
    #Xử lý các query về tuổi
    # if age[0] == 0 and age[1] == 0:
    #     pass
    # elif age[0] == 0:
    #     query |= Q(age__lt = age[1])
    # elif age[1] == 0:
    #     query |= Q(age_gte = age[0])
    # else:
    #     query |= Q(age__range = range(age[0], age[1]))
        
    #Xử lí query sort
    results = Patient.objects.filter(query)
    table = []
    
    for result in results:
        img = [result.avatar.url, result.real_name]
        row = [result.id, img, result.new_age, result.get_gender_display(), result.get_province_display(), result.citizen_identification, result.phone, datetime.strftime(result.date_joined, "%d/%m/%Y %H:%M:%S"), result.is_active]
        table.append(row)
    data = {
        'table_data': table,
    }
    return JsonResponse(data)

def update_patient_status(request):
    patient_id = request.GET.get('id')
    patient = Patient.objects.get(id = int(patient_id))
    status =  patient.is_active
    
    # status = True if status == "true" else False
    # print(patient.is_active)
    patient.is_active = not status
    patient.save()
    return JsonResponse({'status': 'ok'})

def get_amount_info(request):
    account_amount = Patient.objects.filter(is_active = True).count()
    cases = {'zero':0, 'one_more': 0, 'two_more': 0}
    appoint = Transaction.objects.filter(state = 'success').annotate(count = Count('patient__id')).values('count')
    for a in appoint:
        if a['count'] == 0:
            cases['zero'] += 1
        elif a['count'] >= 1:
            cases['one_more'] += 1
        if a['count'] >= 2:
            cases['two_more'] += 1
    cases['zero'] = account_amount - cases['one_more']- cases['two_more']
    rates = Review.objects.filter(rate__gte = 4).count()
    
    data = {
        'accounts': account_amount,
        'not_book_yet': cases['zero'],
        'as_least_one': cases['one_more'],
        'more_than_one': cases['two_more'],
        'patient_satisfied': rates,
    }
    return JsonResponse(data)
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction, Invoice, Notification
from patients.models import Patient
from .models import Doctor, Specialties, Review, MyPaient
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

def get_review_data(request):
    id = request.GET.get('doctor-id')
    # star = start_condition.split(',')
    doctor = Doctor.objects.get(id = int(id))
    doctor_dict = {'id': doctor.id, 'real_name': doctor.real_name, 'avatar': doctor.avatar.url}
    star_condition_str = request.GET.get('star-condition')
    print(star_condition_str)
    # Nếu star_condition_str == None thì trả về {}
    if star_condition_str == None:
        return JsonResponse({})
    #Chuyển star sang int
    star_condition = [int(star) for star in star_condition_str.split(',') if star != '']
    star_avg = {}
    #Tính trung bình số sao
    star_avg['avg'] = Review.objects.filter(receiver_id = int(id)).aggregate(Avg('rate'))['rate__avg']
    #Tính tổng lượt rate
    star_avg['count'] = Review.objects.filter(receiver_id = int(id)).count()
    #Lấy chi tiết lượt rate
    star_detail_temp = Review.objects.filter(receiver_id = int(id)).values('rate').annotate(count = Count('rate')).order_by('rate')
    # for i in range(0,5):
    #     st = str(float(i))
    #     if st not in star_detail_temp:
    #         star_detail[0][st] = 0
    #     else:
    #         star_detail[0][st] = star_detail_temp[0][st]
    star_detail_dict_t = {}
    star_detail_dict = {}
    for star in star_detail_temp:
        star_detail_dict_t[int(star['rate'])] = star['count']
    for i in range(1,6):
        temp = ((i))
        if temp not in star_detail_dict_t:
            star_detail_dict[str(temp)] = 0
        else:
            star_detail_dict[str(temp)] = star_detail_dict_t[i]
    print(star_detail_dict)
    star_query = Q()
    for s in star_condition:
        print(s)
        star_query = star_query | Q(rate = s)
    query = Q(receiver_id = int(id)) & star_query
    reviews = Review.objects.filter(query)
    print(reviews)
    review_arr = []
    for review in reviews:
        temp_dict = {}
        temp_dict['patient_id'] = review.sender_id.id
        temp_dict['doctor_id'] = review.receiver_id.id
        temp_dict['rate'] = review.rate
        temp_dict['feedback'] = review.feedback
        temp_dict['time_review'] = review.time_feedback.strftime("%d/%m/%Y %H:%M:%S")
        review_arr.append(temp_dict)
    data = {
        'star_avg': json.dumps(star_avg),
        'star_detail': json.dumps(star_detail_dict),
        'reviews': json.dumps(review_arr),
        'doctor': json.dumps(doctor_dict),
    }

    return JsonResponse(data)

def get_invoice(request):
    id = request.GET.get('doctor-id')
    time_condition = request.GET.get('time-condition')
    if time_condition != None:
        time_condition = time_condition.split(',')
    query_condition = request.GET.get('query-condition')
    print(id, time_condition, query_condition)
    time_query = Q()
    if time_condition == None:
        time_query = Q()
    elif (time_condition[0] == "" and time_condition[1] == ""):
        time_query = Q()
    elif (time_condition[0] == ""):
        time_format = datetime.strptime(time_condition[1] + " 23:59:59", "%d/%m/%Y %H:%M:%S")
        time_query = Q(transaction_time__lte = time_format)
    elif time_condition[1] == "":
        time_format = datetime.strptime(time_condition[0] + " 00:00:00", "%d/%m/%Y %H:%M:%S")
        time_query = Q(transaction_time__gte = time_format)
    elif time_condition[0] != "" and time_condition[1] != "":
        time_start_format = datetime.strptime(time_condition[0] + " 00:00:00", "%d/%m/%Y %H:%M:%S")
        time_end_format = datetime.strptime(time_condition[1] + " 23:59:59", "%d/%m/%Y %H:%M:%S")
        time_query = Q(transaction_time__gte = time_start_format) & Q(transaction_time__lte = time_end_format)
    else:
        return JsonResponse({'status': 'error'})
    if query_condition == None:
        search_query = Q()
    elif query_condition == "":
        search_query = Q()
    else:
        search_query = Q(id__icontains = query_condition)
    invoice_query = Q(doctor__id = int(id))
    invoices = Invoice.objects.filter(invoice_query & time_query & search_query)
    table = []
    print(invoices)
    for invoice in invoices:
        if invoice.show_on_doctor == False:
            continue
        temp = [invoice.patient.real_name, invoice.patient.avatar.url]
        row = [invoice.id_transaction, invoice.patient.id, temp, invoice.appoint_time.strftime("%d/%m/%Y %H:%M:%S"), invoice.appoint_address, invoice.amount_transact, invoice.status]
        table.append(row)
        
    data = {
        'table': json.dumps(table),
    }
    return JsonResponse(data)

def hide_invoice(request):
    id = request.GET.get('id')
    invoice = Invoice.objects.get(id_transaction = id)
    invoice.show_on_doctor = False
    invoice.save()
    return JsonResponse({'status': 'success'})
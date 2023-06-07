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


def get_doctor_table_data(request):
    url_keys = request.GET.keys()
    query_params = []
    query = Q()
    for key in url_keys:
        key_list = request.GET.getlist(key)
        for param in key_list:
            query_params.append([key, param])
    age_query = Q()
    province_query = Q()
    spec_query = Q()
    gender_query = Q()
    text_query = Q()
    specs = []
    provinces = []
    for key, value in query_params:
        if key == "age":
            if value == "group_1":
                age_query |= Q(new_age__lte = 25)
            elif value == "group_2":
                age_query |= Q(new_age__range = (26, 40))
            elif value == "group_3":
                age_query |= Q(new_age__range = (41, 60))
        elif key == "province":
            # province_query |= Q(province = value)
            provinces.append(value)
        elif key == "spec":
            specs.append(value)
        elif key == "search_query":
            text_query = Q(real_name__icontains = value)
        elif key == "gender":
            gender_query |= Q(gender = value)
    
    province_query = Q(province__in = provinces)
    spec_query = Q(specialty__in = specs)
    query = age_query  & gender_query & text_query
    if (provinces):
        query &= province_query
    if (specs):
        query &= spec_query
    print(query)
    doctors = Doctor.objects.filter(query)
    tables = []
    for doctor in doctors:
        if doctor.avatar:
            temp = [doctor.avatar.url, doctor.real_name]
        else: temp = ['none', doctor.real_name]
        table = [doctor.id, temp, doctor.new_age, doctor.phone, doctor.email, doctor.address, doctor.position, doctor.rate, doctor.income]
        tables.append(table)
    data = {
        'table': json.dumps(tables),
    }
    print(data)
    return JsonResponse(data)


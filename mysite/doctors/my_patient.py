from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction
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

def get_patient(request):
    id = request.GET.get('id')
    condition = request.GET.get('condition')
    today = date.today()
    # doctor = Doctor.objects.get(id = id) 
    time_query = Q()
    # condition_arr = condition.split(',')
    # if "all" in condition_arr:
    #     time_query = Q()
    # else:
    #     if "before" in condition_arr:
    #         time_query = Q(counter = 0)
    #     if "upcoming" in condition_arr:
    #         time_query = Q()
    if time_query != Q():
        patients = MyPaient.objects.filter(doctor__id = int(id)).filter(time_query)
    else:
        patients = MyPaient.objects.filter(doctor__id = int(id))
    patient_data = []
    for patient in patients:
        pat = Patient.objects.get(id = patient.patient.id)
        pat_dict = {}
        pat_dict['name'] = pat.real_name
        pat_dict['avatar'] = pat.avatar.url
        pat_dict['age'] = pat.new_age
        pat_dict['phone'] = pat.phone
        pat_dict['email'] = pat.email
        pat_dict['blood_group'] = pat.blood_group
        pat_dict['address'] = pat.address
        pat_dict['id'] = pat.id
        patient_dict = model_to_dict(patient)
        patient_dict['avatar'] = patient.patient.avatar.url
        # patient_dict['doctor_name'] = patient.doctor.real_name
        # patient_dict['patient_name'] = patient.patient.real_name
        # patient_dict['id'] = patient.patient.id
        # patient_dict['age'] = patient.patient.new_age
        # patient_dict['address'] = patient.patient.address
        # patient_dict['phone'] = patient.patient.phone
        # patient_dict['email'] = patient.patient.email
        # patient_dict['blood_group'] = patient.patient.blood_group
        patient_dict['last_time'] = patient.last_time.strftime("%d/%m/%Y")
        patient_dict['patient'] = pat_dict
        patient_data.append(patient_dict)
    data = {
        'patients': json.dumps(patient_data),
    }
    return JsonResponse(data)

def delete_my_patient(request):
    id = request.GET.get('id')
    print(id)
    my_patient = MyPaient.objects.get(patient__id = int(id))
    my_patient.delete()
    
    return JsonResponse({'status': 'success'})
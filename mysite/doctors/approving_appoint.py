from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction, Notification
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


def get_confirming_appoint(request):
    appoint_id = request.GET.get('id')
    now = datetime.now()
    start_time = now - relativedelta(days = 3)
    appoints = Transaction.objects.filter(state = 'pending').filter(transaction_time__gte = start_time).order_by('-appoint_time')
    table = []
    for appoint in appoints:
        temp = [appoint.patient.real_name, appoint.patient.avatar.url]
        row = [appoint.id, appoint.patient.id, temp, appoint.patient.gender,  appoint.appoint_time.strftime("%d/%m/%Y %H:%M:%S"),  appoint.appoint_address, appoint.amount_transact,appoint.get_state_display()]
        table.append(row)
    
    data = {
        'table': json.dumps(table),
    }
    return JsonResponse(data)

def update_appoint_status(request):
    appoint_id = request.GET.get('appoint_id')
    choice = request.GET.get('choice')
    if (appoint_id == None or choice == None):
        return JsonResponse({'status': 'failure'})
    appoint = Transaction.objects.get(id = int(appoint_id))

    if (choice == "accept-confirm"):
        appoint.state = "waiting"
    elif (choice == "deny-confirm"):
        appoint.state = "denied"
    appoint.save()
    row = [appoint.id, appoint.patient.real_name, appoint.state]
    data = {
        'row': json.dumps(row),
    }
    return JsonResponse(data)

def test(request):
    obj = Transaction.objects.all()
    for o in obj:
        o.state = 'pending'
        o.save()
        


def update_expired_spec_appoint(request):
    appoint_id = request.GET.get('appoint_id')
    if (appoint_id == None):
        return JsonResponse({'status': 'failure'})
    appoint = Transaction.objects.get(id = int(appoint_id))
    if (appoint.state == 'pending'):
        appoint.state = 'denied'
        appoint.save()
    doctor = Doctor.objects.get(id = appoint.doctor.id)
    patient = Patient.objects.get(id = appoint.patient.id)
    content = "Bạn đã không nhận cuộc hẹn với " + patient.real_name 
    notice = Notification.objects.create(content, doctor, patient, time_notice = datetime.now())
    notice.save()
    return JsonResponse({'status': 'success'})

def update_upcoming_appoint_notification(request):
    now = datetime.now()
    start_time = now + relativedelta(minutes = 25)
    end_time = now + relativedelta(minutes = 30)
    transacts = Transaction.objects.filter(state = 'waiting').filter(appoint_time__gte = start_time).filter(appoint_time__lte = end_time).select_related('doctor', 'patient')
    for transact in transacts:
        doctor = transact.doctor
        patient = transact.patient
        content_for_doctor = "Bạn có cuộc hẹn với " + patient.real_name + " trong khoảng 30 phút nữa"
        content_for_patient = "Bạn có cuộc hẹn với " + doctor.real_name + " trong khoảng 30 phút nữa"
        doctor_notice = Notification.objects.create(content = content_for_doctor,receiver = doctor, sender = patient)
        patient_notice = Notification.objects.create(content = content_for_patient, receiver =  patient, sender = doctor)
        doctor_notice.save()
        patient_notice.save()
    return JsonResponse({'status': 'success'})
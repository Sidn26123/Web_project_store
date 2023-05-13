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


def get_spec_data(request):
    spec_labels = []
    specs = Specialties.objects.all()
    spec_labels = [spec.name for spec in specs]
    spec_display = [spec.get_name_display() for spec in specs]
    spec_description = [spec.description for spec in specs]
    transactions = Transaction.objects.filter(medical_specialty__in = spec_labels).values('medical_specialty').annotate(total = Sum('amount_transact')).annotate(count = Count('id_transaction'))
    doctors = Doctor.objects.filter(specialty__in = spec_labels).values('specialty').annotate(count = Count('id'))
    data = []
    for i in range(0, len(spec_labels)):
        transaction_count = transactions.filter(medical_specialty = spec_labels[i])[0]['count'] #if i < len(spec_labels) else transactions
        if transactions.filter(medical_specialty = spec_labels[i], state = 'success').exists():
            transaction_total = transactions.filter(medical_specialty = spec_labels[i], state = 'success')[0]['total'] #if i < len(spec_labels) else transactions
        else:
            transaction_total = 0
        if (doctors.filter(specialty = spec_labels[i]).exists()):
            doctor_num = doctors.filter(specialty = spec_labels[i])[0]['count'] #if i < len(spec_labels) else transactions
        else:
            doctor_num = 0
        temp = [spec_display[i], spec_description[i], doctor_num, transaction_total, transaction_count]
        data.append(temp)
    data = {
        'table_data': json.dumps(data),
    }
    return JsonResponse(data)
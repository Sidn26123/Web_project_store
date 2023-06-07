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

def save_change(request):
    id = request.POST.get('id')
    data = request.POST.get('data')
    data = json.loads(data)
    data['date_of_birth'] = datetime.strptime(data['date_of_birth'], "%Y-%m-%d")
    doctor = Doctor.objects.get(id = int(id))
    for key, value in data.items():
        setattr(doctor, key, value)
    doctor.save()
    return JsonResponse({})
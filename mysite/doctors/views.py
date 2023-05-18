from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction, Test, Notification
from patients.models import Patient
from .models import Doctor, Specialties
from users.models import User
from .forms import Login_form
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from math import ceil
from .forms import Login_form
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear,ExtractMonth, ExtractYear
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.conf import settings
import json
import calendar
import csv
import os
# Create your views here.

@login_required(login_url = '/doctor/login')
def dashboard(request):
    context = {
        'request': request,
    }
    return render(request, 'doctors/dashboard.html', context)

def doctor_login_view(request):
    form = Login_form()
    if request.method == "POST":
        form = Login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            doctor = authenticate(request, username = username, password = password)
            print(doctor)
            if doctor is not None:
                login(request, doctor)
                print(request.user.is_authenticated)
                return redirect(request.GET.get('next', ''))
        else:
            form = Login_form()
    return render(request, 'doctors/login.html', {'form': form})


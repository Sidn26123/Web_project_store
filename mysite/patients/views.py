from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from site_admins.models import Site_admin, Transaction
from .models import Patient
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

class Register_view(View):
	def get(self, request):
		form = Register_form()
		return render(request, 'patients/register_view.html', {'form': form})

	def post(self, request):
		form = Register_form(request.POST)
		if form.is_valid():
			form.save()
			return redirect("../")

		return render(request, 'patients/register_view.html', {'form': form})


class Login_view(View):
	def get(self, request):
		form = Login_form()
		return render(request, 'patients/login_test.html', {'form': form})

	def post(self, request):
		form = Login_form(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			#Hàm auth có sẵn của django trong User class, đưa vào các tham số và trả về 1 obj hoặc None
			user = authenticate(request, username = username, password = password)
			# user_ = Site_admin.objects.get(username = username)
			# if (password == user_.password):
				# user_1 = User.objects.get(username = username)
			if user is not None:
				if user.is_admin:
					login(request, user)
					return redirect('../../admin/')

				else:
					login(request, user)
					return redirect('../../')
		else:
			form = Login_form()
		return render(request, 'patients/login_test.html', {'form': form})

def test_view(request):
    context = {
		'request': request,
	}
    return render(request, 'patients/book.html', context)

def book_appointment(request):
    form_data = request.POST.get('form_data')
    doctor_id = request.POST.get('doctor_id')
    datas = form_data.split('&')
    arr = {}
    for da in datas:
        da = da.split('=')
        arr.update({da[0]: da[1]})
    print(arr)
    patient_id = int(arr['patient-name'])
    date_book = request.POST.get('date_book')
    time_choice = request.POST.get('time_book')
    if time_choice == '1':
        time_choice = '09:00:00'
    elif time_choice == '2':
        time_choice = '10:00:00'
    elif time_choice == '3':
        time_choice = '11:00:00'
    amount = 113000
    time_booked = datetime.strptime(time_choice, '%H:%M:%S')
    date_book = datetime.strptime(date_book, '%Y-%m-%d')
    date_book = date_book.replace(hour = time_booked.hour, minute = time_booked.minute, second = time_booked.second)
    doctor = Doctor.objects.get(id = int(doctor_id))
    spec = doctor.specialty
    patient = Patient.objects.get(id = int(patient_id))
    transact = Transaction.objects.create(doctor = doctor, patient = patient, amount_transact = amount, appoint_time = date_book, state = 'waiting', medical_specialty = spec)
    return JsonResponse({'status': 'success'})
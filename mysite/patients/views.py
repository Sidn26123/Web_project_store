from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Patient
from users.models import User
from site_admins.models import Site_admin
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from .forms import Login_form, Register_form


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
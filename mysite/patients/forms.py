from django import forms
import re
from .models import Patient
from site_admins.models import Site_admin
from django.core.exceptions import ValidationError


class Register_form(forms.Form):
	# class Meta:
	# 	model = User
	# 	fields = [
	# 		'username',
	# 		'password',
	# 		'email'
	# 	]
	username = forms.CharField(
				widget = forms.TextInput(
					attrs = {
						"class": "",
						}
					)
				)
	password = forms.CharField(
					label = "Mật khẩu",
					widget = forms.PasswordInput(
						attrs = {
							"class": "",
							}
						)
				)
	confirm_password = forms.CharField(
					label = "Nhập lại mật khẩu",
					widget = forms.PasswordInput(
						attrs = {
							"class": "",
							}
						)
					)

	def clean_username(self):
		username = self.cleaned_data["username"]
		if 'username' in self.cleaned_data:
			if len(username) <= 3:
				raise forms.ValidationError("Tài khoản quá ngắn. Tên tài khoản phái chứa 4-26 ký tự. Chỉ chứa các ký tự 0-9, a-z, A-Z, @, -,+,_") 
			elif len(username) >= 21:
				raise forms.ValidationError("Tài khoản quá dài. Tên tài khoản phái chứa 4-26 ký tự. Chỉ chứa các ký tự 0-9, a-z, A-Z, @, -,+,_")
			elif not re.search(r'^\w+$', username):
				raise forms.ValidationError("Tên tài khoản chứa kí tự đặc biệt")
			#Kiểm tra account đã tồn tại trong database hay chưa, dùng try expect để không bị redirect hay xuất lỗi không tồn tại
			try:
				Site_admin.objects.get(username = username)
			except Site_admin.DoesNotExist :
				return username
			else:
				raise forms.ValidationError("Tài khoản đã tồn tại")
			return username
		raise forms.ValidationError("Tài khoản")

	def clean_password(self):
		if "password" in self.cleaned_data:
			password = self.cleaned_data["password"]
			if len(password) <= 3:
				raise forms.ValidationError("Mật khẩu quá ngắn")
			elif len(password) >= 31:
				raise forms.ValidationError("Mật khẩu quá dài")
			return password
		raise forms.ValidationError("Mật khẩu")

	def clean_confirm_password(self):
		if "confirm_password" in self.cleaned_data and "password" in self.cleaned_data:
			if (self.cleaned_data["confirm_password"] != self.cleaned_data["password"]):
				raise forms.ValidationError("Mật khẩu không trùng khớp")
			return self.cleaned_data["confirm_password"]
		raise forms.ValidationError("Không hợp lệ")

	def check_email(self):
		regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
		if (re.fullmatch(regex, self.cleaned_data["username"])):
			return self.cleaned_data["username"]
		return ""
	def save(self):
		Site_admin.objects.create(
			username = self.cleaned_data["username"],
			password = self.cleaned_data["password"],
			)


class Login_form(forms.Form):
	username = forms.CharField(
				widget = forms.TextInput(
					attrs = {
						"class": "",
						}
					)
				)
	password = forms.CharField(
					label = "Mật khẩu",
					widget = forms.PasswordInput(
						attrs = {
							"class": "",
							}
						)
				)

	def clean_username(self):
		if 'username' in self.cleaned_data:
			username = self.cleaned_data["username"]
			if len(username) <= 3:
				raise forms.ValidationError("Tài khoản quá ngắn. Tên tài khoản phái chứa 4-26 ký tự. Chỉ chứa các ký tự 0-9, a-z, A-Z, @, -,+,_") 
			elif len(username) >= 21:
				raise forms.ValidationError("Tài khoản quá dài. Tên tài khoản phái chứa 4-26 ký tự. Chỉ chứa các ký tự 0-9, a-z, A-Z, @, -,+,_")
			elif not re.search(r'^\w+$', username):
				raise forms.ValidationError("Tên tài khoản chứa kí tự đặc biệt")
			try:
				Site_admin.objects.get(username = username)
			except Site_admin.DoesNotExist:
				raise forms.ValidationError("Tai khoan khong ton tai")
			return username
		raise forms.ValidationError("Tài khoản")

	def clean_password(self):
		if "password" in self.cleaned_data:
			password = self.cleaned_data["password"]
			if len(password) <= 3:
				raise forms.ValidationError("Mật khẩu quá ngắn")
			elif len(password) >= 31:
				raise forms.ValidationError("Mật khẩu quá dài")
			return password
		raise forms.ValidationError("Mật khẩu không được để trống")

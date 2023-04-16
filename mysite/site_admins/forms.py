from django import forms
import re
from site_admins.models import Site_admin
from django.core.exceptions import ValidationError

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
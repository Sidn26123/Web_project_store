from django import forms
import re
from doctors.models import Doctor
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
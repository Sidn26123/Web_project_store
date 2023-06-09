from django import forms
import re
from doctors.models import Doctor
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import RegexValidator
from site_admins.models import Transaction
from django.core.validators import validate_email
from datetime import datetime
from .models import Doctor

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
class ChangeInfoForm(forms.Form):
    avatar = forms.FileField(
		widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Ảnh đại diện'}), required = False
	)
    real_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên '})
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'})
    )
    email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
	)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ngày sinh', 'type': 'date'})
	)
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tỉnh/Thành phố'})
    )
    district = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Huyện'})
    )
    address = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ cụ thể'})
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # if not email.endswith('@gmail.com'):  # Ràng buộc email phải kết thúc bằng @example.com
        #     raise forms.ValidationError("Email phải kết thúc bằng @gmail.com")
        # return email
        try:
            validate_email(email)
        except:
            raise forms.ValidationError("Email không hợp lệ")
        if len(email) > 120:
            raise forms.ValidationError("Email không hợp lệ")
        if Doctor.objects.filter(email=email).exists():
            user = Doctor.objects.get(email=email)
            
            # Kiểm tra xem email có trùng với email của user hiện tại hay không
            if user.id != self.instance.id:
                raise forms.ValidationError('Email này đã tồn tại.')
        return email
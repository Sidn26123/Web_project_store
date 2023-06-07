# ràng buộc số điện thoại
from django import forms
from django.core.validators import RegexValidator
from site_admins.models import Transaction
from django.core.validators import validate_email
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{10,11}$',
    message="Số điện thoại phải ở định dạng: '+123456789'. Số điện thoại tối thiểu 10 chữ số và tối đa 11 chữ số."
)
# Ràng buộc tỉnh/thành phố



#CODE ĐĂNG KÝ
from django import forms
from .models import Patient
class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'})
    )
    email = forms.EmailField( 
        error_messages={
            'invalid': 'Địa chỉ email không hợp lệ.',
        },
        label='Email',
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật Khẩu'}))
    confirm_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'}))
    real_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'})
    )
    citizen_identification = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Căn cước công dân'})
    )
    phone = forms.CharField(
        validators=[phone_regex],
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'})
    )
    # province = forms.CharField(
    #     max_length=50,
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tỉnh/Thành phố'})
    # )
    #CHOICES = (
    #    ('1',1),
    #    ('2',2),
    #)
    #province = forms.ChoiceField(
    #                            choices = CHOICES,
    #                            widget = forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tỉnh/Thành phố'})
    #                            )
    district = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Huyện'})
    )
    XA = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XA'})
    )
    address = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ cụ thể'})
    )
    class Meta:
        model = Patient
        fields = ('username', 'email', 'password','confirm_password', 'real_name','phone','citizen_identification','date_of_birth', 'gender', 'province', 'district', 'XA','address')
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Mật khẩu không khớp')
        return cleaned_data
  # Ràng buộc email
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
        return email
#code đăng nhập
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())



#code đổi mật khẩu
from django import forms

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

#code phần chuyên lkhoa đặt khám thông tin bác sĩ
from doctors.models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
#Code phầnđặt khám
from .models import Patient

class PatientForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên '})
    )
    phone_number = forms.CharField(
       	validators=[phone_regex],
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'})
    )
    country = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quốc gia'})
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
    
    class Meta:
        model = Patient
        fields = ('name','date_of_birth', 'gender', 'phone_number', 'country', 'city', 'district', 'address')
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}
#code tìm kiếm bác sĩ
from django import forms

class DoctorSearchForm(forms.Form):
    search_keyword = forms.CharField(label='', max_length=100)


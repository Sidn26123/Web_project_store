from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Site_admin, Transaction, Test
from patients.models import Patient
from doctors.models import Doctor
from users.models import User
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
def admin_login_view(request):
    form = Login_form()
    if request.method == "POST":
        form = Login_form(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(password)
            #Hàm auth có sẵn của django trong User class, đưa vào các tham số và trả về 1 obj hoặc None
            user = authenticate(request, username = username, password = password)
            # user_ = Site_admin.objects.get(username = username)
            # if (password == user_.password):
                # user_1 = User.objects.get(username = username)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('site_admin:home')
            # else:
            #     login(request, user)
            #     return redirect('../../')
        else:
            form = Login_form()
    return render(request, 'site_admins/login_view.html', {'form': form})

@login_required(login_url='site_admin:login')
def logout_account(request):
    logout(request)
    return redirect('site_admin:logout_page')


def logout_page(request):
    return render(request, 'site_admins/logout_page.html', {})

@login_required(login_url='site_admin:login')
def admin_home_view(request):
    return render(request, 'site_admins/home_page.html', {'admin': request.user.username})



@login_required(login_url='site_admin:login')
def patient_manage_view(request):
    #../?gender=man&gender=woman&province=Binh_thuan
    #Lấy các key có trong url gender, province
    url_params = request.GET.keys()
    #Luu trữ toàn bộ cặp key-value có trong url
    url_param_values = []
    #Duyệt để đẩy cặp key-value vào url_param_values
    for key in url_params:
        param_list = request.GET.getlist(key)
        for param in param_list:
            url_param_values.append([key, param])
            
    query = Q()
    query_temp = Q()
    sort = ""
    gender_conditions = []
    province_conditions = []
    age_conditions = []
    age = (0,0)
    #Duyệt các phần tử để thêm vào query
    for key, value in url_param_values:
        if key == "gender":
            gender_conditions.append(value)
        elif key == "province":
            province_conditions.append(value)
        elif key == "sort_by":
            sort = value
        elif key == "search_query":
            query &= Q(username__icontains = value)
        elif key == "age-start":
            age[1] = int(value)
        elif key == "age-end":
            age[1] = int(value)
        elif key == "age":
            age_conditions.append(value)
            # if value == "teen":
            #     query |= Q(new_age__lt = 19)
            # elif value == "adult":
            #     query |= Q(new_age__range = (20,59))
            # elif value == "elderly":
            #     query |= Q(new_age__gte = 60)
    for condition in gender_conditions:
        query_temp |= Q(gender = condition)
    if (query):
        query &= query_temp
    else:
        query = query_temp
    query_temp = Q()
    
    for condition in province_conditions:
        query_temp |= Q(province = condition)
        
    if (query_temp):
        query &= query_temp
        query_temp = Q()
    
    for condition in age_conditions:
        if condition == "teen":
            query_temp |= Q(new_age__lt = 19)
        elif condition == "adult":
            query_temp |= Q(new_age__range = (20,59))
        elif condition == "elderly":
            query_temp |= Q(new_age__gte = 60)
    if query_temp:
        query &= query_temp
    
    #Xử lý các query về tuổi
    # if age[0] == 0 and age[1] == 0:
    #     pass
    # elif age[0] == 0:
    #     query |= Q(age__lt = age[1])
    # elif age[1] == 0:
    #     query |= Q(age_gte = age[0])
    # else:
    #     query |= Q(age__range = range(age[0], age[1]))
        
    #Xử lí query sort
    results = Patient.objects.filter(query)
    if sort == "asc":
        results = results.order_by("username")
    elif sort == "des":
        results = results.order_by("-username")
    elif sort == "date_join":
        results = results.order_by("time_join")
    elif sort == "age":
        results = results.order_by("date_of_birth")
    
    provinces = [
        ('ho_chi_minh', 'TP. Hồ Chí Minh'),
        ('ha_noi', 'Hà Nội'),
        ('da_nang', 'Đà Nẵng'),
        ('hai_phong', 'Hải Phòng'),
        ('can_tho', 'Cần Thơ'),
        ('cao_bang','Cao Bằng'),
        ('an_giang', 'An Giang'),
        ('bac_giang', 'Bắc Giang'),
        ('bac_kan', 'Bắc Kạn'),
        ('bac_lieu', 'Bạc Liêu'),
        ('bac_ninh', 'Bắc Ninh'),
        ('ben_tre', 'Bến Tre'),
        ('binh_dinh', 'Bình Định'),
        ('binh_duong', 'Bình Dương'),
        ('binh_phuoc', 'Bình Phước'),
        ('binh_thuan', 'Bình Thuận'),
        ('ca_mau', 'Cà Mau'),
        ('cao_bang', 'Cao Bằng'),
        ('dak_lak', 'Đắk Lắk'),
        ('dak_nong', 'Đắk Nông'),
        ('dien_bien', 'Điện Biên'),
        ('dong_nai', 'Đồng Nai'),
        ('dong_thap', 'Đồng Tháp'),
        ('gia_lai', 'Gia Lai'),
        ('ha_giang', 'Hà Giang'),
        ('ha_nam', 'Hà Nam'),
        ('ha_tinh', 'Hà Tĩnh'),
        ('hai_duong', 'Hải Dương'),
        ('hau_giang', 'Hậu Giang'),
        ('hoa_binh', 'Hòa Bình'),
        ('hung_yen', 'Hưng Yên'),
        ('khanh_hoa', 'Khánh Hòa'),
        ('kien_giang', 'Kiên Giang'),
        ('kon_tum', 'Kon Tum'),
        ('lai_chau', 'Lai Châu'),
        ('lam_dong', 'Lâm Đồng'),
        ('lang_son', 'Lạng Sơn'),
        ('lao_cai', 'Lào Cai'),
        ('long_an', 'Long An'),
        ('nam_dinh', 'Nam Định'),
        ('nghe_an', 'Nghệ An'),
        ('ninh_binh', 'Ninh Bình'),
        ('ninh_thuan', 'Ninh Thuận'),
        ('phu_tho', 'Phú Thọ'),
        ('quang_binh', 'Quảng Bình'),
        ('quang_nam', 'Quảng Nam'),
        ('quang_ngai', 'Quảng Ngãi'),
        ('quang_ninh', 'Quảng Ninh'),
        ('quang_tri', 'Quảng Trị'),
        ('soc_trang', 'Sóc Trăng'),
        ('son_la', 'Sơn La'),
        ('tay_ninh', 'Tây Ninh'),
        ('thai_binh', 'Thái Bình'),
        ('thai_nguyen', 'Thái Nguyên'),
        ('thanh_hoa', 'Thanh Hóa'),
        ('thua_thien_hue', 'Thừa Thiên Huế'),
        ('tien_giang', 'Tiền Giang'),
        ('tra_vinh', 'Trà Vinh'),
        ('tuyen_quang', 'Tuyên Quang'),
        ('vinh_long', 'Vĩnh Long'),
        ('vinh_phuc', 'Vĩnh Phúc'),
        ('yen_bai', 'Yên Bái')
    ]
    if (results.count() == 0):
        context = {
            'provinces': provinces,
        }
        return render(request, "site_admins/patient_manage_page.html", context)
    num_patient_per_page = 3  
    #paginator: phân trang, num_patient: sô mục maximum hiển thị ở mỗi trang
    
    paginator = Paginator(results, num_patient_per_page)
    #Lấy số trang trên url để render phân trang tương ứng
    #Hiển thị 1 nếu không có
    page = request.GET.get('page', 1)
    #Xử lý các expection
    try:
        page_results = paginator.page(page)
    except PageNotAnInteger:
        page_results = paginator.page(1)
    except EmptyPage:
        page_results = paginator.page(paginator.num_pages)
        
    total_result_page = ceil((results.count())/num_patient_per_page)
    
    context = {
        'query_results': results,
        'page_results': page_results,
        'query_results_paginator': paginator,
        'total_result': results.count(),
        'total_page': total_result_page,
        'page_range': paginator.page_range,
        'provinces': provinces,
        'query_set': query,
        'admin': request.user,
        # 'query': param_values,
    }
    return render(request, "site_admins/patient_manage_page.html", context)

@login_required(login_url='site_admin:login')
def dashboard(request):
    patient_results = Patient.objects.filter(time_join__date = timezone.now().date())
    doctor_results = Doctor.objects.filter(time_join__date = timezone.now().date())
    appoint_results = Transaction.objects.filter(transaction_time__date = timezone.now().date())
    transact_amounts = 0
    for ap in appoint_results:
        transact_amounts += ap.amount_transact
    # months_label = get_months_list(12)
    twelve_months_ago = datetime.now().date() - timezone.timedelta(days=365)

    # months_label = [it['month'] for it in queryset]
    months_label = [month.month for month in get_months_list(12)]
    
    # queryset_get = [it['count'] for it in queryset ]
    queryset = Transaction.objects.annotate(month = TruncMonth('transaction_time')).values('month').annotate(count = Count("id")).filter(month__month__in = months_label)
    json_months_data = json.dumps(months_label)
    json_appointments_data = json.dumps(list(queryset), cls=DjangoJSONEncoder)
    context = {
        'patient_register_new': patient_results,
        'patient_register_new_total': patient_results.count(),
        'doctor_register_new': doctor_results,
        'doctor_register_new_total': doctor_results.count(),
        'total_appointments': appoint_results.count(),
        'total_amount_transact': transact_amounts,
        'months_list': json_months_data,
        'appointments_amount_list': json_appointments_data,
    }
    return render(request, "site_admins/dashboard_page.html", context)

#Data bệnh nhân row 1

@login_required(login_url='site_admin:login') #Yêu cầu login mới được vào, login sẽ lấy view trong login_url 
def new_patient_register_search_view(request):
    new_patient = None
    today = datetime.now().date()
    time_start = today
    time_range = request.GET.get('selected_value')
    if time_range == "today":
        new_patient = Patient.objects.filter(time_join__date = today)
    elif time_range == "cur-week":
        start_of_week = today - relativedelta(days = today.weekday())
        new_patient = Patient.objects.filter(time_join__gt = start_of_week)
    elif time_range == "cur-month":
        start_of_month = today - relativedelta(days = today.day - 1)
        new_patient = Patient.objects.filter(time_join__gt = start_of_month)
    elif time_range == "cur-year":
        start_of_year = today.replace(day = 1, month = 1)
        new_patient = Patient.objects.filter(time_join__gt = start_of_year) #
    
    data = {
        'total_registers': new_patient.count(),
    }
    return JsonResponse(data)

#Data bác sĩ row 1
@login_required(login_url='site_admin:login')
def new_doctor_register_search_view(request):
    new_doctor = None
    today = datetime.now().date()
    start_time = today
    time_range = request.GET.get('selected_value')
    if time_range == "today":
        pass
    elif time_range == "cur-week":
        start_time = today - relativedelta(days = today.weekday())
    elif time_range == "cur-month":
        start_time = today - relativedelta(days = today.day - 1)
    elif time_range == "cur-year":
        start_time = today.replace(day = 1, month = 1)
    
    new_doctor = Doctor.objects.filter(time_join__gt = start_time)
    
    #chuyển render sang dạng bit để trả về cho ajax
    # html = render(request, 'site_admins/search_new_register.html', context).content
    
    # data = {'html': html.decode('utf-8')}
    data = {
        'total_registers': new_doctor.count(),
    }
    return JsonResponse(data)

#Data lượt đặt hẹn trong khoảng thời gian 
@login_required(login_url='site_admin:login')
def new_appointment_view(request):
    new_appointment = None
    today = datetime.now().date()
    time_start = today
    time_range = request.GET.get('selected_value')
    if time_range == "today":
        pass
    elif time_range == "cur-week":
        time_start = today - relativedelta(days = today.weekday())
    elif time_range == "cur-month":
        time_start = today - relativedelta(days = today.day -1)
    elif time_range == "cur-year":
        time_start = today.replace(day = 1, month = 1)
    new_appointment = Transaction.objects.filter(transaction_time__gt = time_start)    
    data = {
        'total_appointments': new_appointment.count(),
    }
    return JsonResponse(data)


@login_required(login_url='site_admin:login')
def new_transaction_view(request):
    today = datetime.now().date()
    start_time = today
    time_range = request.GET.get('selected_value')
    if time_range == "today":
        pass
    elif time_range == "cur-week":
        start_time = today - relativedelta(days = today.weekday())
    elif time_range == "cur-month":
        start_time = today - relativedelta(days = today.day -1)
    elif time_range == "cur-year":
        start_time = today.replace(day = 1, month = 1)
        
    total_transacts = Transaction.objects.filter(transaction_time__gt = start_time).aggregate(total = Sum('amount_transact'))

    data = {
        'totals': total_transacts,
    }
    return JsonResponse(data)
def get_months_list(num_months_get):
    time_now = datetime.now().date() + relativedelta(days = - datetime.now().date().day)
    months = []
    for i in range(0,num_months_get):
        day = datetime.now().date() + relativedelta(months = - i)
        months.append(day)
        
    return months

def get_months_in_year(year):
    year_formatted = datetime.strptime(f"01/01/{year}", "%d/%m/%Y").date()
    # time_now = datetime.strptime(f"{year_formatted}-01-01", "%Y-%m-%d")
    months = []
    for i in range(1,13):
        month = year_formatted + relativedelta(month=i)
        months.append(month)
    return months

def test_json(request):
    cols =  ['a',"B","C","D"]
    rows = [10,20,30,40]
    json_cols = json.dumps((cols))
    # json_rows = json.dumps(list(rows))
    context = {
        'column': cols,
        'row': rows,
    }
    return render(request, "site_admins/test_json.html", context)

# def appoints_total_data(request):
#     selection = request.GET.get('selected_value')
#     months_list_num = []
#     months_list = []
#     if selection == "recent-12-months":
#         months_list = [month for month in get_months_list(12)][::-1]
#         months_list_num = [month.month for month in months_list]

#     elif selection == "2022":
#         months_list = [month for month in get_months_in_year(selection)]
#         months_list_num = [month.month for month in months_list]
#     appoints = Transaction.objects.annotate(month = TruncMonth('transaction_time')).values('month').annotate(count = Count("id")).filter(month__month__in = months_list_num)
#     month_in_results = [int(amount["month"].month) for amount in appoints]
#     results = []
#     for month in months_list_num:
#         if month not in month_in_results:
#             results.append(0)
#         else:
#             temp = appoints.get(month__month = month)
#             count = int(temp.get('count',0))
#             results.append(count)
#     data = {
#         'months': [month.strftime("%m-%Y") for month in months_list],
#         'appoints_list': list(results),
#     }
#     return JsonResponse(data)
    
#Data tổng lượng transact
def appoints_total_data(request):
    selection = request.GET.get('selected_value')
    months_list_num = []
    months_list = []
    if selection == "recent-12-months":
        months_list = [month for month in get_months_list(12)][::-1] #Đảo ngược thứ tự list lại dể đúng thứ tự, vì get_list_month đi ngược T12-T1
        months_list_formatted = [month.strftime("%m-%Y") for month in months_list] #Format lại theo mm/yyyy

    elif selection == "2022":
        months_list = [month for month in get_months_in_year(selection)]
        months_list_formatted = [month.strftime("%m-%Y") for month in months_list]
    # appoints = Transaction.objects.annotate(month = TruncMonth('transaction_time'), year = TruncYear('transaction_time')).values('month').annotate(count = Count("id")).filter(my_datetime_field__month__in=[d.month for d in months_list_num], my_datetime_field__year__in=[d.year for d in months_list_num])
    appoints = Transaction.objects.annotate(month=TruncMonth('transaction_time')) \
                            .annotate(year=ExtractYear('transaction_time')) \
                            .values('month', 'year')\
                            .annotate(total_transact=Sum('amount_transact'), count=Count('id'))
    results = []
    month_in_results = [appoint['month'].strftime("%m-%Y") for appoint in appoints]
    for month in months_list_formatted:
        if month not in month_in_results:
            results.append(0)
        else:
            temp = appoints.filter(month__month = int(month[0:1]))# month__year = int(month[-4:]))
    data = {
        'months': list(appoints),
        'appoints_list': list(results),
        'temp': list(temp),
    }
    return JsonResponse(data)

def appoints_state_data(request):
    selections = request.GET.get("selected_value")
    states = ["success", "failure", "confirming"]
    if selections == "recent-12-months":
        months_list = [month for month in get_months_list(12)][::-1]
        months_list_value = [month.month for month in months_list]
    else:
        months_list = [month for month in get_months_in_year(selections)]
        months_list_num = [month.month for month in months_list]
    time_start = months_list[0].replace(day = 1, month = 1)
    results = Transaction.objects.values('state').annotate(total = Sum('amount_transact')).filter(transaction_time__gte = time_start).order_by('total')
    json_obj = json.dumps(list(results))
    # json_obj = serializers.serialize('json', obj)
    labels = [result['state'] for result in results]
    values = [result['total'] for result in results][::-1]
    json_labels = json.dumps(list(labels))
    json_values = json.dumps(list(values))

    data = {
        'obj': json_obj,
        'labels': json_labels,
        'values': json_values,
    }
    return JsonResponse(data)

def specialities_table_data(request):
    selections = request.GET.get("selected_value")
    results = []
    if (selections == "this-week"):
        time_start = datetime.now().date() + relativedelta(days = -7)
        time_end = datetime.now().date() + relativedelta(days = 1)
        spec_top = Transaction.objects.values('medical_specialty__name')\
                            .annotate(count = Count('id'))\
                            .annotate(total = Sum('amount_transact'))\
                            .filter(transaction_time__gte = time_start, state = 'success', transaction_time__lt = time_end)\
                            .values('count', 'total', 'medical_specialty__name')\
                            .order_by('total')
        
    data = {
        'data': list(spec_top),
        'labels': [item['medical_specialty__name'] for item in spec_top],
        'amounts': [item['total'] for item in spec_top],
        'counts': [item['count'] for item in spec_top],
    }
    return JsonResponse(data)

def specialities_income_chart_data(request):
    selections = request.GET.get("selected_value")
    results = []
    time_labels = []
    today = datetime.now().date()
    if (selections == "weekly"): #Xử lý dữ liệu cho tuần mode
        time_start = today + relativedelta(weeks = -8)
        time_end = today + relativedelta(days = 1)
        start_of_week = today - relativedelta(days = today.weekday()) #Lấy ngày đầu tuần để truncweek gộp nhóm tính tổng trên mỗi nhóm
        for i in range(0,8):
            time_labels.append(start_of_week + relativedelta(weeks = -i)) #Lấy 8 tuần làm nhãn cho chart
        time_labels = time_labels[::-1]
        spec_top = Transaction.objects.annotate(time = TruncWeek('transaction_time'), year = TruncYear('transaction_time'))\
                            .annotate(count = Count('time'))\
                            .annotate(total = Sum('amount_transact'))\
                            .annotate(spec_total = Sum('medical_specialty'))\
                            .filter(transaction_time__gte = time_start, state = 'success', transaction_time__lt = time_end)\
                            .values('time','year','count', 'total','spec_total')
    else:
        time_start = today + relativedelta(months = -8)
        time_end = today + relativedelta(days = 1)
        start_of_month = today - relativedelta(days = today.day - 1)
        for i in range(0,8):
            time_labels.append(start_of_month + relativedelta(months = - i))
        time_labels = time_labels[::-1]
        spec_top = Transaction.objects\
                    .annotate(time = TruncMonth('transaction_time'))\
                    .annotate(year = TruncWeek('transaction_time'))\
                    .annotate(spec_total = 'medical_specialty')\
                    .annotate(count = Count('time'))\
                    .annotate(total = Sum('amount_transact'))\
                    .filter(transaction_time__gte = time_start, state = 'success', transaction_time__lt = time_end)\
                    .values('time','year','count', 'total', 'spec_total')
    # amounts = []
    # counts = []
    # for result in spec_top:
    #     if result['time'] not in TruncMonth(time_labels):
    #         a
    data = {
        'labels': [time for time in time_labels],
        'amounts': [item['total'] for item in spec_top],
        'counts': [item['spec_total'] for item in spec_top],
    }
    return JsonResponse(data)



def download_csv(request):
    id = request.GET.get('id')
    patient = Patient.objects.get(pk = id)
    # j_p = json.dumps(patient, )
    # transact_data = Transaction.objects.filter(id= patient.id).aggregate(count=Count('id'), total=Sum('amount_transact'))
    data = {
        'id': patient.id,
        'address': patient.address,
        'date_of_birth': patient.date_of_birth
    }
    # data_str = request.GET.get('data')
    # data = json.loads(data_str)
    # print(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'

    # Tạo writer CSV và ghi dữ liệu vào response
    writer = csv.writer(response)
    writer.writerow([data['id'], data['address'], data['date_of_birth']]) # Header của file CSV
    # for row in data:
        # writer.writerow([row['field1'], row['field2'], row['field3']]) # Ghi dữ liệu của từng row vào file CSV
    for i in range(0,10):
        writer.writerow([i, i+1, i+2])
    return response

def get_data_patient(request):
    id = request.GET.get('id')
    print(id)
    patient = Patient.objects.get(pk = id)
    # j_p = json.dumps(patient, )
    transact_data = Transaction.objects.filter(id= patient.id).aggregate(count=Count('id'), total=Sum('amount_transact'))
    data = {
        'id': patient.id,
        'name': patient.real_name,
        'address': patient.address,
        # 'avatar': patient.avatar.path,
        'date_of_birth': patient.date_of_birth,
        'phone': patient.phone,
        'province': patient.province,
        'gender': patient.gender,
        'citizen_id': patient.citizen_identification,
        'blood_gr': patient.blood_group,
        'account_status': patient.is_active,
        'patient_total': transact_data['total'],
        'patient_count': transact_data['count'],
    }
        # {'avartar': patient.avatar},
        # {'name': patient.real_name},
        # {'gender': patient.gender},
        # {'province': patient.province},
        # {'phone': patient.phone},
        # {'citizen_id': patient.citizen_identification},
        # {'blood_gr': patient.blood_group},
        # {'patient_total': transact_data['total']},
        # {'patient_count': transact_data['count']},
    return JsonResponse(data)

def get_data_patients(request):
    id_list_r = request.GET.get('id')   #Lấy id_list thô
    id_list_w = json.loads(id_list_r)   #Chuyển id_list thô thành list
    id_list = []
    for i in id_list_w: #Chuyển list str thành list int
        id_list.append(i)
    # transactions = Transaction.objects.filter(id__in = id_list).order_by('id').aggregate(count=Count('id'), total=Sum('amount_transact'))
    #Query các transaction có id trong id_list, kết quả trả về là 1 dict với trường id, total và count, sắp xếp theo id_list
    #annotate để gom nhóm lại theo id, tính tổng và đếm số lượng id của từng nhóm
    print(id_list)
    transactions = Transaction.objects.filter(id__in = id_list).values('id').annotate(count=Count('id'), total=Sum('amount_transact')).order_by('id')
    print(transactions)

    response = HttpResponse(content_type='text/csv') #Tạo response có type là csv
    response['Content-Disposition'] = 'attachment; filename="mydata.csv"'   #Cho biết response sẽ hiên thị 1 của sổ download file csv
    writer = csv.writer(response)   #Tạo writer csv để ghi dữ liệu vào response (csv)
    writer.writerow(["ID", "Address", "Date_of_birth"]) # Header của file CSV
    for transaction in transactions:
        writer.writerow([transaction['id'], transaction['count'], transaction['total']])
        print(transaction)

    return response

def delete_patient(request):
    id = request.GET.get('id')
    patient = Patient.objects.get(pk = id)
    patient.is_active = False
    patient.save()
    return JsonResponse({'status': 'success'})

def update_patient_info(request):
    id = request.POST.get('patient-id')
    name = request.POST.get('patient-name')
    address = request.POST.get('patient-address')
    phone = request.POST.get('patient-phone')
    account_status = request.POST.get('lock-status')
    uploaded_file = request.FILES['patient-avatar']
    #Tạo filename = thời gian hiện tại + tên file
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + uploaded_file.name
    #Tạo đường dẫn file, mediaroot là tương đối, lấy path prefix từ os.path.join
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
    #Lưu file vào thư mục uploads
    default_storage.save(file_path, uploaded_file)
    
    patient = Patient.objects.get(pk = id)

    patient.real_name = name
    patient.address = address
    patient.phone = phone
    patient.avatar = 'uploads/' + file_name
    if (account_status == 'on'):
        patient.is_active = True
    else:
        patient.is_active = False
    patient.save()
    return JsonResponse({'status': 'success'})


def add_patient(request):
    param = {}
    param['real_name'] = request.POST.get('new-patient-name')
    param['username'] = request.POST.get('new-patient-username')
    param['password'] = request.POST.get('new-patient-password')
    param['citizen_identification'] = request.POST.get('new-patient-ci_id')
    dob_str = request.POST.get('new-patient-dob')
    param['date_of_birth'] = datetime.strptime(dob_str, '%d/%m/%Y')
    param['phone'] = request.POST.get('new-patient-phone')
    param['gender'] = request.POST.get('new-patient-gender')
    param['province'] = request.POST.get('new-patient-province')
    param['address'] = request.POST.get('new-patient-address')
    param['blood_group'] = request.POST.get('new-patient-blood-gr')
    #Khởi tạo filepath
    file_path = ""
    #Lấy file từ request
    upload_file = request.FILES['new-patient-avatar']
    #Nếu có file
    if upload_file is not None:
        file_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_" + upload_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
        default_storage.save(file_path, upload_file) 
    #Không có file
    else:
        file_path = os.path.join(settings.MEDIA_ROOT, 'images', 'default.jpeg')
    param['avatar'] = file_path
    Patient.objects.create(**param) #Tạo patient mới với các tham số trong param, **param là unpack DICT param
    return JsonResponse({'status': 'success'})

def get_name_list_chosen_item(request):
    return JsonResponse({'status': 'success'})

def check_user_exist(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return JsonResponse({'status': 'not_exist'})
    
    return JsonResponse({'status': 'exist'})

def test_group(request):
    te = Test.objects.values('age').annotate(count=Count('id'))
    dat = []
    for t in te:
        dat.append(t['count'])
    data = {
        'data': dat,
    }
    return JsonResponse(data)

def appointment_manage_view(request):
    specializations = [('nha_khoa', 'Nha khoa'), ('tim_mach', 'Tim mạch'), ('da_lieu', 'Da liễu'), ('xuong_khop', 'Xương khớp'), ('mat', 'Mắt')]
    context = {
        'specializations': specializations,
    }
    return render(request, 'site_admins/appointment_manage.html', context)

def spec_manage_view(request):
    
    return render(request, 'site_admins/spec_manage.html', {})
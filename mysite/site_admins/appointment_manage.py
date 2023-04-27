from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Site_admin, Transaction
from patients.models import Patient
from doctors.models import Doctor,Specialties
from users.models import User
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.core.files.storage import default_storage
from math import ceil, floor
from .forms import Login_form
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum, Case, When, F, Value, CharField, DateField, IntegerField, DateTimeField
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear,ExtractMonth, ExtractYear, TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.conf import settings
import json
import calendar
import csv
import os


def get_appointment_amounts(request):
    selected_value = request.GET.get('selected_value')
    labels = []
    amounts = []
    today = datetime.now().date()
    step = 0
    cases = []
    if selected_value == "week":
        step = 1
    elif selected_value == "month":
        step = 4
    elif selected_value == "total":
        time_begin = datetime.strptime("01/01/2023", "%d/%m/%Y").date()
        step = ceil(((today- time_begin).days)/ 7)
    # elif selected_value == "weekly":
    #     date_list = [today - relativedelta(days = 7*i) for i in range(0,8)][::-1]
    #     labels = [label.strftime("%d/%m/%Y") for label in date_list]
    #     step = 7
    date_list = [today - relativedelta(days = step*i) for i in range(0, 8)][::-1]
    labels = [date.strftime("%d/%m/%Y") for date in date_list]

        
    for date in date_list:
        q = Q(appoint_time__date__range = (date - relativedelta(days = step - 1), date))
        cases.append(When(q, then = date))
        
    query_results = Transaction.objects.filter(appoint_time__date__range = (date_list[0], date_list[len(date_list)-1])).annotate(date_group = Case(*cases, default=None, output_field=DateField())).values('date_group').annotate(count = Count('id'))
    # amounts = [query_result['count'] for query_result in query_results]
    for date in date_list:
        if query_results.filter(date_group = date).exists():
            amounts.append(query_results.filter(date_group = date)[0]['count'])
        else:
            amounts.append(0)
    
    data = {
        'amounts': amounts,
        'labels': labels,
    }
    
    return JsonResponse(data)

def get_appointment_status_amounts(request):
    today = datetime.now().date()
    day_end = None
    labels = []
    amounts = []
    state_dict = dict(Transaction.appointment_state)
    selected_value = request.GET.get('selected_value')
    if selected_value == "week":
        day_end = today - relativedelta(days = 7)
    elif selected_value == "month":
        day_end = today - relativedelta(months = 1)
    elif selected_value == "total":
        day_end = datetime.strptime("01/01/2023", "%d/%m/%Y").date()
    
    query_results = Transaction.objects.filter(appoint_time__date__range = (day_end, today)).values('state').annotate(count = Count('id')).order_by('-count')
    
    for query in query_results:
        amounts.append(query['count'])
        labels.append(state_dict[query['state']])  
    data = {
        'labels': labels,
        'amounts': amounts,
    }
    return JsonResponse(data)

def trans_day(time1, time2):
    year1 = time1.year
    year2 = time2.year
    month1 = time1.month
    month2 = time2.month
    day1 = time1.day
    day2 = time2.day
    time1 = time1.replace(year = year2, month = month2, day = day2)
    time2 = time2.replace(year = year1, month = month1, day = day1)
    # print(time1, time2)
    return time1, time2
#Mode 0: từ hiện tại lấy về, mode 1: từ hiện tại +1 sec lấy tới
def format_time_for_chart(time_start, time_end, time_now, now, mode):
    if mode == 1:
        time_start = time_start.replace(hour = time_now.hour, minute = time_now.minute, second = time_now.second+1)
        time_end = time_end.replace(hour = 23, minute = 59, second = 59)
        #Đảm bảo chỉ lấy từ hien tai + 1 second, start < end
        if time_start > time_end:
            #Đảm bảo start < end, nếu start > end thì hoán đổi ngày tháng năm cho nhau, giữ nguyên thời gian
            time_start, time_end = trans_day(time_start, time_end)
        
        if time_start <= now:
            time_start = now + timedelta(seconds = 1)
    elif mode == -1:
        time_start = time_start.replace(hour = 0, minute = 0, second = 0)
        time_end = time_end.replace(hour = 23, minute = 59, second = 59)
        if time_start > time_end:
            time_start, time_end = trans_day(time_start, time_end)
        if time_end > now:
            time_end = now
    else:
        print("Loi mode, chỉ 0 hoặc 1")
    return time_start, time_end

def get_time_step(time_start, time_end, step):
    steps = (time_end - time_start).total_seconds()/step
    return steps 
def upcoming_appoint_chart_data(request):    
    selected_value = request.GET.get('selected_value')
    now = datetime.strptime(datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
    time_start = now
    time_end = now
    times = []
    labels = [] 
    amounts = []
    cases = []
    step = 0
    if selected_value == "custom":
        time_start = datetime.strptime(request.GET.get('time_start'), "%Y-%m-%d")
        time_end = datetime.strptime(request.GET.get('time_end'), "%Y-%m-%d")
        time_now = datetime.strptime(request.GET.get('time_now'), "%H:%M:%S")
        #Chỉnh time_start, time_end để đảm bảo now < time_start < time_end
        time_start, time_end = format_time_for_chart(time_start, time_end, time_now, now, 1)
        time_delta = time_end - time_start
        time_delta_seconds = time_delta.total_seconds()
        step = floor(time_delta_seconds/5)
        times = [time_start + timedelta(seconds = step*i) for i in range(1,6)]
        times[len(times)-1].replace(second=59)
    else:
        #Lấy thời gian bắt đầu
        time_start = now + relativedelta(seconds = 1)
        #Lấy thời gian kết thúc
        if selected_value == "next-7-days":
            time_end = now + relativedelta(days = 6)
        elif selected_value == "next-30-days":
            time_end = now + relativedelta(days = 29)
        time_end = time_end.replace(hour = 23, minute = 59, second = 59)
        step = (time_end - time_start).total_seconds()/5
        #Lấy 5 mốc time
        times = [time_start + timedelta(seconds = step*i) for i in range(1,6)]
    labels = [time.strftime("%d/%m/%Y") for time in times] #Chỉ hiển thị ngày
    time_delta = (times[1] - times[0]).total_seconds() - 1  #Lấy lượng thời gian chênh lệch
    for time in times:
        q = Q(appoint_time__range = (time - timedelta(seconds = time_delta), time))
        cases.append(When(q, then = time))
    print(times)
    
    #Lọc trước rồi lấy điều kiện theo khoảng sau, ngày thừa trong khoảng sẽ k có gì, lấy labal là ngày đầu khoảng
    query_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), state = 'waiting').annotate(date_group = Case(*cases, default=None)).values('date_group').annotate(count = Count('id'))
    table_data_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), state = 'waiting').select_related('doctor', 'patient')
    row = []
    table_data = []
    for table_data_result in table_data_results:
        row = [table_data_result.id_transaction, table_data_result.doctor.real_name, table_data_result.patient.real_name, table_data_result.appoint_time.strftime("%d/%m/%Y %H:%M:%S"), table_data_result.amount_transact, table_data_result.medical_specialty.get_name_display()]
        table_data.append(row)
    for time in times:  
        if query_results.filter(date_group = time).exists():
            amounts.append(query_results.filter(date_group = time)[0]['count'])
        else:
            amounts.append(0)
    table_data_json = json.dumps(table_data)
    # print(time_start, time_end)
    data = {
        'line_c_amounts': amounts,
        'line_c_labels': labels,
        'table_data': table_data_json,
    }
    # print(table_data)
    return JsonResponse(data)

def success_appoint_chart_data(request):
    selected_value = request.GET.get('selected_value')
    now = datetime.strptime(datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M:%S'), '%d/%m/%Y %H:%M:%S')
    time_start = now
    time_end = now
    times = []
    # labels = []
    amounts = []
    cases = []
    step = 0
    if selected_value == "custom":
        time_start = datetime.strptime(request.GET.get('time_start'), "%Y-%m-%d")
        time_end = datetime.strptime(request.GET.get('time_end'), "%Y-%m-%d")
        time_now = datetime.strptime(request.GET.get('time_now'), "%H:%M:%S")
        time_start, time_end = format_time_for_chart(time_start, time_end, time_now, now, -1)
    else:
        
        if selected_value == "7-days-before":
            time_end = now
            time_start = now + relativedelta(days = -7) #Lấy 6 ngày trước
            time_start.replace(hour = 00, minute = 00, second = 1) #Thời gian bắt đầu từ đầu ngày
        elif selected_value == "30-days-before":
            time_end = now
            time_start = now + relativedelta(days = -30) #Lấy 30 ngày trước
            time_start.replace(hour = 00, minute = 00, second = 1)
    step = get_time_step(time_start, time_end, 5)
    times = [time_start + timedelta(seconds = step*i) for i in range(1,6)]
    labels = [time.strftime("%d/%m/%Y") for time in times] #Chỉ hiển thị ngày
    time_delta = (times[1] - times[0]).total_seconds() - 1  #Lấy lượng thời gian chênh lệch
    for time in times:
        q = Q(appoint_time__range = (time - timedelta(seconds = step), time))
        cases.append(When(q, then = time))
    query_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), state = "success").annotate(date_group = Case(*cases, default=None)).values('date_group').annotate(count = Count('id'))
    table_data_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), state = 'success').select_related('doctor', 'patient')
    #Thêm 0 vào những time không có
    for time in times:
        if query_results.filter(date_group = time).exists():
            amounts.append(query_results.filter(date_group = time)[0]['count'])
        else:
            amounts.append(0)
    table_data = []
    temp = []
    for result in table_data_results:
        # temp = [result.id_transaction, result.doctor.real_name, result.patient.real_name, result.appoint_time.strftime('%d/%m/%Y %H:%M:%S'), result.amount_transact, result.medical_specialty.get_name_display(), result.canceled_details.reason, result.canceled_details.canceler]
        temp = [result.id_transaction, result.doctor.real_name, result.patient.real_name, result.appoint_time.strftime('%d/%m/%Y %H:%M:%S'), result.appoint_time.strftime('%d/%m/%Y %H:%M:%S'),result.amount_transact, result.medical_specialty.get_name_display()]
        table_data.append(temp)
    data = {
        'amounts': amounts,
        'labels': labels,
        'table_data': json.dumps(table_data),
    }
    return JsonResponse(data)
def failed_appoint_chart_data(request):
    selected_value = request.GET.get('selected_value')
    now = datetime.now()
    time_start = now
    time_end = now
    times = []
    # labels = []
    amounts = []
    cases = []
    step = 0
    if selected_value == "custom":
        time_start = datetime.strptime(request.GET.get('time_start'), "%Y-%m-%d")
        time_end = datetime.strptime(request.GET.get('time_end'), "%Y-%m-%d")
        time_now = datetime.strptime(request.GET.get('time_now'), '%H:%M:%S')
        if time_start > time_end:
            time_start, time_end = time_end, time_start
        #Khoang thoi gian giua 2 thoi diem
    else:
        if selected_value == "7-days-next":
            time_start = now + timedelta(seconds=1)
            time_end = now + relativedelta(days = 7)
            time_end.replace(hour = 23, minute = 59, second = 59)
        
        elif selected_value == "7-days-before":
            time_end = now
            time_start = now + relativedelta(days = -7) #Lấy 5 ngày trước
            time_start.replace(hour = 00, minute = 00, second = 1) #Thời gian bắt đầu từ đầu ngày
    step = get_time_step(time_start, time_end, 5)
    times = [time_start + timedelta(seconds = step*i) for i in range(1,6)]
    labels = [time.strftime("%d/%m/%Y") for time in times] #Chỉ hiển thị ngày
    
    # time_delta = (times[1] - times[0]).total_seconds() - 1  #Lấy lượng thời gian chênh lệch
    for time in times:
        q = Q(appoint_time__range = (time - timedelta(seconds = step - 1), time))
        cases.append(When(q, then = time))
    query_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), state = "failure").annotate(date_group = Case(*cases, default=None)).values('date_group').annotate(count = Count('id'))
    table_data_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), state = 'failure').select_related('doctor', 'patient', 'canceled_details')
    table_data = []
    for result in table_data_results:
        temp = [result.id_transaction,
                result.doctor.real_name,
                result.patient.real_name,
                result.appoint_time.strftime('%d/%m/%Y %H:%M:%S'),
                result.canceled_details.time_cancel.strftime('%d/%m/%Y %H:%M:%S'),
                result.amount_transact,
                result.medical_specialty.get_name_display(),
                result.canceled_details.reason,
                result.canceled_details.get_canceler_display()]
        table_data.append(temp)
        
    #Thêm 0 vào những vị trí time tương ứng không có
    for time in times:
        if query_results.filter(date_group = time).exists():
            amounts.append(query_results.filter(date_group = time)[0]['count'])
        else:
            amounts.append(0)
    data = {
        'amounts': amounts,
        'labels': labels,
        'table_data': json.dumps(table_data),
    }
    return JsonResponse(data)

def spec_appoint_chart_data(request):
    selected_value = request.GET.get('selected_value')
    now = datetime.now()
    time_start = now
    time_end = now
    times = []
    labels = []
    amounts = []
    cases = []
    step = 0
    if selected_value == "custom":
        time_start = datetime.strptime(request.GET.get('time_start'), "%d/%m/%Y %H:%M:%S")
        time_end = datetime.strptime(request.GET.get('time_end'), "%d/%m/%Y %H:%M:%S")
        if time_start > time_end:
            time_start, time_end = time_end, time_start
        time_delta = time_end - time_start
        #Khoang thoi gian giua 2 thoi diem
        time_delta_seconds = time_delta.total_seconds()
        step = time_delta_seconds/5
        times = [time_start + timedelta(seconds = step*i) for i in range(1,6)]
    else:
        if selected_value == "7-days-next":
            time_start = now + timedelta(seconds=1)
            time_end = now + relativedelta(days = 5)
            time_end.replace(hour = 23, minute = 59, second = 59)
        
        elif selected_value == "7-days-before":
            time_end = now
            time_start = now + relativedelta(days = -5) #Lấy 5 ngày trước
            time_start.replace(hour = 00, minute = 00, second = 1) #Thời gian bắt đầu từ đầu ngày
    step = get_time_step(time_start, time_end, 5) #Trả về khoảng sec giữa 2 mốc liên tiếp
    #Lấy các khoảng thời gian
    times = [time_start + timedelta(seconds= step*i) for i in range(1,6)]
    labels = [time.strftime("%d/%m/%Y") for time in times] #Chỉ hiển thị ngày
    time_delta = (times[1] - times[0]).total_seconds() - 1  #Lấy lượng thời gian chênh lệch là second để tiện xử lý chỉ cần trừ sec là được, không cần chuyển sang các giá trị day,...
    for time in times:
        q = Q(appoint_time__range = (time - timedelta(seconds = time_delta), time))
        cases.append(When(q, then = time))
    
    spec_value = request.GET.get('spec_value')
    spec_value_arr = []
    spec_value_label = {'nha_khoa': 'Nha Khoa','da_lieu': 'Da Liêu','tim_mach': 'Tim Mạch','mat': 'Mắt','xuong_khop': 'Xương Khớp'}
    if spec_value != None:
        spec_value_arr = spec_value.split(',')
    if spec_value == "all":
        #Tfìm csách lấy tất cả các giá trị của medical_specialty
        spec_value_arr = ['nha_khoa', 'da_lieu', 'tim_mach', 'mat', 'xuong_khop']
    query_results = Transaction.objects.filter(appoint_time__range = (time_start, time_end), medical_specialty__in = spec_value_arr).annotate(date_group = Case(*cases, default = None)).annotate(spec = F('medical_specialty__name')).values('date_group', 'spec').annotate(count = Count('id'))
    pie_chart_data = {}
    spec_labels = []
    for spec in spec_value_arr:
        temp = []
        sums = 0
        if query_results.filter(spec = spec).exists():
            for time in times:
                if query_results.filter(spec = spec, date_group = time).exists():
                    counts = query_results.filter(spec = spec, date_group = time)[0]['count']
                    temp.append(counts)
                    sums = sums + counts
                else:
                    temp.append(0)
            amounts.append(temp)
            spec_labels.append(spec_value_label[query_results.filter(spec = spec)[0]['spec']])
            pie_chart_data[spec] = sums
    #Sắp xêp lại dữ liệu cho pie chart để hiển thị đúng cách biểu đồ nên hiển thị và theo thứ tự giảm dần; chuyển kiểu dữ liệu từ dict sang list
    pie_chart_data = sorted(pie_chart_data.items(), key = lambda x: x[1], reverse = True)
    pie_c_labels = [spec_value_label[item[0]] for item in pie_chart_data]
    pie_c_amounts = [item[1] for item in pie_chart_data]
    data = {
        'labels': labels,
        'spec_labels': spec_labels,
        'spec_value_arr': spec_value_arr,
        'amounts': amounts,
        'pie_c_labels': pie_c_labels,
        'pie_c_amounts': pie_c_amounts,
    }
    return JsonResponse(data)

def dispose_appoint_chart_data(request):
    
    return JsonResponse({'success': 'true'})




def upcoming_appoint_table_row_data(request):
    pass
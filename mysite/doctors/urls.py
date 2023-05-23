from django.urls import path, include

from .views import (
    dashboard,
    doctor_login_view,
    my_patient,
    review,
    invoice,
)

from .dashboard import (
    get_doctor,
    get_earn_money,
    get_money_left,
    get_total_patient,
    get_total_appointment,
    get_rate,
    get_appoint_next,
    update_doctor_info,
    get_appoint_table_data,
    get_transaction_detail,
)

from .my_patient import (
    get_patient,
)
from .review import (
    get_review_data,
    get_invoice,
)
app_name = "doctor"

urlpatterns = [
    path('dashboard/', dashboard, name = 'dashboard'),
    path('login/', doctor_login_view, name = 'login'),
    path('my-patient/', my_patient, name = 'my-patient'),
    path('review/', review, name = 'review'),
    path('invoice/', invoice, name = 'invoice'),
    path('get-doctor/', get_doctor),
    path('get-earn-money/', get_earn_money),
    path('get-money-left/', get_money_left),
    path('get-total-patient/', get_total_patient),
    path('get-total-appointment/', get_total_appointment),
    path('get-rate/', get_rate),
    path('get-appoint-next/', get_appoint_next),
    path('update-doctor-info/', update_doctor_info),
    path('get-appoint-table-data/', get_appoint_table_data),
    path('get-transaction-detail/', get_transaction_detail),
    path('get-patient/', get_patient),
    path('get-review-data/', get_review_data),
    path('get-invoice/', get_invoice),
]
from django.urls import path, include

from .views import (
    dashboard,
    doctor_login_view,
    my_patient,
    review,
    invoice,
    get_notification,
    approving_appoint,
    add_notification,
    update_appoint_status_all,
    set_status_appointment,
    update_notification,
    get_notification,
    logout_view as logout,
    test_o,
    get_doctor_info,
    settings,
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
    check_next_appoint,
    get_next_appoint_id,
    check_upcoming_appoint,
)

from .my_patient import (
    get_patient,
)
from .review import (
    get_review_data,
    get_invoice,
)

from .approving_appoint import (
    get_confirming_appoint,
    update_appoint_status,
    test,
    
)

from .setting_page import (
    save_change,
)
app_name = "doctor"

urlpatterns = [
    path('dashboard/', dashboard, name = 'dashboard'),
    path('login/', doctor_login_view, name = 'login'),
    path('my-patient/', my_patient, name = 'my-patient'),
    path('review/', review, name = 'review'),
    path('invoice/', invoice, name = 'invoice'),
    path('logout/', logout, name = 'logout'),
    path('upcoming-appoint/', approving_appoint, name = 'approving-appoint'),
    path('settings/', settings, name = 'settings'),
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
    path('get-notification/', get_notification),
    path('get-confirming-appointment/', get_confirming_appoint),
    path('update-appointment-status/', update_appoint_status),
    path('test/', test_o),
    path('check-next-appoint/', check_next_appoint),
    path('get-next-appoint-id/', get_next_appoint_id),
    path('add-notification/', add_notification),
    path('update-appoint-status-all/', update_appoint_status_all),
    path('set-status-appointment/', set_status_appointment),
    path('check-upcoming-appoint/', check_upcoming_appoint),
    path('update-notification/', update_notification),
    path('get-notification/', get_notification),
    path('get-doctor-info/', get_doctor_info),
    path('save-change/', save_change),
]
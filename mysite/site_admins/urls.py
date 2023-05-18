from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include
from .views import (admin_login_view,
                    admin_home_view,
                    patient_manage_view,
                    dashboard,
                    appointment_manage_view,
                    spec_manage_view,
                    transaction_manage_view,
                    doctor_manage_view,
                    new_patient_register_search_view,
                    new_doctor_register_search_view,
                    new_transaction_view,
                    new_appointment_view,
                    logout_account,
                    logout_page,
                    test_json,
                    appoints_total_data,
                    appoints_state_data,
                    download_csv,
                    get_data_patient,
                    get_data_patients,
                    delete_patient,
                    update_patient_info,
                    add_patient,
                    get_name_list_chosen_item,
                    get_notification_data,
                    )
from .patient_views import (
                    update_overview_chart,
                    update_overview_reg_chart,
                    get_new_register_amount,
                    get_account_status,
                    get_patient_table,
                    update_patient_status,
                    )

from .appointment_manage import (
    get_appointment_amounts,
    get_appointment_status_amounts,
    upcoming_appoint_chart_data,
    failed_appoint_chart_data,
    success_appoint_chart_data,
    spec_appoint_chart_data,
    dispose_appoint_chart_data,
    
)   
from .spec import (
    get_spec_data,
)
from .transaction import (
    get_transaction_data,
)
from .dashboard import (
    specialities_table_data,
    specialities_income_chart_data,
    get_spec_overview_table_data,
    
)
from .doctor import (
    get_doctor_table_data,
)
app_name = "site_admin"

urlpatterns = [
    path('login/', admin_login_view, name = "login"),
    path('home/',  admin_home_view, name = "home"),
	path('patient-manage/', patient_manage_view, name = "patient"),
    path('dashboard/', dashboard, name = "dashboard"),
    path('appointment-manage/', appointment_manage_view, name = "appointment"),
    path('spec-manage/', spec_manage_view, name = "spec_manage"),
    path('transaction-manage/', transaction_manage_view, name = "transaction_manage"),
    path('doctor-manage/', doctor_manage_view, name = "doctor"),
    path('get-new-data/', new_patient_register_search_view, name = "total_new_patient"),
    path('get-new-data-doctor/', new_doctor_register_search_view, name = "total_new_doctor"),
    path('get-new-data-transaction/', new_transaction_view, name = "total_new_transaction"),
    path('get-new-data-booking/', new_appointment_view, name = "total_new_appointment"),
    path('lg', logout_account, name = "logout_link"),
    path('logout/', logout_page, name = "logout_page"),
    path('appoints-state-data/', appoints_state_data),
    path('appoints-total/', appoints_total_data),
    path('specialities_table_data/', specialities_table_data),
    path('spec-income-chart-data/', specialities_income_chart_data),
    path('export-file/', download_csv),
    path('get-data-patient/', get_data_patient),
    path('get-data-patients/', get_data_patients),
    path('delete-patient/', delete_patient),
    path('update-patient-info/', update_patient_info),
    path('add-patient/', add_patient),
    path('get-name-list-chosen-item/', get_name_list_chosen_item),
    path('update-overview-chart/', update_overview_chart),
    path('update-overview-reg-chart/', update_overview_reg_chart),
    path('get-new-register-amount/', get_new_register_amount),
    path('get-account-status/', get_account_status),
    path('get-appointment-amounts/', get_appointment_amounts),
    path('get-appointment-status-amounts/', get_appointment_status_amounts),
    path('upcoming-appoint-chart-data/', upcoming_appoint_chart_data),
    path('success-appoint-chart-data/', success_appoint_chart_data),
    path('failed-appoint-chart-data/', failed_appoint_chart_data),
    path('spec-appoint-chart-data/', spec_appoint_chart_data),
    path('dispose-appoint-chart-data/', dispose_appoint_chart_data),
    path('get-spec-data/', get_spec_data),
    path('get-transactions-data/', get_transaction_data),
    path('get-patient-table/', get_patient_table),
    path('update-patient-status/', update_patient_status),
    path('get-spec-overview-table-data/', get_spec_overview_table_data),
    path('get-doctor-table-data/', get_doctor_table_data),
    path('get-notification-data/', get_notification_data),
]

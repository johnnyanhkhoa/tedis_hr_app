from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee/', views.employee_table, name='employee_table'),
    path('employee_create_new/', views.create_new_employee, name='create_new_employee'),
    path('employee_information/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('add_staff_for_manager/<int:pk>/', views.add_staff_for_manager, name='add_staff_for_manager'),
    path('staff_delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('add_children/<int:pk>/', views.add_children, name='add_children'),
    path('add_contract/<int:pk>/', views.add_contract, name='add_contract'),
    path('add_promotion/<int:pk>/', views.add_promotion, name='add_promotion'),
    path('probationary_period_form/<int:pk>/', views.probationary_period_form, name='probationary_period_form'),
    path('TD_job_offer_PDF/<int:pk>/', views.TD_job_offer_PDF, name='TD_job_offer_PDF'),
    path('JV_job_offer_PDF/<int:pk>/', views.JV_job_offer_PDF, name='JV_job_offer_PDF'),
    path('VH_job_offer_PDF/<int:pk>/', views.VH_job_offer_PDF, name='VH_job_offer_PDF'),
    path('JV_HDLD_PDF/<int:pk>/', views.JV_HDLD_PDF, name='JV_HDLD_PDF'),
    path('VH_HDLD_PDF/<int:pk>/', views.VH_HDLD_PDF, name='VH_HDLD_PDF'),
    path('RO_HDLD_PDF/<int:pk>/', views.RO_HDLD_PDF, name='RO_HDLD_PDF'),
    path('leave_application/', views.leave_application, name='leave_application'),
    path('leave_view/<int:pk>/', views.leave_view, name='leave_view'),
    path('leave_verification/', views.leave_verification, name='leave_verification'),
    path('leave_approve/<int:pk>/', views.leave_approve, name='leave_approve'),
    path('HR_leave_approve/<int:pk>/', views.HR_leave_approve, name='HR_leave_approve'),
    path('ot_application/', views.ot_application, name='ot_application'),
    path('ot_verification/', views.ot_verification, name='ot_verification'),
    path('ot_approve/<int:pk>/', views.ot_approve, name='ot_approve'),
    # Period and Dayoff
    path('blank_period/', views.blank_period, name='blank_period'),
    path('period/<int:pk>/', views.period, name='period'),
    path('list_time_sheets/<int:pk>/', views.list_time_sheets, name='list_time_sheets'),
    path('pdf_time_sheets/<int:pk>/', views.pdf_time_sheets, name='pdf_time_sheets'),
    # Payroll
    path('payroll_tedis/<int:pk>/', views.payroll_tedis, name='payroll_tedis'),
    path('payroll_tedis_edit/<int:pk>/', views.payroll_tedis_edit, name='payroll_tedis_edit'),
    path('payroll_tedis_vietha/<int:pk>/', views.payroll_tedis_vietha, name='payroll_tedis_vietha'),
    path('payroll_tedis_vietha_edit/<int:pk>/', views.payroll_tedis_vietha_edit, name='payroll_tedis_vietha_edit'),
    path('payroll_vietha/<int:pk>/', views.payroll_vietha, name='payroll_vietha'),
    path('payroll_vietha_edit/<int:pk>/', views.payroll_vietha_edit, name='payroll_vietha_edit'),
    # Report Payroll
    path('report_payroll_tedis/<int:pk>/', views.report_payroll_tedis, name='report_payroll_tedis'),
    # Report leave
    path('report_leave/<int:pk>/', views.report_leave, name='report_leave'),
    # path('dayoff/', views.dayoff, name='dayoff'),
    
    
]

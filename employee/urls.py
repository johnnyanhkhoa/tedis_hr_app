from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee/', views.employee_table, name='employee_table'),
    path('employee_create_new/', views.create_new_employee, name='create_new_employee'),
    path('employee_information/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_resign/<int:pk>/', views.employee_resign, name='employee_resign'),
    path('add_staff_for_manager/<int:pk>/', views.add_staff_for_manager, name='add_staff_for_manager'),
    path('edit_manager/<int:pk>/', views.edit_manager, name='edit_manager'),
    path('staff_delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('add_children/<int:pk>/', views.add_children, name='add_children'),
    path('view_relatives/<int:pk>/', views.view_relatives, name='view_relatives'),
    path('edit_relatives/<int:pk>/', views.edit_relatives, name='edit_relatives'),
    path('relative_delete/<int:pk>/', views.relative_delete, name='relative_delete'),
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
    # Tedis
    path('report_payroll_tedis/<int:pk>/', views.report_payroll_tedis, name='report_payroll_tedis'),
    path('PIT_report_payroll_tedis_edit/<int:pk>/', views.PIT_report_payroll_tedis_edit, name='PIT_report_payroll_tedis_edit'),
    path('payment_report_payroll_tedis_edit/<int:pk>/', views.payment_report_payroll_tedis_edit, name='payment_report_payroll_tedis_edit'),
    path('payment_report_payroll_tedis_delete/<int:pk>/', views.payment_report_payroll_tedis_delete, name='payment_report_payroll_tedis_delete'),
    # Tedis-VietHa
    path('report_payroll_tedis_vietha/<int:pk>/', views.report_payroll_tedis_vietha, name='report_payroll_tedis_vietha'),
    path('PIT_report_payroll_tedis_vietha_edit/<int:pk>/', views.PIT_report_payroll_tedis_vietha_edit, name='PIT_report_payroll_tedis_vietha_edit'),
    path('payroll_ser_edit/<int:pk>/', views.payroll_ser_edit, name='payroll_ser_edit'),
    path('payment_report_payroll_tedis_vietha_edit/<int:pk>/', views.payment_report_payroll_tedis_vietha_edit, name='payment_report_payroll_tedis_vietha_edit'),
    path('new_staff_report_payroll_tedis_vietha_edit/<int:pk>/', views.new_staff_report_payroll_tedis_vietha_edit, name='new_staff_report_payroll_tedis_vietha_edit'),
    path('confirmed_after_probation_report_payroll_tedis_vietha_edit/<int:pk>/', views.confirmed_after_probation_report_payroll_tedis_vietha_edit, name='confirmed_after_probation_report_payroll_tedis_vietha_edit'),
    path('resigned_staff_report_payroll_tedis_vietha_edit/<int:pk>/', views.resigned_staff_report_payroll_tedis_vietha_edit, name='resigned_staff_report_payroll_tedis_vietha_edit'),
    path('other_changes_report_payroll_tedis_vietha_edit/<int:pk>/', views.other_changes_report_payroll_tedis_vietha_edit, name='other_changes_report_payroll_tedis_vietha_edit'),
    path('maternity_leave_report_payroll_tedis_vietha_edit/<int:pk>/', views.maternity_leave_report_payroll_tedis_vietha_edit, name='maternity_leave_report_payroll_tedis_vietha_edit'),
    path('reconcile_report_payroll_tedis_vietha_edit/<int:remark_id>/', views.reconcile_report_payroll_tedis_vietha_edit, name='reconcile_report_payroll_tedis_vietha_edit'),
    # Report leave
    path('report_leave/', views.report_leave, name='report_leave'),
    # path('dayoff/', views.dayoff, name='dayoff'),
    
    
]

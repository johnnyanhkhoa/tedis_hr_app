from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee/', views.employee_table, name='employee_table'),
    path('employee_information/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('add_children/<int:pk>/', views.add_children, name='add_children'),
    path('add_contract/<int:pk>/', views.add_contract, name='add_contract'),
    path('add_promotion/<int:pk>/', views.add_promotion, name='add_promotion'),
    path('TD_probationary_period_form/<int:pk>/', views.TD_probationary_period_form, name='TD_probationary_period_form'),
    path('TD_job_offer_FORM/<int:pk>/', views.TD_job_offer_FORM, name='TD_job_offer_FORM'),
    path('JV_job_offer_FORM/<int:pk>/', views.JV_job_offer_FORM, name='JV_job_offer_FORM'),
    path('TD_job_offer_PDF/<int:pk>/', views.TD_job_offer_PDF, name='TD_job_offer_PDF'),
    path('JV_job_offer_PDF/<int:pk>/', views.JV_job_offer_PDF, name='JV_job_offer_PDF'),
    
    
]

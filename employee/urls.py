from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee/', views.employee_table, name='employee_table'),
    path('employee_information/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('add_children/<int:pk>/', views.add_children, name='add_children'),
    path('probationary_period_form/<int:pk>/', views.probationary_period_form, name='probationary_period_form'),
    path('job_offer_form/<int:pk>/', views.job_offer_form, name='job_offer_form'),
    path('html_to_pdf_view/<int:pk>/', views.html_to_pdf_view, name='html_to_pdf_view'),
    
    
]

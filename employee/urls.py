from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee/', views.employee_table, name='employee_table'),
    path('employee_information/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('add_children/<int:pk>/', views.add_children, name='add_children'),
    
    
]

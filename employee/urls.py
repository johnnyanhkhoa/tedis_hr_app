from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee/<int:pk>/', views.employee_table, name='employee_table'),
    # path('index/', views.index, name='index'),
    
    
]

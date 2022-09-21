from django.urls import path, include
from employee import views

app_name = 'employee'
urlpatterns = [
    path('employee_table/', views.employee_table, name='employee_table'),
    # path('signup/', views.signup_changepassword, name='signup_changepassword'),
    # path('index/', views.index, name='index'),
    
    
]

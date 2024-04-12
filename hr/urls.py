from django.urls import path, include
from hr import views

app_name = 'hr'
urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup_changepassword, name='signup_changepassword'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('guide/', views.guide, name='guide'),
    path('guide_leave_and_overtime/', views.guide_leave_and_overtime, name='guide_leave_and_overtime'),
    path('guide_employee_information/', views.guide_employee_information, name='guide_employee_information'),
    
    
    
]

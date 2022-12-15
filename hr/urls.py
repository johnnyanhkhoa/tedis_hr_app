from django.urls import path, include
from hr import views

app_name = 'hr'
urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup_changepassword, name='signup_changepassword'),
    path('logout/', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    
    
    
]

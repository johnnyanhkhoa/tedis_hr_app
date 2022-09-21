from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from hr.models import User
from hr.forms import FormDangKy, FormDoiMatKhau
from datetime import datetime

# Create your views here.
def employee_table(request): 
    
    return render(request, 'hr/dist/table-datatable.html', {
        
    })
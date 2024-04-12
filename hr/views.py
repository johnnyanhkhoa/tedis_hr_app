from django.shortcuts import render, redirect
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from hr.models import User
from hr.forms import FormDangKy, FormDoiMatKhau
from datetime import datetime
from employee.models import *

# Create your views here.
def index(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    user_info = User.objects.all()
    s_user = request.session.get('s_user')
    role = s_user[1]
    employee_pk = s_user[2]
    # Lấy thông tin employee và Dayoff
    try:
        employee = Employee.objects.get(pk=employee_pk)
        dayoff_info = Dayoff.objects.get(employee=employee,period=default_period)
    except Employee.DoesNotExist:
        employee = 'admin'
        dayoff_info = ''

    default_period = Period.objects.get(period_year=2023) # Đang để 2023 để test, đúng là period_year=today.year
        
    # Lấy Leave application
    list_leave_application = Leave_application.objects.filter(employee=employee)
    # Lấy Overtime_application
    list_overtime_application = Overtime_application.objects.filter(employee=employee)
        
    return render(request, 'hr/dist/index.html' , {
        'user_info' : user_info,
        'role' : role,
        'employee' : employee,
        'dayoff_info' : dayoff_info,
        'list_leave_application' : list_leave_application,
        'list_overtime_application' : list_overtime_application,
    })

    
def signin(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' in request.session:
        return redirect('hr:index')

    # ĐĂNG NHẬP
    chuoi_kq_dang_nhap = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(user_password, 'tedisHR2023')

        # Đọc dữ liệu từ CSDL
        user = User.objects.filter(user_name=user_name, user_password=encoded)
        # user = User.objects.filter(user_name=user_name, user_password=user_password)
        # print(user.count())
        if user.count() > 0:
            # Tạo session
            list_user_values = []
            # usn = user.values()[0][user_name]
            list_key = ['user_name','permission_id','employee_id']
            for key in list_key:
                list_user_values.append(user.values()[0].get(key))
            request.session['s_user'] = list_user_values
            # print(user.values()[0]['user_name', 'user_full_name'])
            return redirect('hr:index')
        else:
            chuoi_kq_dang_nhap = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng nhập không thành công. Vui lòng kiểm tra lại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    return render(request, 'hr/dist/auth-login.html', {
        'chuoi_kq_dang_nhap' : chuoi_kq_dang_nhap,
        
    })


def logout(request):
    if 's_user' in request.session:
        del request.session['s_user']
    return redirect('hr:signin')


def signup_changepassword(request):
    # ĐĂNG KÝ
    frm_dang_ky = FormDangKy()
    chuoi_kq_dang_ky = ''
    if request.POST.get('btnDangKy'):
        frm_dang_ky = FormDangKy(request.POST, User)
        if frm_dang_ky.is_valid(): #and frm_dang_ky.cleaned_data['user_password'] == frm_dang_ky.cleaned_data['user_password']:
            # hasher = PBKDF2PasswordHasher() # salt: 1 byte
            ngayhienhanh = datetime.now()
            hasher = Argon2PasswordHasher() # salt: 8 bytes # dùng để mã hóa password
            request.POST.__mutable = True
            post = frm_dang_ky.save(commit=False)
            post.user_id = frm_dang_ky.cleaned_data['user_id']
            post.user_name = frm_dang_ky.cleaned_data['user_name']
            post.user_password = hasher.encode(frm_dang_ky.cleaned_data['user_password'], 'tedisHR2023')
            # post.user_password = frm_dang_ky.cleaned_data['user_password']
            post.user_full_name = frm_dang_ky.cleaned_data['user_full_name']
            post.user_title = frm_dang_ky.cleaned_data['user_title']
            post.user_mobile_1 = frm_dang_ky.cleaned_data['user_mobile_1']
            post.user_mobile_2 = frm_dang_ky.cleaned_data['user_mobile_2']
            post.user_email = frm_dang_ky.cleaned_data['user_email']
            post.created_by = frm_dang_ky.cleaned_data['created_by']
            post.create_at = ngayhienhanh
            post.save()
            chuoi_kq_dang_ky = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Registered successfully.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''
        
    # Đổi mật khẩu
    form = FormDoiMatKhau()
    if request.POST.get('btnChangePass'):
        form = FormDoiMatKhau(request.POST, User)
        if form.is_valid():
            mat_khau_hien_tai = form.cleaned_data['mat_khau_hien_tai']
            s_user = request.session.get('s_user')
            user = User.objects.get(id=s_user['id'])

            # hasher = Argon2PasswordHasher()
            # encoded = hasher.encode(mat_khau_hien_tai, '12345678')

            # if encoded == user.user_password:
            if form.cleaned_data['user_password'] == form.cleaned_data['xac_nhan_mat_khau']:
                    print('change pass')
    return render(request, 'hr/dist/auth-register.html', {
        'frm_dang_ky': frm_dang_ky,
        'chuoi_kq_dang_ky': chuoi_kq_dang_ky,
        'form': form,
    })

# User Guide
def guide(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    user_info = User.objects.all()
    s_user = request.session.get('s_user')
    role = s_user[1]
    employee_pk = s_user[2]
    
    return render(request, 'hr/dist/guide.html' , {
        
    })

def guide_leave_and_overtime(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    user_info = User.objects.all()
    s_user = request.session.get('s_user')
    role = s_user[1]
    employee_pk = s_user[2]
    
    return render(request, 'hr/dist/guide_leave_and_overtime.html' , {
        
    })

def guide_employee_information(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    user_info = User.objects.all()
    s_user = request.session.get('s_user')
    role = s_user[1]
    employee_pk = s_user[2]
    
    return render(request, 'hr/dist/guide_employee_information.html' , {
        
    })
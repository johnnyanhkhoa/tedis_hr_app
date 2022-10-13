from asyncio.windows_events import NULL
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from django.db.models import Q
from employee.models import *
from hr.models import User
from employee.form import *
from datetime import datetime

# Create your views here.
def employee_table(request): 
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Create employee
    form = CreateEmployeeForm()
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/employee/')
    

    ''' Filter '''
    # Đọc list fields cần filter trong model
    list_site = Site.objects.all()
    list_division = Division.objects.all()
    list_department_e = Department_E.objects.all()
    list_area = Area.objects.all()
    list_gp = Gp.objects.all()
    list_department_area = Department_area.objects.all()
    list_contract_type = Contract_type.objects.all()
    list_sexual = Sexual.objects.all()
    list_ethic_group = Ethic_group.objects.all()
    list_maritial_status = Marital_status.objects.all()
    list_certificate_e = Certificate_E.objects.all()
    
    # Render employees chưa filter
    employees = Employee.objects.order_by('id')
    
    # Lấy các thông tin cần filter từ template 
    site = request.GET.get('site')
    division = request.GET.get('division')
    department_e = request.GET.get('department_e') 
    area = request.GET.get('area') 
    gp = request.GET.get('gp') 
    department_area = request.GET.get('department_area') 
    contract_type = request.GET.get('contract_type')
    sexual = request.GET.get('sexual')
    ethic_group = request.GET.get('ethic_group')
    marital_status = request.GET.get('marital_status')
    certificate_e = request.GET.get('certificate_e')
    
    # Lấy các thông tin để filter 
    if site != '' and site is not None:
        q = ((Q(site=site)))
        employees = Employee.objects.filter(q)
    elif division != '' and division is not None:
        q = ((Q(division=division)))
        employees = Employee.objects.filter(q)
    elif department_e != '' and department_e is not None:
        q = ((Q(department_e=department_e)))
        employees = Employee.objects.filter(q)
    elif area != '' and area is not None:
        q = ((Q(area=area)))
        employees = Employee.objects.filter(q)
    elif gp != '' and gp is not None:
        q = ((Q(gp=gp)))
        employees = Employee.objects.filter(q)   
    elif department_area != '' and department_area is not None:
        q = ((Q(department_area=department_area)))
        employees = Employee.objects.filter(q)
    elif contract_type != '' and contract_type is not None:
        q = ((Q(contract_type=contract_type)))
        employees = Employee.objects.filter(q) 
    elif sexual != '' and sexual is not None:
        q = ((Q(sexual=sexual)))
        employees = Employee.objects.filter(q)
    elif ethic_group != '' and ethic_group is not None:
        q = ((Q(ethic_group=ethic_group)))
        employees = Employee.objects.filter(q)
    elif marital_status != '' and marital_status is not None:
        q = ((Q(marital_status=marital_status)))
        employees = Employee.objects.filter(q)
    elif certificate_e != '' and certificate_e is not None:
        q = ((Q(certificate_e=certificate_e)))
        employees = Employee.objects.filter(q)

    
    return render(request, 'employee/employee_datatable.html', {
        'form': form,
        'employees' : employees,
        'list_site' : list_site,
        'list_division' : list_division,
        'list_department_e' : list_department_e,
        'list_area' : list_area, 
        'list_gp' : list_gp, 
        'list_department_area' : list_department_area,
        'list_contract_type' : list_contract_type, 
        'list_sexual' : list_sexual,
        'list_ethic_group' : list_ethic_group, 
        'list_maritial_status' : list_maritial_status,
        'list_certificate_e' : list_certificate_e,
        
    })


def employee_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee
    employee = Employee.objects.get(pk=pk)
    
    # Get employee's children
    children = Employee_children.objects.filter(employee=employee)
    
    # Edit employee
    form = CreateEmployeeForm(instance=employee)
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/employee/')
    return render(request, 'employee/employee_edit_and_view.html', {
        'employee' : employee,
        'form' : form,
        'children' : children,
        # 'form_children_edit' : form_children_edit,
    })

def add_children(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    
    # Form
    if request.POST.get('btn_addchildren'):
        employee_name = request.POST.get('employee_id') # lấy từ <input type="hidden">
        employee_id = Employee.objects.only('id').get(id=employee_name)
        children = request.POST.get('children')  
        birthday_of_children = request.POST.get('birthday_of_children')
        children_info = Employee_children(employee=employee_id, children=children, birthday_of_children=birthday_of_children)
        children_info.save()
        return redirect('/employee/')
    return render(request, 'employee/form_add_children.html', {
        'employee' : employee,
        
    })
    
    
def probationary_period_form(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    id = str(pk)
    
    # Form Probationary_period
    form = Probationary_period_form()
    if request.method == 'POST':
        form = Probationary_period_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee:job_offer_form', pk=employee.pk)
    
    return render(request, 'employee/form_probationary_period.html', {
        'employee' : employee,
        'form' : form,
    })

def job_offer_form(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    # date = employee.from_date.strftime('%d')
    # num_month = employee.from_date.strftime('%m')
    # name_month = employee.from_date.strftime('%B')
    # print(date)
    # print(num_month)
    # print(name_month)
    
    
    return render(request, 'employee/form_job_offer.html', {
        'employee' : employee,
    })
    
    
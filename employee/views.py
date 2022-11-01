from asyncio.windows_events import NULL
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from django.db.models import Q
from employee.models import *
from hr.models import User
from employee.form import *
from datetime import datetime

import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
import os

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
            # Get Year of birth 
            phrase_3 = request.POST.get('date_of_birth')
            phrase_to_list_3 = phrase_3.split("-")
            year_of_birth = int(phrase_to_list_3[0])
            
            # Calculate Age
            now = datetime.now()
            present_year = int(now.strftime("%Y"))
            age = present_year - year_of_birth
            
            # Calculate Years of Service
            phrase_1 = request.POST.get('joining_date')
            phrase_to_list_1 = phrase_1.split("-")
            joining_year = int(phrase_to_list_1[0])
            
            if request.POST.get('out_date') != '':
                phrase_2 = request.POST.get('out_date')
                phrase_to_list_2 = phrase_2.split("-")
                out_year = int(phrase_to_list_2[0])
                years_of_service = out_year - joining_year
            else:
                years_of_service = present_year - joining_year
                
            
            # Save age and another info to DB
            request.POST.__mutable = True
            post = form.save(commit=False)
            post.age = age
            post.years_of_service = years_of_service
            post.year_of_birth = year_of_birth
            post.save()
            return redirect('/employee/')
    

    ''' Filter '''
    # Đọc list fields cần filter trong model
    list_site = Site.objects.all()
    list_division = Division.objects.all()
    list_department_e = Department_E.objects.all()
    list_area = Area.objects.all()
    list_gp = Gp.objects.all()
    list_contract_type = Contract_type.objects.all()
    list_university = University.objects.all()
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
    university = request.GET.get('university')
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
    elif university != '' and university is not None:
        q = ((Q(university=university)))
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
        'list_contract_type' : list_contract_type, 
        'list_sexual' : list_sexual,
        'list_ethic_group' : list_ethic_group, 
        'list_maritial_status' : list_maritial_status,
        'list_certificate_e' : list_certificate_e,
        'list_university' : list_university,
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
    
    
def employee_delete(request, pk):
    employee_children_relatives = Employee_children.objects.filter(employee=pk)
    # employee_probationary_period = Probationary_period.objects.filter(employee=pk)
    employee_contract = Employee_contract.objects.filter(employee=pk)
    employee_promotion = Employee_promotion.objects.filter(employee=pk)

    try:
        employee_info = Employee.objects.get(id = pk)
        if employee_children_relatives.exists() or employee_contract.exists() or employee_promotion.exists():
            messages.error(request, 'Employee can not be deleted. Check relevant papers.')
        else:
            employee_info.delete()
            messages.success(request, 'Employee deleted')
    except Employee.DoesNotExist:
        return redirect('/employee/')
    return redirect('/employee/')
        
    

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

def add_contract(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee & list of contract type:
    employee = Employee.objects.get(pk=pk)
    list_contract_type = Contract_type.objects.all()
    
    # Create contract
    if request.POST.get('btn_addcontract'):
        employee_id = Employee.objects.only('id').get(id=pk)
        contract_no = request.POST.get('contract_no')
        type_id = request.POST.get('type_id')  
        contract_type = Contract_type.objects.only('id').get(id=type_id)
        signed_contract_date = request.POST.get('signed_contract_date')
        contract_info = Employee_contract(employee=employee_id, contract_no=contract_no, contract_type=contract_type,signed_contract_date=signed_contract_date)                 
        contract_info.save()
        return redirect('/employee/')
        
    return render(request, 'employee/form_add_contract.html', {
        'employee' : employee,
        'list_contract_type' : list_contract_type,

    })
    

def add_promotion(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    
    # Create employee
    if request.POST.get('btn_addpromotion'):
        employee_id = Employee.objects.only('id').get(id=pk)
        promotion_effective_date = request.POST.get('promotion_effective_date')
        promotion_decision_number = request.POST.get('promotion_decision_number')
        promotion_info = Employee_promotion(employee=employee_id, promotion_effective_date=promotion_effective_date, promotion_decision_number=promotion_decision_number)                 
        promotion_info.save()
        return redirect('/employee/')
        
    return render(request, 'employee/form_add_promotion.html', {
        'employee' : employee,

    })
    
    
def TD_probationary_period_form(request, pk):
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
            return redirect('employee:TD_job_offer_FORM', pk=employee.pk)
    
    return render(request, 'employee/form_probationary_period.html', {
        'employee' : employee,
        'form' : form,
    })
    

def JV_probationary_period_form(request, pk):
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
            return redirect('employee:JV_job_offer_FORM', pk=employee.pk)
    
    return render(request, 'employee/form_probationary_period.html', {
        'employee' : employee,
        'form' : form,
    })


def TD_job_offer_FORM(request, pk):
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
    
    
    return render(request, 'employee/TD_letter_job_offer.html', {
        'employee' : employee,
    })
    

def JV_job_offer_FORM(request, pk):
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
    
    
    return render(request, 'employee/JV_letter_job_offer.html', {
        'employee' : employee,
    })
    
    
def JV_HDLD(request, pk):
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
    
    
    return render(request, 'employee/JV_HDLD.html', {
        'employee' : employee,
    })
    
    
def TD_job_offer_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)

    html_string = render_to_string('employee/TD_letter_job_offer.html', {
        'today': today,
        'employee': employee,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'report_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)


    return HttpResponse(html_string)


def JV_job_offer_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)

    html_string = render_to_string('employee/JV_letter_job_offer.html', {
        'today': today,
        'employee': employee,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'report_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)


    return HttpResponse(html_string)

# def html_to_pdf_view(request, pk):
#     employee = Employee.objects.get(pk=pk)
#     return render(request, 'employee/TD_letter_job_offer.html', {
#         'employee' : employee,
#     })
    
    

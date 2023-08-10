from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from django.db.models import Q, Case, When, Value
from employee.models import *
from hr.models import User
from employee.form import *
from datetime import datetime, date, timedelta
from django.shortcuts import get_object_or_404

import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
import os
# calendar
import calendar
from calendar import HTMLCalendar, monthrange
# Json
from django.http import JsonResponse
import json
from django.core.serializers import serialize
# XLWT
import xlwt
from io import StringIO, BytesIO
from PIL import Image
# Random
import random
# Math
import math


# Create Custom Function
def date_range(start, end):
    delta = end - start
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days



# Create your views here.
def employee_table(request): 
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 1 or s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    
    ''' Filter '''
    # Đọc list fields cần filter trong model
    # list_site = Site.objects.all()
    # list_division = Division.objects.all()
    # list_department_e = Department_E.objects.all()
    # list_area = Area.objects.all()
    # list_gp = Gp.objects.all()
    # list_contract_type = Contract_type.objects.all()
    # list_university = University.objects.all()
    # list_sexual = Sexual.objects.all()
    # list_ethic_group = Ethic_group.objects.all()
    # list_maritial_status = Marital_status.objects.all()
    # list_certificate_e = Certificate_E.objects.all()
    
    # Render employees chưa filter
    if s_user[1] == 1:
        employees = Employee_manager.objects.filter(manager=s_user[2])
    else:
        employees = Employee.objects.order_by('site')
    
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
    # if site != '' and site is not None:
    #     q = ((Q(site=site)))
    #     employees = Employee.objects.filter(q)
    # elif division != '' and division is not None:
    #     q = ((Q(division=division)))
    #     employees = Employee.objects.filter(q)
    # elif department_e != '' and department_e is not None:
    #     q = ((Q(department_e=department_e)))
    #     employees = Employee.objects.filter(q)
    # elif area != '' and area is not None:
    #     q = ((Q(area=area)))
    #     employees = Employee.objects.filter(q)
    # elif gp != '' and gp is not None:
    #     q = ((Q(gp=gp)))
    #     employees = Employee.objects.filter(q)   
    # elif department_area != '' and department_area is not None:
    #     q = ((Q(department_area=department_area)))
    #     employees = Employee.objects.filter(q)
    # elif contract_type != '' and contract_type is not None:
    #     q = ((Q(contract_type=contract_type)))
    #     employees = Employee.objects.filter(q) 
    # elif university != '' and university is not None:
    #     q = ((Q(university=university)))
    #     employees = Employee.objects.filter(q) 
    # elif sexual != '' and sexual is not None:
    #     q = ((Q(sexual=sexual)))
    #     employees = Employee.objects.filter(q)
    # elif ethic_group != '' and ethic_group is not None:
    #     q = ((Q(ethic_group=ethic_group)))
    #     employees = Employee.objects.filter(q)
    # elif marital_status != '' and marital_status is not None:
    #     q = ((Q(marital_status=marital_status)))
    #     employees = Employee.objects.filter(q)
    # elif certificate_e != '' and certificate_e is not None:
    #     q = ((Q(certificate_e=certificate_e)))
    #     employees = Employee.objects.filter(q)

    
    return render(request, 'employee/employee_datatable.html', {
        'employees' : employees,
        'role' : role,
        # 'list_site' : list_site,
        # 'list_division' : list_division,
        # 'list_department_e' : list_department_e,
        # 'list_area' : list_area, 
        # 'list_gp' : list_gp, 
        # 'list_contract_type' : list_contract_type, 
        # 'list_sexual' : list_sexual,
        # 'list_ethic_group' : list_ethic_group, 
        # 'list_maritial_status' : list_maritial_status,
        # 'list_certificate_e' : list_certificate_e,
        # 'list_university' : list_university,
    })
    
    
def create_new_employee(request): 
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    s_user = request.session.get('s_user')
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
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
            post.joining_year = joining_year
            post.active = 1
            post.created_at = datetime.now()
            full_name = request.POST.get('full_name')
            post.save()
            employee = Employee.objects.get(full_name=full_name) 
            return redirect('employee:add_staff_for_manager', pk=employee.id)
        else:
            print(form.errors.as_data())
    
    return render(request, 'employee/employee_create_new.html', {
        'form': form,

    })


def employee_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee
    employee = Employee.objects.get(pk=pk)
    
    # Get promotion
    promotion_list = list(Employee_promotion.objects.filter(employee=pk).order_by('-created_at'))
    if promotion_list == []:
        latest_promotion = ''
    else:
        latest_promotion = promotion_list[0]
    
    # Get contract
    contract_list = list(Employee_contract.objects.filter(employee=pk).order_by('-created_at'))
    if contract_list == []:
        latest_contract = ''
    else:
        latest_contract = contract_list[0]
        
    
    
    # Get employee's children
    children_list = Employee_children.objects.filter(employee=employee)
    
    # Edit employeeinstance
    form = CreateEmployeeForm(instance=employee)
    if request.method == 'POST':
        form = CreateEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/employee/')
    return render(request, 'employee/employee_edit_and_view.html', {
        'employee' : employee,
        'form' : form,
        'children_list' : children_list,
        'latest_promotion' : latest_promotion,
        'latest_contract' : latest_contract
    })
    
    
def employee_resign(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee
    employee = Employee.objects.get(pk=pk)
    
    # Edit employee instance
    form = CreateEmployeeForm(instance=employee)
    if request.POST.get('btnResignEmployee'):
        post = form.save(commit=False)
        post.out_date = request.POST.get('out_date')
        post.active = 0
        post.save()
        messages.success(request, 'Staff resigned')
        return redirect('/employee/')
        
    return render(request, 'employee/form_resign_employee.html', {
        'employee' : employee,
        'form' : form,
    })
    



def add_staff_for_manager(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get user
    s_user = request.session.get('s_user')
    role = s_user[1]
    
    # Get employee
    employee = Employee.objects.get(id = pk)
    
    # Add manager
    form = AddManager()
    if request.method == 'POST':
        form = AddManager(request.POST)
        if form.is_valid():
            # Save age and another info to DB
            request.POST.__mutable = True
            post = form.save(commit=False)
            post.employee = employee
            post.save()
            messages.success(request, 'Staff added')
            return redirect('/employee/')
        else:
            print(form.errors.as_data())
    
    
    return render(request, 'employee/form_add_staff.html', {
        'employee' : employee,
        'form' : form,
        
    })
    

def edit_manager(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get user
    s_user = request.session.get('s_user')
    role = s_user[1]
    
    # Get employee
    employee = Employee.objects.get(id = pk)
    
    # Get manager
    try: 
        manager_info = Employee_manager.objects.get(employee = pk)
    
        # Edit manager
        form = AddManager(instance=manager_info)
        if request.method == 'POST':
            form = AddManager(request.POST, instance=manager_info)
            if form.is_valid():
                post = form.save(commit=False)
                post.employee = employee
                post.save()
                messages.success(request, 'Manager updated')
                return redirect('/employee/')
            
    except Employee_manager.DoesNotExist:
        # Add manager
        form = AddManager()
        if request.method == 'POST':
            form = AddManager(request.POST)
            if form.is_valid():
                # Save age and another info to DB
                request.POST.__mutable = True
                post = form.save(commit=False)
                post.employee = employee
                post.save()
                messages.success(request, 'Staff added')
                return redirect('/employee/')
            else:
                print(form.errors.as_data())
    
    
    return render(request, 'employee/edit_manager.html', {
        'employee' : employee,
        'form' : form,
        
    })
    

def staff_delete(request, pk):
    try:
        staff_info = Employee_manager.objects.get(employee = pk)
        staff_info.delete()
        messages.success(request, 'Staff deleted')
    except Employee.DoesNotExist:
        return redirect('/add_staff_for_manager/')
    return redirect('/add_staff_for_manager/')
        

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
        messages.success(request, 'SUCCESS: Dependent registered')
        return redirect('/employee/')
    return render(request, 'employee/form_add_children.html', {
        'employee' : employee,
        
    })


def view_relatives(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    
    # Get relatives
    list_of_relatives = Employee_children.objects.filter(employee=employee)
    number_of_relatives = list_of_relatives.count()
    
    
    return render(request, 'employee/view_relatives.html', {
        'employee' : employee,
        'list_of_relatives' : list_of_relatives,
        'number_of_relatives' : number_of_relatives,
        
    })
    

def edit_relatives(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get relatives:
    relative = Employee_children.objects.get(pk=pk)
    relative_date_of_birth = relative.birthday_of_children.strftime("%Y-%m-%d")
    
    # Form
    if request.POST.get('btnUpdaterelative'):
        employee = relative.employee
        children = request.POST.get('children') 
        birthday_of_children = request.POST.get('birthday_of_children')  
        relative_info = Employee_children(id=relative.id,employee=employee,
                                          children=children, birthday_of_children=birthday_of_children)
        relative_info.save()
        messages.success(request, 'SUCCESS: Relative updated')
        return redirect('employee:edit_relatives',pk=relative.id)
    return render(request, 'employee/edit_relatives.html', {
        'relative' : relative,
        'relative_date_of_birth' : relative_date_of_birth,
        
    })


def relative_delete(request, pk):
    try:
        relative_info = Employee_children.objects.get(pk = pk)
        employee = relative_info.employee
        relative_info.delete()
        messages.success(request, 'Relative deleted')
    except Employee_children.DoesNotExist:
        return redirect('employee:view_relatives',pk=employee.id)
    return redirect('employee:view_relatives',pk=employee.id)


def add_contract(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee & list of contract type:
    employee = Employee.objects.get(pk=pk)
    employee_site = employee.site
    list_contract_category = Contract_category.objects.all()
    list_contract_type = Contract_type.objects.all()
    
    # Create contract
    if request.POST.get('btn_addcontract'):
        employee_id = Employee.objects.only('id').get(id=pk)
        contract_no = request.POST.get('contract_no')
        category_id = request.POST.get('category_id')  
        contract_category = Contract_category.objects.only('id').get(id=category_id)
        type_id = request.POST.get('type_id')  
        contract_type = Contract_type.objects.only('id').get(id=type_id)
        signed_contract_date = request.POST.get('signed_contract_date')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        basic_salary = request.POST.get('basic_salary')
        if request.POST.get('responsibility_allowance') == '':
            responsibility_allowance = 0
        else:
            responsibility_allowance = request.POST.get('responsibility_allowance')
        if request.POST.get('lunch_support') == '':
            lunch_support = 0
        else:
            lunch_support = request.POST.get('lunch_support')
        if request.POST.get('transportation_support') == '':
            transportation_support = 0
        else:
            transportation_support = request.POST.get('transportation_support')
        if request.POST.get('telephone_support') == '':
            telephone_support = 0
        else:
            telephone_support = request.POST.get('telephone_support')
        if request.POST.get('travel_support') == '':
            travel_support = 0
        else:
            travel_support = request.POST.get('travel_support')
        if request.POST.get('seniority_bonus') == '':
            seniority_bonus = 0
        else:
            seniority_bonus = request.POST.get('seniority_bonus')
        contract_info = Employee_contract(employee=employee_id, contract_no=contract_no, contract_category=contract_category,contract_type=contract_type,signed_contract_date=signed_contract_date,from_date=from_date,to_date=to_date,basic_salary=basic_salary,responsibility_allowance=responsibility_allowance,lunch_support=lunch_support,transportation_support=transportation_support,telephone_support=telephone_support,seniority_bonus=seniority_bonus,travel_support=travel_support)                 
        if str(employee_site) == 'RO':
            contract_info.save()
            return redirect('employee:RO_HDLD_PDF', pk=employee.pk)
        elif str(employee_site) == "JV":
            contract_info.save()
            return redirect('employee:JV_HDLD_PDF', pk=employee.pk)
        elif str(employee_site) == "VH":
            contract_info.save()
            return redirect('employee:VH_HDLD_PDF', pk=employee.pk)
        else:
            messages.error(request, 'MISSING DATA: Employee Site')
        
    return render(request, 'employee/form_add_contract.html', {
        'employee' : employee,
        'list_contract_category' : list_contract_category,
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
    
    
def probationary_period_form(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    employee_site = employee.site
    
    # Form Probationary_period
    if request.POST.get('btn_addperiod'):
        employee_id = Employee.objects.only('id').get(id=pk)
        letter_date = request.POST.get('letter_date')
        letter_returning_date = request.POST.get('letter_returning_date')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        monthly_gross_salary = request.POST.get('monthly_gross_salary')
        monthly_allowance = request.POST.get('monthly_allowance')
        period_info = Probationary_period(employee=employee_id, letter_date=letter_date, from_date=from_date, to_date=to_date, monthly_gross_salary=monthly_gross_salary, monthly_allowance=monthly_allowance,letter_returning_date=letter_returning_date)                 
        if str(employee_site) == 'RO':
            period_info.save()
            return redirect('employee:TD_job_offer_PDF', pk=employee.pk)
        elif str(employee_site) == "JV":
            period_info.save()
            return redirect('employee:JV_job_offer_PDF', pk=employee.pk)
        elif str(employee_site) == "VH":
            period_info.save()
            return redirect('employee:VH_job_offer_PDF', pk=employee.pk)
        else:
            messages.error(request, 'MISSING DATA: Employee Site')
    
    return render(request, 'employee/form_probationary_period.html', {
        'employee' : employee,
    })
    
    
def TD_job_offer_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)
    # Get Probationary_period
    probationary_period_list = list(Probationary_period.objects.filter(employee=pk).order_by('-id'))    
    latest_probationary_period = probationary_period_list[0]
    
    # Get letter_date day-month-year
    letter_date_day = latest_probationary_period.letter_date.strftime("%d")
    letter_date_month = latest_probationary_period.letter_date.strftime("%m")
    letter_date_period_year = latest_probationary_period.letter_date.strftime("%Y")
    
    # Get letter_returning_date day-month-year
    letter_returning_date_day = latest_probationary_period.letter_returning_date.strftime("%d")
    letter_returning_date_month = latest_probationary_period.letter_returning_date.strftime("%m")
    letter_returning_date_year = latest_probationary_period.letter_returning_date.strftime("%Y")
    
    # Get from_date day-month-year
    from_date_day = latest_probationary_period.from_date.strftime("%d")
    from_date_month = latest_probationary_period.from_date.strftime("%m")
    from_date_month_name = latest_probationary_period.from_date.strftime("%B")
    from_date_year = latest_probationary_period.from_date.strftime("%Y")
    
    # Get to_date day-month-year
    to_date_day = latest_probationary_period.to_date.strftime("%d")
    to_date_month = latest_probationary_period.to_date.strftime("%m")
    to_date_month_name = latest_probationary_period.to_date.strftime("%B")
    to_date_year = latest_probationary_period.to_date.strftime("%Y")

    html_string = render_to_string('employee/TD_letter_job_offer.html', {
        'today': today,
        'employee': employee,
        'latest_probationary_period' : latest_probationary_period,
        #letter_date day-month-year
        'letter_date_day' : letter_date_day,
        'letter_date_month' : letter_date_month,
        'letter_date_period_year' : letter_date_period_year,
        # from_date day-month-year
        'from_date_day' : from_date_day,
        'from_date_month' : from_date_month, 
        'from_date_month_name' : from_date_month_name,
        'from_date_year' : from_date_year,
        # to_date day-month-year
        'to_date_day' : to_date_day,
        'to_date_month' : to_date_month,
        'to_date_month_name' : to_date_month_name,
        'to_date_year' : to_date_year,
        # letter_retuning_date day-month-year
        'letter_returning_date_day' : letter_returning_date_day, 
        'letter_returning_date_month' : letter_returning_date_month, 
        'letter_returning_date_year' : letter_returning_date_year,
        
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'TD_job_offer_' + datetime.now().strftime('%Y%m%d___%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def JV_job_offer_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)
    # Get Probationary_period
    probationary_period_list = list(Probationary_period.objects.filter(employee=pk).order_by('-id'))    
    latest_probationary_period = probationary_period_list[0]
    
    # Get letter_date day-month-year
    letter_date_day = latest_probationary_period.letter_date.strftime("%d")
    letter_date_month = latest_probationary_period.letter_date.strftime("%m")
    letter_date_period_year = latest_probationary_period.letter_date.strftime("%Y")
    
    # Get letter_returning_date day-month-year
    letter_returning_date_day = latest_probationary_period.letter_returning_date.strftime("%d")
    letter_returning_date_month = latest_probationary_period.letter_returning_date.strftime("%m")
    letter_returning_date_year = latest_probationary_period.letter_returning_date.strftime("%Y")
    
    # Get from_date day-month-year
    from_date_day = latest_probationary_period.from_date.strftime("%d")
    from_date_month = latest_probationary_period.from_date.strftime("%m")
    from_date_year = latest_probationary_period.from_date.strftime("%Y")
    
    # Get to_date day-month-year
    to_date_day = latest_probationary_period.to_date.strftime("%d")
    to_date_month = latest_probationary_period.to_date.strftime("%m")
    to_date_year = latest_probationary_period.to_date.strftime("%Y")

    html_string = render_to_string('employee/JV_letter_job_offer.html', {
        'today': today,
        'employee': employee,
        'latest_probationary_period' : latest_probationary_period,
        #letter_date day-month-year
        'letter_date_day' : letter_date_day,
        'letter_date_month' : letter_date_month,
        'letter_date_period_year' : letter_date_period_year,
        # from_date day-month-year
        'from_date_day' : from_date_day,
        'from_date_month' : from_date_month, 
        'from_date_year' : from_date_year,
        # to_date day-month-year
        'to_date_day' : to_date_day,
        'to_date_month' : to_date_month,
        'to_date_year' : to_date_year,
        # letter_retuning_date day-month-year
        'letter_returning_date_day' : letter_returning_date_day, 
        'letter_returning_date_month' : letter_returning_date_month, 
        'letter_returning_date_year' : letter_returning_date_year,
        
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'JV_job_offer_' + datetime.now().strftime('%Y%m%d___%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def VH_job_offer_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)
    # Get Probationary_period
    probationary_period_list = list(Probationary_period.objects.filter(employee=pk).order_by('-id'))    
    latest_probationary_period = probationary_period_list[0]
    
    # Get letter_date day-month-year
    letter_date_day = latest_probationary_period.letter_date.strftime("%d")
    letter_date_month = latest_probationary_period.letter_date.strftime("%m")
    letter_date_period_year = latest_probationary_period.letter_date.strftime("%Y")
    
    # Get letter_returning_date day-month-year
    letter_returning_date_day = latest_probationary_period.letter_returning_date.strftime("%d")
    letter_returning_date_month = latest_probationary_period.letter_returning_date.strftime("%m")
    letter_returning_date_year = latest_probationary_period.letter_returning_date.strftime("%Y")
    
    # Get from_date day-month-year
    from_date_day = latest_probationary_period.from_date.strftime("%d")
    from_date_month = latest_probationary_period.from_date.strftime("%m")
    from_date_year = latest_probationary_period.from_date.strftime("%Y")
    
    # Get to_date day-month-year
    to_date_day = latest_probationary_period.to_date.strftime("%d")
    to_date_month = latest_probationary_period.to_date.strftime("%m")
    to_date_year = latest_probationary_period.to_date.strftime("%Y")

    html_string = render_to_string('employee/VH_letter_job_offer.html', {
        'today': today,
        'employee': employee,
        'latest_probationary_period' : latest_probationary_period,
        #letter_date day-month-year
        'letter_date_day' : letter_date_day,
        'letter_date_month' : letter_date_month,
        'letter_date_period_year' : letter_date_period_year,
        # from_date day-month-year
        'from_date_day' : from_date_day,
        'from_date_month' : from_date_month, 
        'from_date_year' : from_date_year,
        # to_date day-month-year
        'to_date_day' : to_date_day,
        'to_date_month' : to_date_month,
        'to_date_year' : to_date_year,
        # letter_retuning_date day-month-year
        'letter_returning_date_day' : letter_returning_date_day, 
        'letter_returning_date_month' : letter_returning_date_month, 
        'letter_returning_date_year' : letter_returning_date_year,
        
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'VH_job_offer_' + datetime.now().strftime('%Y%m%d___%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def JV_HDLD_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)
    # Get Contract
    contract_list = list(Employee_contract.objects.filter(employee=pk).order_by('-id'))    
    latest_contract = contract_list[0]
    # Get signed_contract_date day-month-year
    signed_contract_date_day = latest_contract.signed_contract_date.strftime("%d")
    signed_contract_date_month = latest_contract.signed_contract_date.strftime("%m")
    signed_contract_date_month_name = latest_contract.signed_contract_date.strftime("%B")
    signed_contract_date_year = latest_contract.signed_contract_date.strftime("%Y")
    # Get from_date day-month-year
    from_date_day = latest_contract.from_date.strftime("%d")
    from_date_month = latest_contract.from_date.strftime("%m")
    from_date_month_name = latest_contract.from_date.strftime("%B")
    from_date_year = latest_contract.from_date.strftime("%Y")
    # Get to_date day-month-year
    to_date_day = latest_contract.to_date.strftime("%d")
    to_date_month = latest_contract.to_date.strftime("%m")
    to_date_month_name = latest_contract.to_date.strftime("%B")
    to_date_year = latest_contract.to_date.strftime("%Y")
    

    html_string = render_to_string('employee/JV_HDLD.html', {
        'today': today,
        'employee': employee,
        'latest_contract' : latest_contract,
        # signed_contract_date
        'signed_contract_date_day' : signed_contract_date_day,
        'signed_contract_date_month' : signed_contract_date_month,
        'signed_contract_date_month_name' : signed_contract_date_month_name,
        'signed_contract_date_year' : signed_contract_date_year,
        # from_date
        'from_date_day' : from_date_day,
        'from_date_month' : from_date_month,
        'from_date_month_name' : from_date_month_name,
        'from_date_year' : from_date_year,
        # to_date
        'to_date_day' : to_date_day,
        'to_date_month' : to_date_month,
        'to_date_month_name' : to_date_month_name,
        'to_date_year' : to_date_year,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'JV_HDLD_' + datetime.now().strftime('%Y%m%d___%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def RO_HDLD_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)
    # Get Contract
    contract_list = list(Employee_contract.objects.filter(employee=pk).order_by('-id'))    
    latest_contract = contract_list[0]
    # Get signed_contract_date day-month-year
    signed_contract_date_day = latest_contract.signed_contract_date.strftime("%d")
    signed_contract_date_month = latest_contract.signed_contract_date.strftime("%m")
    signed_contract_date_month_name = latest_contract.signed_contract_date.strftime("%B")
    signed_contract_date_year = latest_contract.signed_contract_date.strftime("%Y")
    # Get from_date day-month-year
    from_date_day = latest_contract.from_date.strftime("%d")
    from_date_month = latest_contract.from_date.strftime("%m")
    from_date_month_name = latest_contract.from_date.strftime("%B")
    from_date_year = latest_contract.from_date.strftime("%Y")
    # Get to_date day-month-year
    to_date_day = latest_contract.to_date.strftime("%d")
    to_date_month = latest_contract.to_date.strftime("%m")
    to_date_month_name = latest_contract.to_date.strftime("%B")
    to_date_year = latest_contract.to_date.strftime("%Y")
    

    html_string = render_to_string('employee/RO_HDLD.html', {
        'today': today,
        'employee': employee,
        'latest_contract' : latest_contract,
        # signed_contract_date
        'signed_contract_date_day' : signed_contract_date_day,
        'signed_contract_date_month' : signed_contract_date_month,
        'signed_contract_date_month_name' : signed_contract_date_month_name,
        'signed_contract_date_year' : signed_contract_date_year,
        # from_date
        'from_date_day' : from_date_day,
        'from_date_month' : from_date_month,
        'from_date_month_name' : from_date_month_name,
        'from_date_year' : from_date_year,
        # to_date
        'to_date_day' : to_date_day,
        'to_date_month' : to_date_month,
        'to_date_month_name' : to_date_month_name,
        'to_date_year' : to_date_year,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'RO_HDLD_' + datetime.now().strftime('%Y%m%d___%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def VH_HDLD_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)
    # Get Contract
    contract_list = list(Employee_contract.objects.filter(employee=pk).order_by('-id'))    
    latest_contract = contract_list[0]
    # Get signed_contract_date day-month-year
    signed_contract_date_day = latest_contract.signed_contract_date.strftime("%d")
    signed_contract_date_month = latest_contract.signed_contract_date.strftime("%m")
    signed_contract_date_month_name = latest_contract.signed_contract_date.strftime("%B")
    signed_contract_date_year = latest_contract.signed_contract_date.strftime("%Y")
    # Get from_date day-month-year
    from_date_day = latest_contract.from_date.strftime("%d")
    from_date_month = latest_contract.from_date.strftime("%m")
    from_date_month_name = latest_contract.from_date.strftime("%B")
    from_date_year = latest_contract.from_date.strftime("%Y")
    # Get to_date day-month-year
    to_date_day = latest_contract.to_date.strftime("%d")
    to_date_month = latest_contract.to_date.strftime("%m")
    to_date_month_name = latest_contract.to_date.strftime("%B")
    to_date_year = latest_contract.to_date.strftime("%Y")

    # Get Probationary_period
    probationary_period_list = list(Probationary_period.objects.filter(employee=pk).order_by('-id'))    
    latest_probationary_period = probationary_period_list[0]
    # Get from_date day-month-year
    probation_from_date_day = latest_probationary_period.from_date.strftime("%d")
    probation_from_date_month = latest_probationary_period.from_date.strftime("%m")
    probation_from_date_month_name = latest_probationary_period.from_date.strftime("%B")
    probation_from_date_year = latest_probationary_period.from_date.strftime("%Y")
    # Get to_date day-month-year
    probation_to_date_day = latest_probationary_period.to_date.strftime("%d")
    probation_to_date_month = latest_probationary_period.to_date.strftime("%m")
    probation_to_date_month_name = latest_probationary_period.to_date.strftime("%B")
    probation_to_date_year = latest_probationary_period.to_date.strftime("%Y")
    

    html_string = render_to_string('employee/VH_HDLD.html', {
        'today': today,
        'employee': employee,
        'latest_contract' : latest_contract,
        # signed_contract_date
        'signed_contract_date_day' : signed_contract_date_day,
        'signed_contract_date_month' : signed_contract_date_month,
        'signed_contract_date_month_name' : signed_contract_date_month_name,
        'signed_contract_date_year' : signed_contract_date_year,
        # from_date
        'from_date_day' : from_date_day,
        'from_date_month' : from_date_month,
        'from_date_month_name' : from_date_month_name,
        'from_date_year' : from_date_year,
        # to_date
        'to_date_day' : to_date_day,
        'to_date_month' : to_date_month,
        'to_date_month_name' : to_date_month_name,
        'to_date_year' : to_date_year,
        
        # probation from
        'probation_from_date_day' : probation_from_date_day,
        'probation_from_date_month' : probation_from_date_month,
        'probation_from_date_month_name' : probation_from_date_month_name,
        'probation_from_date_year' : probation_from_date_year,
        # probation to
        'probation_to_date_day' : probation_to_date_day,
        'probation_to_date_month' : probation_to_date_month,
        'probation_to_date_month_name' : probation_to_date_month_name,
        'probation_to_date_year' : probation_to_date_year,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'VH_HDLD_' + datetime.now().strftime('%Y%m%d___%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def leave_application(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get manager:
    employee_id_in_Employee_model = int(employee_pk)
    manager_id_in_Manager_model = Employee_manager.objects.only('id').get(employee=employee_id_in_Employee_model)
    manager_int_id_in_Manager_model = int(manager_id_in_Manager_model.manager.id)
    manager = Employee.objects.get(pk=manager_int_id_in_Manager_model)
    
    # Get today date
    application_date = date.today()
    
    # Get Employee, Leave_type, Hour and Minute list
    list_employee = Employee.objects.all()
    
    
    # Data input
    if request.POST.get('btn_addleave'):
        employee_id = Employee.objects.only('id').get(id=employee_pk)
        emergency_contact = request.POST.get('emergency_contact')
        contact_person = request.POST.get('contact_person')
        relation = request.POST.get('relation')
        # Annual
        annual_from = request.POST.get('annual_from')
        annual_to = request.POST.get('annual_to')
        annual_number_of_leave_days = request.POST.get('annual_number_of_leave_days')
        annual_remark = request.POST.get('annual_remark')
        # Non-paid
        non_paid_from = request.POST.get('non_paid_from')
        non_paid_to = request.POST.get('non_paid_to')
        non_paid_number_of_leave_days = request.POST.get('non_paid_number_of_leave_days')
        non_paid_remark = request.POST.get('non_paid_remark')
        # Wedding
        wedding_from = request.POST.get('wedding_from')
        wedding_to = request.POST.get('wedding_to')
        wedding_number_of_leave_days = request.POST.get('wedding_number_of_leave_days')
        wedding_remark = request.POST.get('wedding_remark')
        # Bereavement
        bereavement_from = request.POST.get('bereavement_from')
        bereavement_to = request.POST.get('bereavement_to')
        bereavement_number_of_leave_days = request.POST.get('bereavement_number_of_leave_days')
        bereavement_remark = request.POST.get('bereavement_remark')
        # Maternity / Obstetric
        maternity_obstetric_from = request.POST.get('maternity_obstetric_from')
        maternity_obstetric_to = request.POST.get('maternity_obstetric_to')
        maternity_obstetric_number_of_leave_days = request.POST.get('maternity_obstetric_number_of_leave_days')
        maternity_obstetric_remark = request.POST.get('maternity_obstetric_remark')
        # Sick
        sick_from = request.POST.get('sick_from')
        sick_to = request.POST.get('sick_to')
        sick_number_of_leave_days = request.POST.get('sick_number_of_leave_days')
        sick_remark = request.POST.get('sick_remark')
        # Off in-lieu
        offinlieu_from = request.POST.get('offinlieu_from')
        offinlieu_to = request.POST.get('offinlieu_to')
        offinlieu_number_of_leave_days = request.POST.get('offinlieu_number_of_leave_days')
        offinlieu_remark = request.POST.get('offinlieu_remark')
        # Other in-lieu
        other_from = request.POST.get('other_from')
        other_to = request.POST.get('other_to')
        other_number_of_leave_days = request.POST.get('other_number_of_leave_days')
        other_remark = request.POST.get('other_remark')
        # Total days of leave
        if annual_number_of_leave_days == '':
            annual_number_of_leave_days = 0
        if non_paid_number_of_leave_days == '':
            non_paid_number_of_leave_days = 0
        if wedding_number_of_leave_days == '':
            wedding_number_of_leave_days = 0
        if bereavement_number_of_leave_days == '':
            bereavement_number_of_leave_days = 0
        if maternity_obstetric_number_of_leave_days == '':
            maternity_obstetric_number_of_leave_days = 0
        if sick_number_of_leave_days == '':
            sick_number_of_leave_days = 0
        if offinlieu_number_of_leave_days == '':
            offinlieu_number_of_leave_days = 0
        if other_number_of_leave_days == '':
            other_number_of_leave_days = 0
        total_days = float(annual_number_of_leave_days) + float(non_paid_number_of_leave_days) + float(wedding_number_of_leave_days) + float(bereavement_number_of_leave_days) + float(maternity_obstetric_number_of_leave_days) + float(sick_number_of_leave_days) + float(offinlieu_number_of_leave_days) + float(other_number_of_leave_days)
        temporary_replacement = request.POST.get('temporary_replacement_id')  
        application_date = date.today()
        status = Status.objects.get(id=1)
        hr_status = Status.objects.get(id=1)
        leave_application_info = Leave_application(employee=employee_id,emergency_contact=emergency_contact,contact_person=contact_person,relation=relation,
                                                   annual_from=annual_from,annual_to=annual_to,annual_number_of_leave_days=annual_number_of_leave_days,annual_remark=annual_remark,
                                                   non_paid_from=non_paid_from,non_paid_to=non_paid_to,non_paid_number_of_leave_days=non_paid_number_of_leave_days,non_paid_remark=non_paid_remark,
                                                   wedding_from=wedding_from,wedding_to=wedding_to,wedding_number_of_leave_days=wedding_number_of_leave_days,wedding_remark=wedding_remark,
                                                   bereavement_from=bereavement_from,bereavement_to=bereavement_to,bereavement_number_of_leave_days=bereavement_number_of_leave_days,bereavement_remark=bereavement_remark,
                                                   maternity_obstetric_from=maternity_obstetric_from,maternity_obstetric_to=maternity_obstetric_to,maternity_obstetric_number_of_leave_days=maternity_obstetric_number_of_leave_days,maternity_obstetric_remark=maternity_obstetric_remark,
                                                   sick_from=sick_from,sick_to=sick_to,sick_number_of_leave_days=sick_number_of_leave_days,sick_remark=sick_remark,
                                                   offinlieu_from=offinlieu_from,offinlieu_to=offinlieu_to,offinlieu_number_of_leave_days=offinlieu_number_of_leave_days,offinlieu_remark=offinlieu_remark,
                                                   other_from=other_from,other_to=other_to,other_number_of_leave_days=other_number_of_leave_days,other_remark=other_remark,
                                                   total_days=total_days,temporary_replacement=temporary_replacement,application_date=application_date, approved_by=manager, status=status,hr_status=hr_status)  
        leave_application_info.save()
        messages.success(request, 'SUCCESS: Application registered')
        
    return render(request, 'employee/leave_application.html', {
        'employee' : employee,
        'application_date':application_date,
        'list_employee' : list_employee,
        'manager' : manager,
        
    })
    

def leave_view(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    # Get Leave application
    leave_application = Leave_application.objects.get(pk=pk)
    manager_status_id = leave_application.status.id
    hr_status_id = leave_application.hr_status.id
    
   
    
    
    return render(request, 'employee/view_leave_application.html', {
        'employee' : employee,
        'leave_application' : leave_application,
        'manager_status_id' : manager_status_id,
        'hr_status_id' : hr_status_id,
        
    })
    

def leave_verification(request):
    today = datetime.now()
    
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id and role
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get all Leave application in present year
    list_present_year_leave_application = Leave_application.objects.filter(application_date__year = today.year).order_by('application_date')
    
    # Get Leave application của employee đang đăng nhập ( user )
    list_leave_application = Leave_application.objects.filter(employee=employee_pk, application_date__month = today.month)
    
    # Get Staff Leave application
    list_staff_application = Leave_application.objects.filter(approved_by=employee_pk, status=1)
    list_list_staff_application = list(list_staff_application)
    available_list_staff_application = 0
    if list_list_staff_application == []:
        available_list_staff_application = 0
    else:
        available_list_staff_application = 1
        
    # Get Leave application list for HR
    hr_list_leave_application = Leave_application.objects.filter(status = 2, hr_status=1)
    
    # Get Employee, Leave_type, Hour and Minute list
    list_employee = Employee.objects.all()
        
    return render(request, 'employee/leave_verification.html', {
        'employee' : employee,
        'list_leave_application' : list_leave_application,
        'list_employee' : list_employee,
        'list_staff_application' : list_staff_application,
        'available_list_staff_application' : available_list_staff_application,
        'role' : role,
        'hr_list_leave_application' : hr_list_leave_application,
        'list_present_year_leave_application' : list_present_year_leave_application,
    })
    

def leave_approve(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get today
    approved_date = date.today()
    
    # Get Leave application
    leave_application = Leave_application.objects.get(pk=pk)
    
     # Data input
    if request.POST.get('btn_approve'):
        status = Status.objects.get(id=2)
        leave_application.status = status
        leave_application.approved_date = approved_date
        leave_application.save()
        return redirect('/leave_verification/')
    if request.POST.get('btn_reject'):
        status = Status.objects.get(id=3)
        leave_application.status = status
        leave_application.approved_date = approved_date
        leave_application.save()
        return redirect('/leave_verification/')
    
    
        
    return render(request, 'employee/form_leave_approve.html', {
        'employee' : employee,
        'leave_application' : leave_application,
        'approved_date' : approved_date,
        
    })


def HR_leave_approve(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get today
    approved_date = today.date()
    
    # Get Leave application
    leave_application = Leave_application.objects.get(pk=pk)
    
     # Data input
    if request.POST.get('btn_approve'):
        status = Status.objects.get(id=2)
        # Annual
        annual_from = request.POST.get('annual_from')
        annual_to = request.POST.get('annual_to')
        annual_remark = request.POST.get('annual_remark')
        if annual_from != '' and annual_to != '':
            # Convert to datetime format
            annual_from_date = datetime.strptime(annual_from, '%Y-%m-%d')
            annual_to_date = datetime.strptime(annual_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if annual_from == annual_to:
                daily_work = Daily_work.objects.get(date=annual_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work, employee=leave_application.employee)
                    # Nghỉ full ngày
                if annual_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif annual_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if annual_from_date != annual_to_date:
                datesRange = date_range(annual_from_date, annual_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ 
                    if annual_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif annual_remark != '':
                        list_half_days_str = annual_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('annual_number_of_leave_days') == '':
            annual_number_of_leave_days = 0
        else:
            annual_number_of_leave_days = request.POST.get('annual_number_of_leave_days')
        
        
        # Non-paid
        non_paid_from = request.POST.get('non_paid_from')
        non_paid_to = request.POST.get('non_paid_to')
        non_paid_remark = request.POST.get('non_paid_remark')
        if non_paid_from != '' and non_paid_to != '':
            # Convert to datetime format
            non_paid_from_date = datetime.strptime(non_paid_from, '%Y-%m-%d')
            non_paid_to_date = datetime.strptime(non_paid_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if non_paid_from == non_paid_to:
                daily_work = Daily_work.objects.get(date=non_paid_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if non_paid_remark == '':
                    daily_work_employee.unpaid_leave = 1
                    daily_work_employee.paid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif non_paid_remark != '':
                    daily_work_employee.unpaid_leave = 0.5
                    daily_work_employee.paid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if non_paid_from_date != non_paid_to_date:
                datesRange = date_range(non_paid_from_date, non_paid_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if non_paid_remark == '':
                        daily_work_employee.unpaid_leave = 1
                        daily_work_employee.paid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif non_paid_remark != '':
                        list_half_days_str = non_paid_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.unpaid_leave = 0.5
                                daily_work_employee.paid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.unpaid_leave = 1
                                daily_work_employee.paid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')   
        if request.POST.get('non_paid_number_of_leave_days') == '':
            non_paid_number_of_leave_days = 0
        else:
            non_paid_number_of_leave_days = request.POST.get('non_paid_number_of_leave_days')
        
        # Wedding
        wedding_from = request.POST.get('wedding_from')
        wedding_to = request.POST.get('wedding_to')
        wedding_remark = request.POST.get('wedding_remark')
        if wedding_from != '' and wedding_to != '':
            # Convert to datetime format
            wedding_from_date = datetime.strptime(wedding_from, '%Y-%m-%d')
            wedding_to_date = datetime.strptime(wedding_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if wedding_from == wedding_to:
                daily_work = Daily_work.objects.get(date=wedding_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if wedding_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif wedding_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if wedding_from_date != wedding_to_date:
                datesRange = date_range(wedding_from_date, wedding_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if wedding_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif wedding_remark != '':
                        list_half_days_str = wedding_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('wedding_number_of_leave_days') == '':
            wedding_number_of_leave_days = 0
        else:
            wedding_number_of_leave_days = request.POST.get('wedding_number_of_leave_days')
        
        # Bereavement
        bereavement_from = request.POST.get('bereavement_from')
        bereavement_to = request.POST.get('bereavement_to')
        bereavement_remark = request.POST.get('bereavement_remark')
        if bereavement_from != '' and bereavement_to != '':
            # Convert to datetime format
            bereavement_from_date = datetime.strptime(bereavement_from, '%Y-%m-%d')
            bereavement_to_date = datetime.strptime(bereavement_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if bereavement_from == bereavement_to:
                daily_work = Daily_work.objects.get(date=bereavement_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if bereavement_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif bereavement_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if bereavement_from_date != bereavement_to_date:
                datesRange = date_range(bereavement_from_date, bereavement_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if bereavement_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif bereavement_remark != '':
                        list_half_days_str = bereavement_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('bereavement_number_of_leave_days') == '':
            bereavement_number_of_leave_days = 0
        else:
            bereavement_number_of_leave_days = request.POST.get('bereavement_number_of_leave_days')
        
        # Maternity / Obstetric
        maternity_obstetric_from = request.POST.get('maternity_obstetric_from')
        maternity_obstetric_to = request.POST.get('maternity_obstetric_to')
        maternity_obstetric_remark = request.POST.get('maternity_obstetric_remark')
        if maternity_obstetric_from != '' and maternity_obstetric_to != '':
            # Convert to datetime format
            maternity_obstetric_from_date = datetime.strptime(maternity_obstetric_from, '%Y-%m-%d')
            maternity_obstetric_to_date = datetime.strptime(maternity_obstetric_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if maternity_obstetric_from == maternity_obstetric_to:
                daily_work = Daily_work.objects.get(date=maternity_obstetric_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if maternity_obstetric_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif maternity_obstetric_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if maternity_obstetric_from_date != maternity_obstetric_to_date:
                datesRange = date_range(maternity_obstetric_from_date, maternity_obstetric_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if maternity_obstetric_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif maternity_obstetric_remark != '':
                        list_half_days_str = maternity_obstetric_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('maternity_obstetric_number_of_leave_days') == '':
            maternity_obstetric_number_of_leave_days = 0
        else:
            maternity_obstetric_number_of_leave_days = request.POST.get('maternity_obstetric_number_of_leave_days')
        # Sick
        sick_from = request.POST.get('sick_from')
        sick_to = request.POST.get('sick_to')
        sick_remark = request.POST.get('sick_remark')
        if sick_from != '' and sick_to != '':
            # Convert to datetime format
            sick_from_date = datetime.strptime(sick_from, '%Y-%m-%d')
            sick_to_date = datetime.strptime(sick_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if sick_from == sick_to:
                daily_work = Daily_work.objects.get(date=sick_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if sick_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif sick_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if sick_from_date != sick_to_date:
                datesRange = date_range(sick_from_date, sick_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if sick_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif sick_remark != '':
                        list_half_days_str = sick_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('sick_number_of_leave_days') == '':
            sick_number_of_leave_days = 0
        else:
            sick_number_of_leave_days = request.POST.get('sick_number_of_leave_days')
        # Off in-lieu
        offinlieu_from = request.POST.get('offinlieu_from')
        offinlieu_to = request.POST.get('offinlieu_to')
        offinlieu_remark = request.POST.get('offinlieu_remark')
        if offinlieu_from != '' and offinlieu_to != '':
            # Convert to datetime format
            offinlieu_from_date = datetime.strptime(offinlieu_from, '%Y-%m-%d')
            offinlieu_to_date = datetime.strptime(offinlieu_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if offinlieu_from == offinlieu_to:
                daily_work = Daily_work.objects.get(date=offinlieu_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if offinlieu_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif offinlieu_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if offinlieu_from_date != offinlieu_to_date:
                datesRange = date_range(offinlieu_from_date, offinlieu_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if offinlieu_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif offinlieu_remark != '':
                        list_half_days_str = offinlieu_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('offinlieu_number_of_leave_days') == '':
            offinlieu_number_of_leave_days = 0
        else:
            offinlieu_number_of_leave_days = request.POST.get('offinlieu_number_of_leave_days')
        # Other
        other_from = request.POST.get('other_from')
        other_to = request.POST.get('other_to')
        other_remark = request.POST.get('other_remark')
        if other_from != '' and other_to != '':
            # Convert to datetime format
            other_from_date = datetime.strptime(other_from, '%Y-%m-%d')
            other_to_date = datetime.strptime(other_to, '%Y-%m-%d')
            # Link Leave to Daily_work_employee
            # Nghỉ trong cùng 1 ngày:
            if other_from == other_to:
                daily_work = Daily_work.objects.get(date=other_from_date)
                daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work , employee=leave_application.employee)
                    # Nghỉ full ngày
                if other_remark == '':
                    daily_work_employee.paid_leave = 1
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                    # Nghỉ 1/2 ngày
                elif other_remark != '':
                    daily_work_employee.paid_leave = 0.5
                    daily_work_employee.unpaid_leave = 0
                    daily_work_employee.leave_application = leave_application
                    daily_work_employee.save()
                else:
                    messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
                
            
            # Nghỉ nhiều ngày:
            if other_from_date != other_to_date:
                datesRange = date_range(other_from_date, other_to_date)
                list_daily_work = Daily_work.objects.filter(date__in=datesRange)
                for index, daily_work in enumerate(list_daily_work):
                    daily_work_employee = Daily_work_for_employee.objects.get(daily_work=daily_work,employee=leave_application.employee)
                    # Nghỉ nhiều ngày không lẻ
                    if other_remark == '':
                        daily_work_employee.paid_leave = 1
                        daily_work_employee.unpaid_leave = 0
                        daily_work_employee.leave_application = leave_application
                        daily_work_employee.save()
                    # Nghỉ nhiều ngày có lẻ
                    elif other_remark != '':
                        list_half_days_str = other_remark.split()
                        for half_day_str in list_half_days_str:
                            half_day_date = datetime.strptime(half_day_str, '%d/%m/%Y').date()
                            if daily_work_employee.daily_work.date == half_day_date:
                                daily_work_employee.paid_leave = 0.5
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                                break
                            elif daily_work_employee.daily_work.date != half_day_date:
                                daily_work_employee.paid_leave = 1
                                daily_work_employee.unpaid_leave = 0
                                daily_work_employee.leave_application = leave_application
                                daily_work_employee.save()
                    else:
                        messages.error(request, 'ERROR: Wrong time format, please check NOTES!')
        if request.POST.get('other_number_of_leave_days') == '':
            other_number_of_leave_days = 0
        else:
            other_number_of_leave_days = request.POST.get('other_number_of_leave_days')
        # SAVE LEAVE APLLICATION AFTER EDIT AND APPROVE
        # Annual
        leave_application.annual_from = annual_from
        leave_application.annual_to = annual_to
        leave_application.annual_number_of_leave_days = annual_number_of_leave_days
        leave_application.annual_remark = annual_remark
        # Non-paid
        leave_application.non_paid_from = non_paid_from
        leave_application.non_paid_to = non_paid_to
        leave_application.non_paid_number_of_leave_days = non_paid_number_of_leave_days
        leave_application.non_paid_remark = non_paid_remark
        # Wedding
        leave_application.wedding_from = wedding_from
        leave_application.wedding_to = wedding_to
        leave_application.wedding_number_of_leave_days = wedding_number_of_leave_days
        leave_application.wedding_remark = wedding_remark
        # Bereavement
        leave_application.bereavement_from = bereavement_from
        leave_application.bereavement_to = bereavement_to
        leave_application.bereavement_number_of_leave_days = bereavement_number_of_leave_days
        leave_application.bereavement_remark = bereavement_remark
        # Maternity / Obstetric
        leave_application.maternity_obstetric_from = maternity_obstetric_from
        leave_application.maternity_obstetric_to = maternity_obstetric_to
        leave_application.maternity_obstetric_number_of_leave_days = maternity_obstetric_number_of_leave_days
        leave_application.maternity_obstetric_remark = maternity_obstetric_remark
        # Sick
        leave_application.sick_from = sick_from
        leave_application.sick_to = sick_to
        leave_application.sick_number_of_leave_days = sick_number_of_leave_days
        leave_application.sick_remark = sick_remark
        # Off in-lieu
        leave_application.offinlieu_from = offinlieu_from
        leave_application.offinlieu_to = offinlieu_to
        leave_application.offinlieu_number_of_leave_days = offinlieu_number_of_leave_days
        leave_application.offinlieu_remark = offinlieu_remark
        # Other
        leave_application.other_from = other_from
        leave_application.other_to = other_to
        leave_application.other_number_of_leave_days = other_number_of_leave_days
        leave_application.other_remark = other_remark
        # Total days off
        total_days_off = float(annual_number_of_leave_days) + float(non_paid_number_of_leave_days) + float(wedding_number_of_leave_days) + float(bereavement_number_of_leave_days) + float(maternity_obstetric_number_of_leave_days) + float(sick_number_of_leave_days) + float(offinlieu_number_of_leave_days) + float(other_number_of_leave_days)
        leave_application.total_days = total_days_off
        # Update used and remain dayoff in Dayoff model
        total_paid_leave = float(annual_number_of_leave_days) + float(wedding_number_of_leave_days) + float(bereavement_number_of_leave_days) + float(maternity_obstetric_number_of_leave_days) + float(sick_number_of_leave_days) + float(offinlieu_number_of_leave_days) + float(other_number_of_leave_days)
        period = Period.objects.get(period_year=leave_application.application_date.year)
        dayoff = Dayoff.objects.get(period=period, employee=leave_application.employee)
        if dayoff.previous_remain_dayoff != 0:
            if dayoff.previous_remain_dayoff >= total_paid_leave:
                dayoff.previous_remain_dayoff = dayoff.previous_remain_dayoff - total_paid_leave
            else:
                remain_total_paid_leave = total_paid_leave - dayoff.previous_remain_dayoff
                dayoff.used_dayoff = dayoff.used_dayoff + remain_total_paid_leave
                dayoff.remain_dayoff = dayoff.remain_dayoff - remain_total_paid_leave
                dayoff.previous_remain_dayoff = 0
        else:
            dayoff.used_dayoff = dayoff.used_dayoff + total_paid_leave
            dayoff.remain_dayoff = dayoff.remain_dayoff - total_paid_leave
            dayoff.previous_remain_dayoff = 0
        dayoff.save()
        # Create Update_dayoff model
        update_dayoff_info = Update_dayoff(leave_application=leave_application,day_off=dayoff
                                           ,minus_dayoff=total_paid_leave,reason_of_changing='leave')
        update_dayoff_info.save()
        
        
        # Status
        leave_application.hr_status = status
        leave_application.hr_approved_date = approved_date
        leave_application.save()
        # return redirect('/leave_verification/')
    if request.POST.get('btn_reject'):
        status = Status.objects.get(id=3)
        leave_application.hr_status = status
        leave_application.hr_approved_date = approved_date
        leave_application.save()
        
        return redirect('/leave_verification/')

    
        
    return render(request, 'employee/form_HR_leave_approve.html', {
        'employee' : employee,
        'leave_application' : leave_application,
        'approved_date' : approved_date,
        
    })
    
    
def ot_application(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get manager:
    employee_id_in_Employee_model = int(employee_pk)
    manager_id_in_Manager_model = Employee_manager.objects.only('id').get(employee=employee_id_in_Employee_model)
    manager_int_id_in_Manager_model = int(manager_id_in_Manager_model.manager.id)
    manager = Employee.objects.get(pk=manager_int_id_in_Manager_model)
    
    # Get today date and current month
    application_date = date.today()
    application_month = application_date.month
    
    # Get Employee, Leave_type, Hour and Minute list
    list_employee = Employee.objects.all()
    
    
    # Data input
    if request.POST.get('btn_addot'):
        employee_id = Employee.objects.only('id').get(id=employee_pk)
        ot_date = request.POST.get('ot_date')
        ot_time_from = request.POST.get('ot_time_from')
        ot_time_to = request.POST.get('ot_time_to')
        ot_total_time = request.POST.get('ot_total_time')
        reason = request.POST.get('reason')
        status = Status.objects.get(id=1)
        hr_status = Status.objects.get(id=1)
        ot_application_info = Overtime_application(employee=employee_id,application_date=application_date,month=application_month,ot_date=ot_date,
                                                   ot_time_from=ot_time_from,ot_time_to=ot_time_to,ot_total_time=ot_total_time,
                                                   approved_by=manager,reason=reason,status=status,hr_status=hr_status)  
        ot_application_info.save()
        messages.success(request, 'SUCCESS: Application registered')
        
    return render(request, 'employee/ot_application.html', {
        'employee' : employee,
        'application_date':application_date,
        'application_month' : application_month,
        'list_employee' : list_employee,
        'manager' : manager,
        
    })
    

def ot_verification(request):
    today = datetime.now()
    
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get all Leave application in present year
    list_present_year_ot_application = Overtime_application.objects.filter(application_date__year = today.year).order_by('application_date')
    
    # Get ot application
    list_ot_application = Overtime_application.objects.filter(employee=employee_pk, application_date__month = today.month)
    
    # Get Staff ot application
    list_staff_application = Overtime_application.objects.filter(approved_by=employee_pk, status=1)
    list_list_staff_application = list(list_staff_application)
    available_list_staff_application = 0
    if list_list_staff_application == []:
        available_list_staff_application = 0
    else:
        available_list_staff_application = 1
    
    # Get Employee, Leave_type, Hour and Minute list
    list_employee = Employee.objects.all()
    
     # Get OT application list for HR
    hr_ot_leave_application = Overtime_application.objects.filter(status = 2, hr_status=1)
        
    return render(request, 'employee/ot_verification.html', {
        'employee' : employee,
        'list_ot_application' : list_ot_application,
        'list_employee' : list_employee,
        'list_staff_application' : list_staff_application,
        'available_list_staff_application' : available_list_staff_application,
        'role' : role,
        'hr_ot_leave_application' : hr_ot_leave_application,
        'list_present_year_ot_application' : list_present_year_ot_application,
    })
    

def ot_approve(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Get employee:
    employee = Employee.objects.get(pk=employee_pk)
    
    # Get today
    approved_date = date.today()
    
    # Get Ot application
    ot_application = Overtime_application.objects.get(pk=pk)
    
     # Data input
    if role == 3:
        if request.POST.get('btn_approve'):
            approve_type = request.POST.get('type')
            time_input = request.POST.get('time_input')
            if approve_type == 'recuperation':
                ot_application.ot_unpaid_day = time_input
                period = Period.objects.get(period_year = ot_application.application_date.year)
                dayoff = Dayoff.objects.get(period=period, employee=ot_application.employee)
                dayoff.remain_dayoff = dayoff.remain_dayoff + float(time_input)
                dayoff.save()
            elif approve_type == 'overtime':
                ot_application.ot_paid_hour = time_input
                # Làm tiếp phần trả lương sau khi đã có paid_hour
            status = Status.objects.get(id=2)
            ot_application.hr_status = status
            ot_application.hr_approved_date = approved_date
            ot_application.save()
            # Create Update_recuperation model
            period = Period.objects.get(period_year=ot_application.application_date.year)
            dayoff = Dayoff.objects.get(period=period, employee=ot_application.employee)
            update_dayoff_info = Update_dayoff(ot_application=ot_application,day_off=dayoff
                                           ,plus_dayoff=time_input,reason_of_changing='ot')
            update_dayoff_info.save()
            return redirect('/ot_verification/')
        elif request.POST.get('btn_reject'):
            status = Status.objects.get(id=3)
            ot_application.hr_status = status
            ot_application.hr_approved_date = approved_date
            ot_application.save()
            return redirect('/ot_verification/')
    else:
        if request.POST.get('btn_approve'):
            status = Status.objects.get(id=2)
            ot_application.status = status
            ot_application.approved_date = approved_date
            ot_application.save()
            return redirect('/ot_verification/')
        elif request.POST.get('btn_reject'):
            status = Status.objects.get(id=3)
            ot_application.status = status
            ot_application.approved_date = approved_date
            ot_application.save()
            return redirect('/ot_verification/')
    
    
        
    return render(request, 'employee/form_ot_approve.html', {
        'role' : role,
        'employee' : employee,
        'ot_application' : ot_application,
        'approved_date' : approved_date,
        
    })


# Period and Dayoff
def blank_period(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 1 or s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get period
    try:
        period = Period.objects.get(period_year=today.year)
        return redirect('employee:period', pk=period.pk)
    except Period.DoesNotExist:
        pass
    
    
    # Start new period
    if request.POST.get('btnStartPeriod'):
        period_year = request.POST.get('period_year')
        total_months = request.POST.get('total_months')
        start_period_date = request.POST.get('start_period_date')
        end_period_date = request.POST.get('end_period_date')
        period_info = Period(period_year=period_year,total_months=total_months,start_period_date=start_period_date,end_period_date=end_period_date)  
        period_info.save()
        messages.success(request, 'SUCCESS: Period started')
        # Update years of service và tạo dayoff cho tất cả nhân viên sau khi đã tạo period
        list_employee = Employee.objects.all()
        for employee in list_employee:
            # Lấy thông tin employee để update years_of_service
            present_year = today.year
            if employee.joining_year == present_year:
                employee.years_of_service = 1
            else:
                employee.years_of_service = present_year - employee.joining_year
            employee.save() 
            # Tạo dayoff cho tất cả nhân viên
            period = Period.objects.get(period_year=period_year)
            if employee.years_of_service == 1:
                if employee.joining_date.month == 1:
                    total_dayoff = 12
                elif employee.joining_date.month == 2:
                    total_dayoff = 11
                elif employee.joining_date.month == 3:
                    total_dayoff = 10
                elif employee.joining_date.month == 4:
                    total_dayoff = 9
                elif employee.joining_date.month == 5:
                    total_dayoff = 8
                elif employee.joining_date.month == 6:
                    total_dayoff = 7
                elif employee.joining_date.month == 7:
                    total_dayoff = 6
                elif employee.joining_date.month == 8:
                    total_dayoff = 5
                elif employee.joining_date.month == 9:
                    total_dayoff = 4
                elif employee.joining_date.month == 10:
                    total_dayoff = 3
                elif employee.joining_date.month == 11:
                    total_dayoff = 2
                elif employee.joining_date.month == 12:
                    total_dayoff = 1
            else:
                
                if employee.years_of_service > 1 and employee.years_of_service < 5:
                    total_dayoff = 12
                elif employee.years_of_service >= 5 and employee.years_of_service < 10:
                    total_dayoff = 13
                elif employee.years_of_service >= 10 and employee.years_of_service < 15:
                    total_dayoff = 14
                elif employee.years_of_service >= 15 and employee.years_of_service < 20:
                    total_dayoff = 15
                elif employee.years_of_service >= 20 and employee.years_of_service < 25:
                    total_dayoff = 16
                elif employee.years_of_service >= 25 and employee.years_of_service < 30:
                    total_dayoff = 17
                elif employee.years_of_service >= 30 and employee.years_of_service < 35:
                    total_dayoff = 18
                elif employee.years_of_service >= 35 and employee.years_of_service < 40:
                    total_dayoff = 19
                elif employee.years_of_service >= 40 and employee.years_of_service < 45:
                    total_dayoff = 20
                elif employee.years_of_service >= 45 and employee.years_of_service < 50:
                    total_dayoff = 21
            int_period_year = int(period_year)
            try:
                previous_period = Period.objects.get(period_year=int_period_year-1)
                previous_dayoff = Dayoff.objects.get(period=previous_period, employee=employee.id)
                previous_remain_dayoff = previous_dayoff.remain_dayoff
            except Period.DoesNotExist:
                previous_period = None
                previous_remain_dayoff = 0      
            dayoff_info = Dayoff(period=period,employee=employee,
                                 total_dayoff=total_dayoff,remain_dayoff=total_dayoff,previous_remain_dayoff=previous_remain_dayoff,
                                 used_dayoff=0)
            dayoff_info.save()
        return redirect('employee:period', pk=period_info.pk)
    
    
    
    return render(request, 'employee/period_blank.html', {
        'role' : role
    })
    
    
def period(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 1 or s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    
    # Get period
    try:
        period = Period.objects.get(pk=pk)
    except Period.DoesNotExist:
        return redirect('employee:blank_period')
    
    # Previous and next period button
    if request.POST.get('btn_previousperiod'):
        try:
            previous_period = Period.objects.get(period_year=period.period_year-1)
            return redirect('employee:period',pk=previous_period.id)
        except Period.DoesNotExist:
            messages.error(request, 'Period does not exist.')
    
    if request.POST.get('btn_nextperiod'):
        try:
            previous_period = Period.objects.get(period_year=period.period_year+1)
            return redirect('employee:period',pk=previous_period.id)
        except Period.DoesNotExist:
            messages.error(request, 'Period does not exist.')

    
    # Start new period
    if request.POST.get('btnStartPeriod'):
        period_year = request.POST.get('period_year')
        total_months = request.POST.get('total_months')
        start_period_date = request.POST.get('start_period_date')
        end_period_date = request.POST.get('end_period_date')
        period_info = Period(period_year=period_year,total_months=total_months,start_period_date=start_period_date,end_period_date=end_period_date)  
        period_info.save()
        messages.success(request, 'SUCCESS: Period started')
        # Update years of service và tạo dayoff cho tất cả nhân viên sau khi đã tạo period
        list_employee = Employee.objects.filter(active=1)
        for employee in list_employee:
            # Lấy thông tin employee để update years_of_service
            present_year = today.year
            if employee.joining_year == present_year:
                employee.years_of_service = 1
            else:
                employee.years_of_service = present_year - employee.joining_year + 1
            employee.save() 
            # Tạo dayoff cho tất cả nhân viên
            period = Period.objects.get(period_year=period_year)
            if employee.years_of_service == 1:
                if employee.joining_date.month == 1:
                    total_dayoff = 12
                elif employee.joining_date.month == 2:
                    total_dayoff = 11
                elif employee.joining_date.month == 3:
                    total_dayoff = 10
                elif employee.joining_date.month == 4:
                    total_dayoff = 9
                elif employee.joining_date.month == 5:
                    total_dayoff = 8
                elif employee.joining_date.month == 6:
                    total_dayoff = 7
                elif employee.joining_date.month == 7:
                    total_dayoff = 6
                elif employee.joining_date.month == 8:
                    total_dayoff = 5
                elif employee.joining_date.month == 9:
                    total_dayoff = 4
                elif employee.joining_date.month == 10:
                    total_dayoff = 3
                elif employee.joining_date.month == 11:
                    total_dayoff = 2
                elif employee.joining_date.month == 12:
                    total_dayoff = 1
            else:
                
                if employee.years_of_service > 1 and employee.years_of_service < 5:
                    total_dayoff = 12
                elif employee.years_of_service >= 5 and employee.years_of_service < 10:
                    total_dayoff = 13
                elif employee.years_of_service >= 10 and employee.years_of_service < 15:
                    total_dayoff = 14
                elif employee.years_of_service >= 15 and employee.years_of_service < 20:
                    total_dayoff = 15
                elif employee.years_of_service >= 20 and employee.years_of_service < 25:
                    total_dayoff = 16
                elif employee.years_of_service >= 25 and employee.years_of_service < 30:
                    total_dayoff = 17
                elif employee.years_of_service >= 30 and employee.years_of_service < 35:
                    total_dayoff = 18
                elif employee.years_of_service >= 35 and employee.years_of_service < 40:
                    total_dayoff = 19
                elif employee.years_of_service >= 40 and employee.years_of_service < 45:
                    total_dayoff = 20
                elif employee.years_of_service >= 45 and employee.years_of_service < 50:
                    total_dayoff = 21
            int_period_year = int(period_year)
            try:
                previous_period = Period.objects.get(period_year=int_period_year-1)
                previous_dayoff = Dayoff.objects.get(period=previous_period, employee=employee.id)
                previous_remain_dayoff = previous_dayoff.remain_dayoff
            except Period.DoesNotExist:
                previous_period = None
                previous_remain_dayoff = 0        
            dayoff_info = Dayoff(period=period,employee=employee,
                                 total_dayoff=total_dayoff,remain_dayoff=total_dayoff,previous_remain_dayoff=previous_remain_dayoff,used_dayoff=0)
            dayoff_info.save()
    
    
    # Reset previous dayoff
    if request.POST.get('btnReset'):    
        present_period = Period.objects.get(period_year=today.year)
        list_dayoff = Dayoff.objects.filter(period=present_period)
        for dayoff in list_dayoff:
            dayoff.previous_remain_dayoff = 0
            dayoff.save()
        messages.success(request, 'SUCCESS: Remain leave reset')
     
    
    # Get month in period
    month_in_period = Month_in_period.objects.filter(period=period)

        
    # Add month to current PERIOD
    if request.POST.get('btnAddMonth'):    
        month_name = request.POST.get('month_name')
        month_number = request.POST.get('month_number')
        total_days = int(monthrange(period.period_year, int(month_number))[1])
        holidays = request.POST.get('holidays')
        total_work_days_bo = request.POST.get('total_work_days_bo')
        total_work_days_wh = request.POST.get('total_work_days_wh')
        month_info = Month_in_period(period=period,month_name=month_name,month_number=month_number,
                                     total_days=total_days,holidays=holidays,total_work_days_bo=total_work_days_bo,total_work_days_wh=total_work_days_wh)  
        month_info.save()
        messages.success(request, 'SUCCESS: Month created')
        # Create daily work
        for number_day in range(1,int(total_days)+1):
                month = Month_in_period.objects.get(month_name=month_name)
                day_str = str(number_day)
                month_str = str(month.month_number)
                year_str = str(month.period.period_year)
                date_str = day_str + '/' + month_str + '/' + year_str
                date_before_format = datetime.strptime(date_str, '%d/%m/%Y')
                date = date_before_format.strftime("%d/%m/%Y")
                if date_before_format.weekday() < 5:
                    weekend = False
                else:
                    weekend = True
                find_result = holidays.find(date)    
                if find_result >= 0:
                    holiday = True
                else:
                    holiday = False
                daily_work_info = Daily_work(month=month,date=date_before_format,weekend=weekend,holiday=holiday)
                daily_work_info.save()
        
        # Create each employee a daily_work        
        list_employee = Employee.objects.filter(active=1)
        list_daily_work = Daily_work.objects.filter(month=month)
        for employee in list_employee:
            for daily_work in list_daily_work:
                if daily_work.date.weekday() < 5:
                    daily_work_info_for_employee = Daily_work_for_employee(employee=employee,daily_work=daily_work,work=1)
                    daily_work_info_for_employee.save()
                else:
                    daily_work_info_for_employee = Daily_work_for_employee(employee=employee,daily_work=daily_work)
                    daily_work_info_for_employee.save()
        # Add 1/2 work day on Saturday for Warehouse employees
        list_daily_work = Daily_work.objects.filter(month=month)
        warehouse_department_e = Department_E.objects.get(department_e='Warehouse')
        list_warehouse_employees = Employee.objects.filter(department_e=warehouse_department_e)
        for warehouse_employee in list_warehouse_employees:
            list_warehouse_employee_daily_work = Daily_work_for_employee.objects.filter(employee=warehouse_employee,daily_work__in=list_daily_work)
            for daily_work_warehouse_employee in list_warehouse_employee_daily_work:
                if daily_work_warehouse_employee.daily_work.date.weekday() == 5:
                    daily_work_warehouse_employee.work = 0.5
                    daily_work_warehouse_employee.save()
    

    
    return render(request, 'employee/period.html', {
        'role' : role,
        'period':period,
        'month_in_period' : month_in_period,
    })
    

    
    
def list_time_sheets(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 1 or s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    

    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    
    list_days_in_month = Daily_work.objects.filter(month=period_month)
    if role == 3:
        list_employees = Employee.objects.all()
    else:
        list_staff = Employee_manager.objects.filter(manager=s_user[2])
        list_employee_id = []
        for staff in list_staff:
            list_employee_id.append(staff.employee.id)
        list_employees = Employee.objects.filter(id__in=list_employee_id)
    list_data = []
    for employee in list_employees:        
        # Get total_salary_working_day 
        list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_days_in_month, work__gt=0)
        total_working_day = 0
        for daily_work_info in list_daily_work_info:
            total_working_day += daily_work_info.work
        # Get leave
        list_paid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_days_in_month,work__gt=0, paid_leave__gt=0)
        total_paid_leave_day = 0
        for paid_leave_info in list_paid_leave_info:
            total_paid_leave_day += paid_leave_info.paid_leave
        
        list_unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_days_in_month,work__gt=0, unpaid_leave__gt=0)
        total_unpaid_leave_day = 0
        for unpaid_leave_info in list_unpaid_leave_info:
            total_unpaid_leave_day += unpaid_leave_info.unpaid_leave
        # Get OT hour to pay salary
        ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
        total_paid_hour = 0
        for application in ot_applications:
            total_paid_hour += application.ot_paid_hour
        # Make data    
        data = {
            'employee': employee,
            'total_paid_leave_days': total_paid_leave_day,
            'total_unpaid_leave_days': total_unpaid_leave_day,
            'total_salary_working_day': total_working_day - total_unpaid_leave_day,
            'total_ot_paid_hour': total_paid_hour,
             
        }
        list_data.append(data)
    
        
        
    # Add month to current PERIOD
    list_employee_days = None
    employee_full_name = None
    if request.POST.get('get_timesheet'):   
        file_name = str(period_month.month_name) + '_timesheets.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 640, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'white')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'white')
        # Style for day
        # Weekend
        style_weekend = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'pale_blue')
        # Holiday
        style_holiday = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'lavender')
        # paid_leave
        style_paid_leave = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'yellow')
        # unpaid_leave
        style_unpaid_leave = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'orange')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Timesheet')

        # Table
        # Set col width
        ws.col(0).width = 5000
        ws.col(1).width = 6000
        ws.col(2).width = 5000
        # Top
        ws.write_merge(0, 0, 0, 6, 'TIMESHEETS', style_head)
        ws.write_merge(0, 0, 9, 11, str(period_month.month_name),style_head)
        
        # Body
        # Body head
        ws.write(2, 0, 'Employee code', style_table_head)
        ws.write(2, 1, 'Full name', style_table_head)
        ws.write(2, 2, 'Department', style_table_head)
        ws.write(2, 3, 'Total paid leave days', style_table_head)
        ws.write(2, 4, 'Total unpaid leave days', style_table_head)
        ws.write(2, 5, 'Total salary working days', style_table_head)
        ws.write(2, 6, 'Total OT paid hour', style_table_head)
        for index,day in enumerate(list_days_in_month):
            if day.weekend == True:
                ws.write(2, 7+index, str(day.date.day), style_weekend)
            elif day.holiday == True:
                ws.write(2, 7+index, str(day.date.day), style_holiday)
            else:
                ws.write(2, 7+index, str(day.date.day), style_table_head)
        for index, data in enumerate(list_data):
            ws.write(3+index, 0, str(data['employee'].employee_code),style_normal)
            ws.write(3+index, 1, str(data['employee'].full_name),style_normal)
            ws.write(3+index, 2, str(data['employee'].department_e),style_normal)
            ws.write(3+index, 3, str(data['total_paid_leave_days']),style_normal)
            ws.write(3+index, 4, str(data['total_unpaid_leave_days']),style_normal)
            ws.write(3+index, 5, str(data['total_salary_working_day']),style_normal)
            ws.write(3+index, 6, str(data['total_ot_paid_hour']),style_normal)
        row = 0    
        for employee in list_employees:
            list_employee_days = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_days_in_month)
            for index,day in enumerate(list_employee_days):
                if day.daily_work.holiday == True:
                    ws.write(3+row, 7+index, str('HOL'),style_holiday)
                elif day.daily_work.weekend == True:
                    if day.work == 0.5:
                        ws.write(3+row, 7+index, str('1/2X'),style_weekend)
                    else:
                        ws.write(3+row, 7+index, str(''),style_weekend)
                elif day.paid_leave == 1.0:
                    ws.write(3+row, 7+index, str('P'),style_paid_leave)
                elif day.paid_leave == 0.5:
                    ws.write(3+row, 7+index, str('1/2P'),style_paid_leave)
                elif day.unpaid_leave == 1.0:
                    ws.write(3+row, 7+index, str('U'),style_unpaid_leave)
                elif day.unpaid_leave == 0.5:
                    ws.write(3+row, 7+index, str('1/2U'),style_unpaid_leave)
                elif day.work == 1:
                    ws.write(3+row, 7+index, str('1X'),style_normal)
            row += 1   


        wb.save(response)
        return response  
    
    return render(request, 'employee/time_sheets_list.html', {
        'role' : role,
        'period_month' : period_month,
        'list_data' : list_data,
        'employee_full_name' : employee_full_name,
        'list_employee_days' : list_employee_days,
    })
    

def payroll_tedis(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    

    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    
    
    # Get payroll HCM data
    site_RO = Site.objects.get(site='RO')
    area_HCM = Area.objects.get(area='HCMC')
    list_employee_tedis_HCM = Employee.objects.filter(site=site_RO, area=area_HCM)
    # Get total_working_days
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    daily_work_info = Daily_work_for_employee.objects.filter(employee=list_employee_tedis_HCM[0], daily_work__in=list_work_days)
    total_working_day = daily_work_info.count()
    # Create payroll dict
    list_payroll_HCM_info = []
    for employee in list_employee_tedis_HCM:
        try:
            payroll_info = Payroll_Tedis.objects.get(employee=employee,month=period_month)
            payrollExist = 1
            # Make data
            # Get working days
            list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
            daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
            unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
            working_days = daily_work_info.count() - unpaid_leave_info.count()    
            data = {
                'payroll_info': payroll_info,
                
                
            }
            list_payroll_HCM_info.append(data)
        except Payroll_Tedis.DoesNotExist:
            payrollExist = 0
            
    # Get payroll HANOI data
    site_RO = Site.objects.get(site='RO')
    area_HANOI = Area.objects.get(area='HANOI')
    list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
    # Get total_working_days
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    daily_work_info = Daily_work_for_employee.objects.filter(employee=list_employee_tedis_HANOI[0], daily_work__in=list_work_days)
    total_working_day = daily_work_info.count()
    # Create payroll dict
    list_payroll_HANOI_info = []
    for employee in list_employee_tedis_HANOI:
        try:
            payroll_info = Payroll_Tedis.objects.get(employee=employee,month=period_month)
            payrollExist = 1
            # Make data
            # Get working days
            list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
            daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
            unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
            working_days = daily_work_info.count() - unpaid_leave_info.count()    
            data = {
                'payroll_info': payroll_info,
                
                
            }
            list_payroll_HANOI_info.append(data)
        except Payroll_Tedis.DoesNotExist:
            payrollExist = 0
        
    # Create payroll data
    if request.POST.get('btn_adjust_percent'):
        '''Payroll HCM'''
        # Get % Adjust  
        adjust_percent = float(request.POST.get('adjust_percent'))
        
        site_RO = Site.objects.get(site='RO')
        area_HCM = Area.objects.get(area='HCMC')
        list_employee_tedis_HCM = Employee.objects.filter(site=site_RO, area=area_HCM)
        for employee in list_employee_tedis_HCM:
            # Get Salary info
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
            if list_contracts.count() == 0:
                newest_salary = 0
            else:
                newest_salary = list_contracts[0].basic_salary
            # Get working days
            list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
            daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
            unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
            working_days = daily_work_info.count() - unpaid_leave_info.count()
            total_working_day = daily_work_info.count()
            # Get gross income
            gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(total_working_day) )
            # Get salary_recuperation
            salary_recuperation = 0
            # Get OT hour to pay salary
            ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
            total_paid_hour = 0
            for application in ot_applications:
                total_paid_hour += application.ot_paid_hour
            salary_per_hour = newest_salary/total_working_day/8
            overtime = round(salary_per_hour * total_paid_hour)
            # Get transportation, phone, lunch, training_fee, toxic_allowance, travel, responsibility, seniority_bonus
            if list_contracts.count() == 0:
                transportation = 0
                phone = 0
                lunch = 0
                training_fee = 0
                toxic_allowance = 0
                travel = 0
                responsibility = 0
                seniority_bonus = 0
            else:
                transportation = round(list_contracts[0].transportation_support * working_days / total_working_day)
                phone = round(list_contracts[0].telephone_support * working_days / total_working_day)
                lunch = round(list_contracts[0].lunch_support * working_days / total_working_day)
                training_fee = 0
                toxic_allowance = 0
                travel = round(list_contracts[0].travel_support * working_days / total_working_day)
                responsibility = round(list_contracts[0].responsibility_allowance * working_days / total_working_day)
                seniority_bonus = round(list_contracts[0].seniority_bonus * working_days / total_working_day)
            # Get other, total_allowance_recuperation, benefits, severance_allowance, outstanding_annual_leave, month_13_salary_Pro_ata
            other = 0
            total_allowance_recuperation = 0
            benefits = 0
            severance_allowance = 0 
            outstanding_annual_leave = 0
            month_13_salary_Pro_ata = 0
            # Get SHUI_10point5percent_employee_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.095
                    else: 
                        first_value = combo * 0.095
                    
                    # 2nd if
                    if combo > 93600000:
                        second_value = 93600000 * 0.01
                    else: 
                        second_value = combo * 0.01
                    SHUI_10point5percent_employee_pay = round(first_value + second_value)
                else: 
                    SHUI_10point5percent_employee_pay = 0
            else:
                SHUI_10point5percent_employee_pay = 0
            # Get recuperation_of_SHU_Ins_10point5percent_staff_pay
            recuperation_of_SHU_Ins_10point5percent_staff_pay = 0
            # Get SHUI_21point5percent_company_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.205
                    else: 
                        first_value = combo * 0.205
                    
                    # 2nd if
                    if combo > 93600000:
                        second_value = 93600000 * 0.01
                    else: 
                        second_value = combo * 0.01
                    SHUI_21point5percent_company_pay = round(first_value + second_value)
                else: 
                    SHUI_21point5percent_company_pay = 0
            else:
                SHUI_21point5percent_company_pay = 0
            # Get recuperation_of_SHU_Ins_21point5percent_company_pay
            recuperation_of_SHU_Ins_21point5percent_company_pay = 0
            # Get occupational_accident_and_disease
            occupational_accident_and_disease = 0
            # Get trade_union_fee_company_pay_2percent
            combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
            if SHUI_10point5percent_employee_pay > 0: 
                if combo > 29800000:
                    SalarytoBH = 29800000
                else:
                    SalarytoBH = combo
            else:
                SalarytoBH = 0
            trade_union_fee_company_pay_2percent = round(SalarytoBH * 2/100)
            # Get trade_union_fee_member
            if trade_union_fee_company_pay_2percent > 0:
                trade_union_fee_member = 4680000 * 1/100
            else:
                trade_union_fee_member = 0
            # Get family_deduction
            list_of_dependents = Employee_children.objects.filter(employee=employee)
            number_of_dependents = list_of_dependents.count()
            family_deduction = 11000000 + (number_of_dependents * 4400000)
            # Get taxable_income
            contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus :
                    sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
                    taxable_income = sum_K_AA - lunch - severance_allowance + occupational_accident_and_disease
                else:
                    taxable_income = sum_K_AA - severance_allowance + occupational_accident_and_disease
            else:
                taxable_income = 0
            # Get taxed_income
            if taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction < 0:
                taxed_income = 0
            else:
                taxed_income = taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction
            # Get PIT
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus :
                    if 5000000 < taxed_income <= 10000000:
                        PIT_before_round = (taxed_income * 0.1) - 250000
                    elif 10000000 < taxed_income <= 18000000:
                        PIT_before_round = (taxed_income * 0.15) - 750000
                    elif 18000000 < taxed_income <= 32000000:
                        PIT_before_round = (taxed_income * 0.2) - 1650000
                    elif 32000000 < taxed_income <= 52000000:
                    
                        PIT_before_round = (taxed_income * 0.25) - 3250000
                    elif 52000000 < taxed_income <= 80000000:
                        PIT_before_round = (taxed_income * 0.3) - 5850000
                    elif taxed_income > 80000000:
                        PIT_before_round = (taxed_income * 0.35) - 9850000
                    else: 
                        PIT_before_round = taxed_income * 0.05
                elif taxed_income >= 2000000:
                    PIT_before_round = taxed_income * 10/100
                else:
                    PIT_before_round = 0                     
            else:
                PIT_before_round = 0
            PIT = round(PIT_before_round)
            # Get deduct
            deduct = 0
            # Get net_income
            sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
            net_income = sum_K_AA + occupational_accident_and_disease - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - PIT - deduct
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
            total_cost = round((sum_K_AA + SHUI_21point5percent_company_pay + recuperation_of_SHU_Ins_21point5percent_company_pay + occupational_accident_and_disease + trade_union_fee_company_pay_2percent + trade_union_fee_member + transfer_bank - deduct),1)
            

    
            
            payroll_employee_info = Payroll_Tedis(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,
                                                  gross_income=gross_income,salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch, training_fee=training_fee, toxic_allowance=toxic_allowance, travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                  other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata, 
                                                  recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,occupational_accident_and_disease=occupational_accident_and_disease,
                                                  trade_union_fee_company_pay_2percent=trade_union_fee_company_pay_2percent,trade_union_fee_member=trade_union_fee_member,
                                                  family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT=PIT,deduct=deduct,net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
            payroll_employee_info.save()
        
        
        '''Payroll HANOI'''
        # Get % Adjust  
        adjust_percent = float(request.POST.get('adjust_percent'))
        
        site_RO = Site.objects.get(site='RO')
        area_HANOI = Area.objects.get(area='HANOI')
        list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
        for employee in list_employee_tedis_HANOI:
            # Get Salary info
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
            if list_contracts.count() == 0:
                newest_salary = 0
            else:
                newest_salary = list_contracts[0].basic_salary
            # Get working days
            list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
            daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
            unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
            working_days = daily_work_info.count() - unpaid_leave_info.count()
            total_working_day = daily_work_info.count()
            # Get gross income
            gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(total_working_day),0)
            # Get salary_recuperation
            salary_recuperation = 0
            # Get OT hour to pay salary
            ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
            total_paid_hour = 0
            for application in ot_applications:
                total_paid_hour += application.ot_paid_hour
            salary_per_hour = newest_salary/total_working_day/8
            overtime = round(salary_per_hour * total_paid_hour,0)
            # Get transportation, phone, lunch, training_fee, toxic_allowance, travel, responsibility, seniority_bonus
            if list_contracts.count() == 0:
                transportation = 0
                phone = 0
                lunch = 0
                training_fee = 0
                toxic_allowance = 0
                travel = 0
                responsibility = 0
                seniority_bonus = 0
            else:
                transportation = round(list_contracts[0].transportation_support * working_days / total_working_day)
                phone = round(list_contracts[0].telephone_support * working_days / total_working_day)
                lunch = round(list_contracts[0].lunch_support * working_days / total_working_day)
                training_fee = 0
                toxic_allowance = 0
                travel = round(list_contracts[0].travel_support * working_days / total_working_day)
                responsibility = round(list_contracts[0].responsibility_allowance * working_days / total_working_day)
                seniority_bonus = round(list_contracts[0].seniority_bonus * working_days / total_working_day)
            # Get other, total_allowance_recuperation, benefits, severance_allowance, outstanding_annual_leave, month_13_salary_Pro_ata
            other = 0
            total_allowance_recuperation = 0
            benefits = 0
            severance_allowance = 0 
            outstanding_annual_leave = 0
            month_13_salary_Pro_ata = 0
            # Get SHUI_10point5percent_employee_pay
            combo = newest_salary + responsibility
            # 1st if
            if combo > 29800000:
                first_value = 29800000 * 0.095
            else: 
                first_value = combo * 0.095
            
            # 2nd if
            if combo > 93600000:
                second_value = 93600000 * 0.01
            else: 
                second_value = combo * 0.01
            SHUI_10point5percent_employee_pay = round(first_value + second_value,0)
            # Get recuperation_of_SHU_Ins_10point5percent_staff_pay
            recuperation_of_SHU_Ins_10point5percent_staff_pay = 0
            # Get SHUI_21point5percent_company_pay
            combo = newest_salary + responsibility
            # 1st if
            if combo > 29800000:
                first_value = 29800000 * 0.205
            else: 
                first_value = combo * 0.205
            
            # 2nd if
            if combo > 93600000:
                second_value = 93600000 * 0.01
            else: 
                second_value = combo * 0.01
            SHUI_21point5percent_company_pay = round(first_value + second_value,0)
            # Get recuperation_of_SHU_Ins_21point5percent_company_pay
            recuperation_of_SHU_Ins_21point5percent_company_pay = 0
            # Get occupational_accident_and_disease
            occupational_accident_and_disease = 0
            # Get trade_union_fee_company_pay_2percent
            if SHUI_10point5percent_employee_pay > 0: 
                if newest_salary > 29800000:
                    SalarytoBH = 29800000
                else:
                    SalarytoBH = newest_salary
            else:
                SalarytoBH = 0
            trade_union_fee_company_pay_2percent = round(SalarytoBH * 2/100)
            # Get trade_union_fee_member
            trade_union_fee_member = 0
            # Get family_deduction
            list_of_dependents = Employee_children.objects.filter(employee=employee)
            number_of_dependents = list_of_dependents.count()
            family_deduction = 11000000 + (number_of_dependents * 4400000)
            # Get taxable_income
            sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
            taxable_income = sum_K_AA - lunch + occupational_accident_and_disease
            # Get taxed_income
            if taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction < 0:
                taxed_income = 0
            else:
                taxed_income = taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction
            # Get PIT
            if 5000000 < taxed_income <= 10000000:
                PIT_before_round = (taxed_income * 0.1) - 250000
            elif 10000000 < taxed_income <= 18000000:
                PIT_before_round = (taxed_income * 0.15) - 750000
            elif 18000000 < taxed_income <= 32000000:
                PIT_before_round = (taxed_income * 0.2) - 1650000
            elif 32000000 < taxed_income <= 52000000:
                PIT_before_round = (taxed_income * 0.25) - 3250000
            elif 52000000 < taxed_income <= 80000000:
                PIT_before_round = (taxed_income * 0.3) - 5850000
            elif taxed_income > 80000000:
                PIT_before_round = (taxed_income * 0.35) - 9850000
            else: 
                PIT_before_round = taxed_income * 0.05
            PIT = round(PIT_before_round)
            # Get deduct
            deduct = 0
            # Get net_income
            sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
            net_income = sum_K_AA + occupational_accident_and_disease - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - PIT - deduct
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
            total_cost = round((sum_K_AA + SHUI_21point5percent_company_pay + recuperation_of_SHU_Ins_21point5percent_company_pay + occupational_accident_and_disease + trade_union_fee_company_pay_2percent + trade_union_fee_member),0)
            

    
            
            payroll_employee_info = Payroll_Tedis(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,
                                                  gross_income=gross_income,salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch, training_fee=training_fee, toxic_allowance=toxic_allowance, travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                  other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata, 
                                                  recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,occupational_accident_and_disease=occupational_accident_and_disease,
                                                  trade_union_fee_company_pay_2percent=trade_union_fee_company_pay_2percent,trade_union_fee_member=trade_union_fee_member,
                                                  family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT=PIT,deduct=deduct,net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
            payroll_employee_info.save()
        messages.success(request, 'SUCCESS: Payroll created')
        return redirect('employee:payroll_tedis',pk=period_month.id)
            
            
        

    # Export payroll
    if request.POST.get('get_payroll'):   
        file_name = str(period_month.month_name) + '_payroll-Tedis.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 640, colour black;' % 'white')
        style_head_small = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 300, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % '67')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        
        '''Sheet Payroll HCM'''
        HCM_sheet_name = str(period_month.month_name) + ' HCM'
        ws_HCM = wb.add_sheet(HCM_sheet_name)

        # Table
        
        # Set col width
        for col in range(0,41):
            ws_HCM.col(col).width = 5000
        

        
        # Top
        ws_HCM.write_merge(0, 0, 0, 6, 'TEDIS REP. OFFICE IN HO CHI MINH', style_head)
        ws_HCM.write(1, 0, 'Room 2B, Floor 2 & 4 - 150 Nguyen Luong Bang, Tan Phu Ward, District 7', style_head_small)
        ws_HCM.write_merge(0, 0, 9, 11, 'PAYROLL IN ' + str(period_month.month_name),style_head)
        
        # Body
        # Set row height
        ws_HCM.row(2).set_style(xlwt.easyxf('font:height 500;'))
        # Body head
        ws_HCM.write(2, 0, 'No.', style_table_head)
        ws_HCM.write(2, 1, 'Employee code', style_table_head)
        ws_HCM.write(2, 2, 'Full name', style_table_head)
        ws_HCM.write(2, 3, 'Joining Date', style_table_head)
        ws_HCM.write(2, 4, 'Department/Area', style_table_head)
        ws_HCM.write(2, 5, 'Job Title', style_table_head)
        ws_HCM.write(2, 6, 'Salary ' + str(period_month.period.period_year) + ' (VND)', style_table_head)
        ws_HCM.write(2, 7, 'Working days', style_table_head)
        ws_HCM.write(2, 8, '% Adjust', style_table_head)
        ws_HCM.write(2, 9, 'Gross Income', style_table_head)
        ws_HCM.write(2, 10, 'Salary recuperation', style_table_head)
        ws_HCM.write(2, 11, 'Overtime', style_table_head)
        ws_HCM.write(2, 12, 'Transportation', style_table_head)
        ws_HCM.write(2, 13, 'Phone', style_table_head)
        ws_HCM.write(2, 14, 'Lunch', style_table_head)
        ws_HCM.write(2, 15, 'Training fee', style_table_head)
        ws_HCM.write(2, 16, 'Toxic Allowance', style_table_head)
        ws_HCM.write(2, 17, 'Travel', style_table_head)
        ws_HCM.write(2, 18, 'Responsibility', style_table_head)
        ws_HCM.write(2, 19, 'Seniority Bonus', style_table_head)
        ws_HCM.write(2, 20, 'Other', style_table_head)
        ws_HCM.write(2, 21, 'Total allowance recuperation', style_table_head)
        ws_HCM.write(2, 22, 'Benefits', style_table_head)
        ws_HCM.write(2, 23, 'Severance Allowance', style_table_head)
        ws_HCM.write(2, 24, 'Outstanding annual leave', style_table_head)
        ws_HCM.write(2, 25, '13th salary (pro-rata)', style_table_head)
        ws_HCM.write(2, 26, 'SHUI(10.5%)(Employee pay)', style_table_head)
        ws_HCM.write(2, 27, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_table_head)
        ws_HCM.write(2, 28, 'SHUI(21.5%)(Company pay)', style_table_head)
        ws_HCM.write(2, 29, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_table_head)
        ws_HCM.write(2, 30, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_table_head)
        ws_HCM.write(2, 31, 'Trade Union fee (Company pay 2%)', style_table_head)
        ws_HCM.write(2, 32, 'Trade Union fee (Employee pay)', style_table_head)
        ws_HCM.write(2, 33, 'Family deduction', style_table_head)
        ws_HCM.write(2, 34, 'Taxable Income', style_table_head)
        ws_HCM.write(2, 35, 'Taxed Income', style_table_head)
        ws_HCM.write(2, 36, 'PIT', style_table_head)
        ws_HCM.write(2, 37, 'Deduct', style_table_head)
        ws_HCM.write(2, 38, 'Net Income', style_table_head)
        ws_HCM.write(2, 39, 'Transfer Bank', style_table_head)
        ws_HCM.write(2, 40, 'Total Cost', style_table_head)
        
        # Body
        # Create total var
        ttnewest_salary = 0
        ttgross_income = 0
        ttsalary_recuperation = 0
        ttovertime = 0
        tttransportation = 0
        ttphone = 0
        ttlunch = 0
        tttraining_fee = 0
        tttoxic_allowance = 0
        tttravel = 0
        ttresponsibility = 0
        ttseniority_bonus = 0
        ttother = 0
        tttotal_allowance_recuperation = 0
        ttbenefits = 0
        ttseverance_allowance = 0
        ttoutstanding_annual_leave = 0
        ttmonth_13_salary_Pro_ata = 0
        ttSHUI_10point5percent_employee_pay = 0
        ttrecuperation_of_SHU_Ins_10point5percent_staff_pay = 0
        ttSHUI_21point5percent_company_pay = 0
        ttrecuperation_of_SHU_Ins_21point5percent_company_pay = 0
        ttoccupational_accident_and_disease = 0
        tttrade_union_fee_company_pay_2percent = 0
        tttrade_union_fee_member = 0
        ttfamily_deduction = 0
        tttaxable_income = 0
        tttaxed_income = 0
        ttPIT = 0
        ttdeduct = 0
        ttnet_income = 0
        tttransfer_bank = 0
        tttotal_cost = 0
        
        for index, data in enumerate(list_payroll_HCM_info):
            # Set row height
            ws_HCM.row(3+index).set_style(xlwt.easyxf('font:height 500;'))
            # Write data
            ws_HCM.write(3+index, 0, str(index+1),style_normal)
            ws_HCM.write(3+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws_HCM.write(3+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws_HCM.write(3+index, 3, str(data['payroll_info'].employee.joining_date.strftime('%d/%m/%Y')),style_normal)
            ws_HCM.write(3+index, 4, str(data['payroll_info'].employee.department_e),style_normal)
            ws_HCM.write(3+index, 5, str(data['payroll_info'].employee.position_e),style_normal)
            ws_HCM.write(3+index, 6, str("{:,}".format(round(data['payroll_info'].newest_salary))),style_normal)
            ws_HCM.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws_HCM.write(3+index, 8, str(round(data['payroll_info'].adjust_percent)) + '%',style_normal)
            ws_HCM.write(3+index, 9, str("{:,}".format(round(data['payroll_info'].gross_income))),style_normal)
            ws_HCM.write(3+index, 10, str("{:,}".format(round(data['payroll_info'].salary_recuperation))),style_normal)
            ws_HCM.write(3+index, 11, str("{:,}".format(round(data['payroll_info'].overtime))),style_normal)
            ws_HCM.write(3+index, 12, str("{:,}".format(round(data['payroll_info'].transportation))),style_normal)
            ws_HCM.write(3+index, 13, str("{:,}".format(round(data['payroll_info'].phone))),style_normal)
            ws_HCM.write(3+index, 14, str("{:,}".format(round(data['payroll_info'].lunch))),style_normal)
            ws_HCM.write(3+index, 15, str("{:,}".format(round(data['payroll_info'].training_fee))),style_normal)
            ws_HCM.write(3+index, 16, str("{:,}".format(round(data['payroll_info'].toxic_allowance))),style_normal)
            ws_HCM.write(3+index, 17, str("{:,}".format(round(data['payroll_info'].travel))),style_normal)
            ws_HCM.write(3+index, 18, str("{:,}".format(round(data['payroll_info'].responsibility))),style_normal)
            ws_HCM.write(3+index, 19, str("{:,}".format(round(data['payroll_info'].seniority_bonus))),style_normal)
            ws_HCM.write(3+index, 20, str("{:,}".format(round(data['payroll_info'].other))),style_normal)
            ws_HCM.write(3+index, 21, str("{:,}".format(round(data['payroll_info'].total_allowance_recuperation))),style_normal)
            ws_HCM.write(3+index, 22, str("{:,}".format(round(data['payroll_info'].benefits))),style_normal)
            ws_HCM.write(3+index, 23, str("{:,}".format(round(data['payroll_info'].severance_allowance))),style_normal)
            ws_HCM.write(3+index, 24, str("{:,}".format(round(data['payroll_info'].outstanding_annual_leave))),style_normal)
            ws_HCM.write(3+index, 25, str("{:,}".format(round(data['payroll_info'].month_13_salary_Pro_ata))),style_normal)
            ws_HCM.write(3+index, 26, str("{:,}".format(round(data['payroll_info'].SHUI_10point5percent_employee_pay))),style_normal)
            ws_HCM.write(3+index, 27, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay))),style_normal)
            ws_HCM.write(3+index, 28, str("{:,}".format(round(data['payroll_info'].SHUI_21point5percent_company_pay))),style_normal)
            ws_HCM.write(3+index, 29, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay))),style_normal)
            ws_HCM.write(3+index, 30, str("{:,}".format(round(data['payroll_info'].occupational_accident_and_disease))),style_normal)
            ws_HCM.write(3+index, 31, str("{:,}".format(round(data['payroll_info'].trade_union_fee_company_pay_2percent))),style_normal)
            ws_HCM.write(3+index, 32, str("{:,}".format(round(data['payroll_info'].trade_union_fee_member))),style_normal)
            ws_HCM.write(3+index, 33, str("{:,}".format(round(data['payroll_info'].family_deduction))),style_normal)
            ws_HCM.write(3+index, 34, str("{:,}".format(round(data['payroll_info'].taxable_income))),style_normal)
            ws_HCM.write(3+index, 35, str("{:,}".format(round(data['payroll_info'].taxed_income))),style_normal)
            ws_HCM.write(3+index, 36, str("{:,}".format(round(data['payroll_info'].PIT))),style_normal)
            ws_HCM.write(3+index, 37, str("{:,}".format(round(data['payroll_info'].deduct))),style_normal)
            ws_HCM.write(3+index, 38, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws_HCM.write(3+index, 39, str("{:,}".format(round(data['payroll_info'].transfer_bank))),style_normal)
            ws_HCM.write(3+index, 40, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 3+index+1
            ttnewest_salary += data['payroll_info'].newest_salary
            ttgross_income += data['payroll_info'].gross_income
            ttsalary_recuperation += data['payroll_info'].salary_recuperation
            ttovertime += data['payroll_info'].overtime
            tttransportation += data['payroll_info'].transportation
            ttphone += data['payroll_info'].phone
            ttlunch += data['payroll_info'].lunch
            tttraining_fee += data['payroll_info'].training_fee
            tttoxic_allowance += data['payroll_info'].toxic_allowance
            tttravel += data['payroll_info'].travel
            ttresponsibility += data['payroll_info'].responsibility
            ttseniority_bonus += data['payroll_info'].seniority_bonus
            ttother += data['payroll_info'].other
            tttotal_allowance_recuperation += data['payroll_info'].total_allowance_recuperation
            ttbenefits += data['payroll_info'].benefits
            ttseverance_allowance += data['payroll_info'].severance_allowance
            ttoutstanding_annual_leave += data['payroll_info'].outstanding_annual_leave
            ttmonth_13_salary_Pro_ata += data['payroll_info'].month_13_salary_Pro_ata
            ttSHUI_10point5percent_employee_pay += data['payroll_info'].SHUI_10point5percent_employee_pay
            ttrecuperation_of_SHU_Ins_10point5percent_staff_pay += data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay
            ttSHUI_21point5percent_company_pay += data['payroll_info'].SHUI_21point5percent_company_pay
            ttrecuperation_of_SHU_Ins_21point5percent_company_pay += data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay
            ttoccupational_accident_and_disease += data['payroll_info'].occupational_accident_and_disease
            tttrade_union_fee_company_pay_2percent += data['payroll_info'].trade_union_fee_company_pay_2percent
            tttrade_union_fee_member += data['payroll_info'].trade_union_fee_member
            ttfamily_deduction += data['payroll_info'].family_deduction
            tttaxable_income += data['payroll_info'].taxable_income
            tttaxed_income += data['payroll_info'].taxed_income
            ttPIT += data['payroll_info'].PIT
            ttdeduct += data['payroll_info'].deduct
            ttnet_income += data['payroll_info'].net_income
            tttransfer_bank += data['payroll_info'].transfer_bank
            tttotal_cost += data['payroll_info'].total_cost
        # Total line in bottom of table 
        ws_HCM.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_table_head)
        ws_HCM.write(last_row, 6, str("{:,}".format(round(ttnewest_salary))),style_table_head)
        ws_HCM.write(last_row, 7, '-',style_table_head)
        ws_HCM.write(last_row, 8, '-',style_table_head)
        ws_HCM.write(last_row, 9, str("{:,}".format(round(ttgross_income))),style_table_head)
        ws_HCM.write(last_row, 10, str("{:,}".format(round(ttsalary_recuperation))),style_table_head)
        ws_HCM.write(last_row, 11, str("{:,}".format(round(ttovertime))),style_table_head)
        ws_HCM.write(last_row, 12, str("{:,}".format(round(tttransportation))),style_table_head)
        ws_HCM.write(last_row, 13, str("{:,}".format(round(ttphone))),style_table_head)
        ws_HCM.write(last_row, 14, str("{:,}".format(round(ttlunch))),style_table_head)
        ws_HCM.write(last_row, 15, str("{:,}".format(round(tttraining_fee))),style_table_head)
        ws_HCM.write(last_row, 16, str("{:,}".format(round(tttoxic_allowance))),style_table_head)
        ws_HCM.write(last_row, 17, str("{:,}".format(round(tttravel))),style_table_head)
        ws_HCM.write(last_row, 18, str("{:,}".format(round(ttresponsibility))),style_table_head)
        ws_HCM.write(last_row, 19, str("{:,}".format(round(ttseniority_bonus))),style_table_head)
        ws_HCM.write(last_row, 20, str("{:,}".format(round(ttother))),style_table_head)
        ws_HCM.write(last_row, 21, str("{:,}".format(round(tttotal_allowance_recuperation))),style_table_head)
        ws_HCM.write(last_row, 22, str("{:,}".format(round(ttbenefits))),style_table_head)
        ws_HCM.write(last_row, 23, str("{:,}".format(round(ttseverance_allowance))),style_table_head)
        ws_HCM.write(last_row, 24, str("{:,}".format(round(ttoutstanding_annual_leave))),style_table_head)
        ws_HCM.write(last_row, 25, str("{:,}".format(round(ttmonth_13_salary_Pro_ata))),style_table_head)
        ws_HCM.write(last_row, 26, str("{:,}".format(round(ttSHUI_10point5percent_employee_pay))),style_table_head)
        ws_HCM.write(last_row, 27, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay))),style_table_head)
        ws_HCM.write(last_row, 28, str("{:,}".format(round(ttSHUI_21point5percent_company_pay))),style_table_head)
        ws_HCM.write(last_row, 29, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_21point5percent_company_pay))),style_table_head)
        ws_HCM.write(last_row, 30, str("{:,}".format(round(ttoccupational_accident_and_disease))),style_table_head)
        ws_HCM.write(last_row, 31, str("{:,}".format(round(tttrade_union_fee_company_pay_2percent))),style_table_head)
        ws_HCM.write(last_row, 32, str("{:,}".format(round(tttrade_union_fee_member))),style_table_head)
        ws_HCM.write(last_row, 33, str("{:,}".format(round(ttfamily_deduction))),style_table_head)
        ws_HCM.write(last_row, 34, str("{:,}".format(round(tttaxable_income))),style_table_head)
        ws_HCM.write(last_row, 35, str("{:,}".format(round(tttaxed_income))),style_table_head)
        ws_HCM.write(last_row, 36, str("{:,}".format(round(ttPIT))),style_table_head)
        ws_HCM.write(last_row, 37, str("{:,}".format(round(ttdeduct))),style_table_head)
        ws_HCM.write(last_row, 38, str("{:,}".format(round(ttnet_income))),style_table_head)
        ws_HCM.write(last_row, 39, str("{:,}".format(round(tttransfer_bank))),style_table_head)
        ws_HCM.write(last_row, 40, str("{:,}".format(round(tttotal_cost))),style_table_head)
        
        
        '''Sheet Payroll HANOI'''
        HANOI_sheet_name = str(period_month.month_name) + ' HAN'
        ws_HAN = wb.add_sheet(HANOI_sheet_name)

        # Table
        
        # Set col width
        for col in range(0,41):
            ws_HAN.col(col).width = 5000
        

        
        # Top
        ws_HAN.write_merge(0, 0, 0, 6, 'TEDIS REP. OFFICE IN HANOI', style_head)
        ws_HAN.write(1, 0, 'Giang Vo Lake View Building, Unit 202, D10 Giang Vo St. Ba Dinh District', style_head_small)
        ws_HAN.write_merge(0, 0, 9, 11, 'PAYROLL IN ' + str(period_month.month_name),style_head)
        
        # Body
        # Set row height
        ws_HAN.row(2).set_style(xlwt.easyxf('font:height 500;'))
        # Body head
        ws_HAN.write(2, 0, 'No.', style_table_head)
        ws_HAN.write(2, 1, 'Employee code', style_table_head)
        ws_HAN.write(2, 2, 'Full name', style_table_head)
        ws_HAN.write(2, 3, 'Joining Date', style_table_head)
        ws_HAN.write(2, 4, 'Department/Area', style_table_head)
        ws_HAN.write(2, 5, 'Job Title', style_table_head)
        ws_HAN.write(2, 6, 'Salary ' + str(period_month.period.period_year) + ' (VND)', style_table_head)
        ws_HAN.write(2, 7, 'Working days', style_table_head)
        ws_HAN.write(2, 8, '% Adjust', style_table_head)
        ws_HAN.write(2, 9, 'Gross Income', style_table_head)
        ws_HAN.write(2, 10, 'Salary recuperation', style_table_head)
        ws_HAN.write(2, 11, 'Overtime', style_table_head)
        ws_HAN.write(2, 12, 'Transportation', style_table_head)
        ws_HAN.write(2, 13, 'Phone', style_table_head)
        ws_HAN.write(2, 14, 'Lunch', style_table_head)
        ws_HAN.write(2, 15, 'Training fee', style_table_head)
        ws_HAN.write(2, 16, 'Toxic Allowance', style_table_head)
        ws_HAN.write(2, 17, 'Travel', style_table_head)
        ws_HAN.write(2, 18, 'Responsibility', style_table_head)
        ws_HAN.write(2, 19, 'Seniority Bonus', style_table_head)
        ws_HAN.write(2, 20, 'Other', style_table_head)
        ws_HAN.write(2, 21, 'Total allowance recuperation', style_table_head)
        ws_HAN.write(2, 22, 'Benefits', style_table_head)
        ws_HAN.write(2, 23, 'Severance Allowance', style_table_head)
        ws_HAN.write(2, 24, 'Outstanding annual leave', style_table_head)
        ws_HAN.write(2, 25, '13th salary (pro-rata)', style_table_head)
        ws_HAN.write(2, 26, 'SHUI(10.5%)(Employee pay)', style_table_head)
        ws_HAN.write(2, 27, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_table_head)
        ws_HAN.write(2, 28, 'SHUI(21.5%)(Company pay)', style_table_head)
        ws_HAN.write(2, 29, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_table_head)
        ws_HAN.write(2, 30, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_table_head)
        ws_HAN.write(2, 31, 'Trade Union fee (Company pay 2%)', style_table_head)
        ws_HAN.write(2, 32, 'Trade Union fee (Employee pay)', style_table_head)
        ws_HAN.write(2, 33, 'Family deduction', style_table_head)
        ws_HAN.write(2, 34, 'Taxable Income', style_table_head)
        ws_HAN.write(2, 35, 'Taxed Income', style_table_head)
        ws_HAN.write(2, 36, 'PIT', style_table_head)
        ws_HAN.write(2, 37, 'Deduct', style_table_head)
        ws_HAN.write(2, 38, 'Net Income', style_table_head)
        ws_HAN.write(2, 39, 'Transfer Bank', style_table_head)
        ws_HAN.write(2, 40, 'Total Cost', style_table_head)
        
        # Body
        # Create total var
        ttnewest_salary = 0
        ttgross_income = 0
        ttsalary_recuperation = 0
        ttovertime = 0
        tttransportation = 0
        ttphone = 0
        ttlunch = 0
        tttraining_fee = 0
        tttoxic_allowance = 0
        tttravel = 0
        ttresponsibility = 0
        ttseniority_bonus = 0
        ttother = 0
        tttotal_allowance_recuperation = 0
        ttbenefits = 0
        ttseverance_allowance = 0
        ttoutstanding_annual_leave = 0
        ttmonth_13_salary_Pro_ata = 0
        ttSHUI_10point5percent_employee_pay = 0
        ttrecuperation_of_SHU_Ins_10point5percent_staff_pay = 0
        ttSHUI_21point5percent_company_pay = 0
        ttrecuperation_of_SHU_Ins_21point5percent_company_pay = 0
        ttoccupational_accident_and_disease = 0
        tttrade_union_fee_company_pay_2percent = 0
        tttrade_union_fee_member = 0
        ttfamily_deduction = 0
        tttaxable_income = 0
        tttaxed_income = 0
        ttPIT = 0
        ttdeduct = 0
        ttnet_income = 0
        tttransfer_bank = 0
        tttotal_cost = 0
        
        for index, data in enumerate(list_payroll_HANOI_info):
            # Set row height
            ws_HAN.row(3+index).set_style(xlwt.easyxf('font:height 500;'))
            # Write data
            ws_HAN.write(3+index, 0, str(index+1),style_normal)
            ws_HAN.write(3+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws_HAN.write(3+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws_HAN.write(3+index, 3, str(data['payroll_info'].employee.joining_date.strftime('%d/%m/%Y')),style_normal)
            ws_HAN.write(3+index, 4, str(data['payroll_info'].employee.department_e),style_normal)
            ws_HAN.write(3+index, 5, str(data['payroll_info'].employee.position_e),style_normal)
            ws_HAN.write(3+index, 6, str("{:,}".format(round(data['payroll_info'].newest_salary))),style_normal)
            ws_HAN.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws_HAN.write(3+index, 8, str(round(data['payroll_info'].adjust_percent)) + '%',style_normal)
            ws_HAN.write(3+index, 9, str("{:,}".format(round(data['payroll_info'].gross_income))),style_normal)
            ws_HAN.write(3+index, 10, str("{:,}".format(round(data['payroll_info'].salary_recuperation))),style_normal)
            ws_HAN.write(3+index, 11, str("{:,}".format(round(data['payroll_info'].overtime))),style_normal)
            ws_HAN.write(3+index, 12, str("{:,}".format(round(data['payroll_info'].transportation))),style_normal)
            ws_HAN.write(3+index, 13, str("{:,}".format(round(data['payroll_info'].phone))),style_normal)
            ws_HAN.write(3+index, 14, str("{:,}".format(round(data['payroll_info'].lunch))),style_normal)
            ws_HAN.write(3+index, 15, str("{:,}".format(round(data['payroll_info'].training_fee))),style_normal)
            ws_HAN.write(3+index, 16, str("{:,}".format(round(data['payroll_info'].toxic_allowance))),style_normal)
            ws_HAN.write(3+index, 17, str("{:,}".format(round(data['payroll_info'].travel))),style_normal)
            ws_HAN.write(3+index, 18, str("{:,}".format(round(data['payroll_info'].responsibility))),style_normal)
            ws_HAN.write(3+index, 19, str("{:,}".format(round(data['payroll_info'].seniority_bonus))),style_normal)
            ws_HAN.write(3+index, 20, str("{:,}".format(round(data['payroll_info'].other))),style_normal)
            ws_HAN.write(3+index, 21, str("{:,}".format(round(data['payroll_info'].total_allowance_recuperation))),style_normal)
            ws_HAN.write(3+index, 22, str("{:,}".format(round(data['payroll_info'].benefits))),style_normal)
            ws_HAN.write(3+index, 23, str("{:,}".format(round(data['payroll_info'].severance_allowance))),style_normal)
            ws_HAN.write(3+index, 24, str("{:,}".format(round(data['payroll_info'].outstanding_annual_leave))),style_normal)
            ws_HAN.write(3+index, 25, str("{:,}".format(round(data['payroll_info'].month_13_salary_Pro_ata))),style_normal)
            ws_HAN.write(3+index, 26, str("{:,}".format(round(data['payroll_info'].SHUI_10point5percent_employee_pay))),style_normal)
            ws_HAN.write(3+index, 27, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay))),style_normal)
            ws_HAN.write(3+index, 28, str("{:,}".format(round(data['payroll_info'].SHUI_21point5percent_company_pay))),style_normal)
            ws_HAN.write(3+index, 29, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay))),style_normal)
            ws_HAN.write(3+index, 30, str("{:,}".format(round(data['payroll_info'].occupational_accident_and_disease))),style_normal)
            ws_HAN.write(3+index, 31, str("{:,}".format(round(data['payroll_info'].trade_union_fee_company_pay_2percent))),style_normal)
            ws_HAN.write(3+index, 32, str("{:,}".format(round(data['payroll_info'].trade_union_fee_member))),style_normal)
            ws_HAN.write(3+index, 33, str("{:,}".format(round(data['payroll_info'].family_deduction))),style_normal)
            ws_HAN.write(3+index, 34, str("{:,}".format(round(data['payroll_info'].taxable_income))),style_normal)
            ws_HAN.write(3+index, 35, str("{:,}".format(round(data['payroll_info'].taxed_income))),style_normal)
            ws_HAN.write(3+index, 36, str("{:,}".format(round(data['payroll_info'].PIT))),style_normal)
            ws_HAN.write(3+index, 37, str("{:,}".format(round(data['payroll_info'].deduct))),style_normal)
            ws_HAN.write(3+index, 38, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws_HAN.write(3+index, 39, str("{:,}".format(round(data['payroll_info'].transfer_bank))),style_normal)
            ws_HAN.write(3+index, 40, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 3+index+1
            ttnewest_salary += data['payroll_info'].newest_salary
            ttgross_income += data['payroll_info'].gross_income
            ttsalary_recuperation += data['payroll_info'].salary_recuperation
            ttovertime += data['payroll_info'].overtime
            tttransportation += data['payroll_info'].transportation
            ttphone += data['payroll_info'].phone
            ttlunch += data['payroll_info'].lunch
            tttraining_fee += data['payroll_info'].training_fee
            tttoxic_allowance += data['payroll_info'].toxic_allowance
            tttravel += data['payroll_info'].travel
            ttresponsibility += data['payroll_info'].responsibility
            ttseniority_bonus += data['payroll_info'].seniority_bonus
            ttother += data['payroll_info'].other
            tttotal_allowance_recuperation += data['payroll_info'].total_allowance_recuperation
            ttbenefits += data['payroll_info'].benefits
            ttseverance_allowance += data['payroll_info'].severance_allowance
            ttoutstanding_annual_leave += data['payroll_info'].outstanding_annual_leave
            ttmonth_13_salary_Pro_ata += data['payroll_info'].month_13_salary_Pro_ata
            ttSHUI_10point5percent_employee_pay += data['payroll_info'].SHUI_10point5percent_employee_pay
            ttrecuperation_of_SHU_Ins_10point5percent_staff_pay += data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay
            ttSHUI_21point5percent_company_pay += data['payroll_info'].SHUI_21point5percent_company_pay
            ttrecuperation_of_SHU_Ins_21point5percent_company_pay += data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay
            ttoccupational_accident_and_disease += data['payroll_info'].occupational_accident_and_disease
            tttrade_union_fee_company_pay_2percent += data['payroll_info'].trade_union_fee_company_pay_2percent
            tttrade_union_fee_member += data['payroll_info'].trade_union_fee_member
            ttfamily_deduction += data['payroll_info'].family_deduction
            tttaxable_income += data['payroll_info'].taxable_income
            tttaxed_income += data['payroll_info'].taxed_income
            ttPIT += data['payroll_info'].PIT
            ttdeduct += data['payroll_info'].deduct
            ttnet_income += data['payroll_info'].net_income
            tttransfer_bank += data['payroll_info'].transfer_bank
            tttotal_cost += data['payroll_info'].total_cost
        # Total line in bottom of table 
        ws_HAN.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_table_head)
        ws_HAN.write(last_row, 6, str("{:,}".format(round(ttnewest_salary))),style_table_head)
        ws_HAN.write(last_row, 7, '-',style_table_head)
        ws_HAN.write(last_row, 8, '-',style_table_head)
        ws_HAN.write(last_row, 9, str("{:,}".format(round(ttgross_income))),style_table_head)
        ws_HAN.write(last_row, 10, str("{:,}".format(round(ttsalary_recuperation))),style_table_head)
        ws_HAN.write(last_row, 11, str("{:,}".format(round(ttovertime))),style_table_head)
        ws_HAN.write(last_row, 12, str("{:,}".format(round(tttransportation))),style_table_head)
        ws_HAN.write(last_row, 13, str("{:,}".format(round(ttphone))),style_table_head)
        ws_HAN.write(last_row, 14, str("{:,}".format(round(ttlunch))),style_table_head)
        ws_HAN.write(last_row, 15, str("{:,}".format(round(tttraining_fee))),style_table_head)
        ws_HAN.write(last_row, 16, str("{:,}".format(round(tttoxic_allowance))),style_table_head)
        ws_HAN.write(last_row, 17, str("{:,}".format(round(tttravel))),style_table_head)
        ws_HAN.write(last_row, 18, str("{:,}".format(round(ttresponsibility))),style_table_head)
        ws_HAN.write(last_row, 19, str("{:,}".format(round(ttseniority_bonus))),style_table_head)
        ws_HAN.write(last_row, 20, str("{:,}".format(round(ttother))),style_table_head)
        ws_HAN.write(last_row, 21, str("{:,}".format(round(tttotal_allowance_recuperation))),style_table_head)
        ws_HAN.write(last_row, 22, str("{:,}".format(round(ttbenefits))),style_table_head)
        ws_HAN.write(last_row, 23, str("{:,}".format(round(ttseverance_allowance))),style_table_head)
        ws_HAN.write(last_row, 24, str("{:,}".format(round(ttoutstanding_annual_leave))),style_table_head)
        ws_HAN.write(last_row, 25, str("{:,}".format(round(ttmonth_13_salary_Pro_ata))),style_table_head)
        ws_HAN.write(last_row, 26, str("{:,}".format(round(ttSHUI_10point5percent_employee_pay))),style_table_head)
        ws_HAN.write(last_row, 27, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay))),style_table_head)
        ws_HAN.write(last_row, 28, str("{:,}".format(round(ttSHUI_21point5percent_company_pay))),style_table_head)
        ws_HAN.write(last_row, 29, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_21point5percent_company_pay))),style_table_head)
        ws_HAN.write(last_row, 30, str("{:,}".format(round(ttoccupational_accident_and_disease))),style_table_head)
        ws_HAN.write(last_row, 31, str("{:,}".format(round(tttrade_union_fee_company_pay_2percent))),style_table_head)
        ws_HAN.write(last_row, 32, str("{:,}".format(round(tttrade_union_fee_member))),style_table_head)
        ws_HAN.write(last_row, 33, str("{:,}".format(round(ttfamily_deduction))),style_table_head)
        ws_HAN.write(last_row, 34, str("{:,}".format(round(tttaxable_income))),style_table_head)
        ws_HAN.write(last_row, 35, str("{:,}".format(round(tttaxed_income))),style_table_head)
        ws_HAN.write(last_row, 36, str("{:,}".format(round(ttPIT))),style_table_head)
        ws_HAN.write(last_row, 37, str("{:,}".format(round(ttdeduct))),style_table_head)
        ws_HAN.write(last_row, 38, str("{:,}".format(round(ttnet_income))),style_table_head)
        ws_HAN.write(last_row, 39, str("{:,}".format(round(tttransfer_bank))),style_table_head)
        ws_HAN.write(last_row, 40, str("{:,}".format(round(tttotal_cost))),style_table_head)
         


        wb.save(response)
        return response

    
    return render(request, 'employee/view_payroll_tedis.html', {
        'period_month' : period_month,
        'payrollExist': payrollExist,
        'list_payroll_HCM_info' : list_payroll_HCM_info,
        'list_payroll_HANOI_info' : list_payroll_HANOI_info,
        'total_working_day' : total_working_day,
    })


def payroll_tedis_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    payroll_info = Payroll_Tedis.objects.get(pk=pk)
    
    # Get month total working days
    list_work_days = Daily_work.objects.filter(month=payroll_info.month,weekend=False,holiday=False)
    month_total_working_days = list_work_days.count()
    
    # Update payroll info
    if request.POST.get('btnupdatepayroll'):
        '''HCM'''
        area_HCM = Area.objects.get(area='HCMC')
        if payroll_info.employee.area == area_HCM:
            # Get month,employee,newest_salary,working_days,adjust_percent
            month = payroll_info.month
            employee = payroll_info.employee
            newest_salary = payroll_info.newest_salary
            working_days = payroll_info.working_days
            adjust_percent = payroll_info.adjust_percent
            # Get gross_income
            gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(month_total_working_days) )
            # Get salary_recuperation
            salary_recuperation = request.POST.get('salary_recuperation')
            # Get overtime
            overtime = payroll_info.overtime
            # Get transportation,phone,lunch
            transportation = payroll_info.transportation
            phone = payroll_info.phone
            lunch = payroll_info.lunch
            # Get training_fee
            training_fee = request.POST.get('training_fee')
            # Get toxic_allowance
            toxic_allowance = request.POST.get('toxic_allowance')
            # Get travel,responsibility,seniority_bonus
            travel = payroll_info.travel
            responsibility = payroll_info.responsibility
            seniority_bonus = payroll_info.seniority_bonus
            # Get other,total_allowance_recuperation,benefits,severance_allowance,outstanding_annual_leave,month_13_salary_Pro_ata
            other = request.POST.get('other')
            total_allowance_recuperation = request.POST.get('total_allowance_recuperation')
            benefits = request.POST.get('benefits')
            severance_allowance = request.POST.get('severance_allowance')
            outstanding_annual_leave = request.POST.get('outstanding_annual_leave')
            month_13_salary_Pro_ata = request.POST.get('month_13_salary_Pro_ata')
            # Get SHUI_10point5percent_employee_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.095
                    else: 
                        first_value = combo * 0.095
                    
                    # 2nd if
                    if combo > 93600000:
                        second_value = 93600000 * 0.01
                    else: 
                        second_value = combo * 0.01
                    SHUI_10point5percent_employee_pay = round(first_value + second_value)
                else: 
                    SHUI_10point5percent_employee_pay = 0
            else:
                SHUI_10point5percent_employee_pay = 0
            # Get recuperation_of_SHU_Ins_10point5percent_staff_pay
            recuperation_of_SHU_Ins_10point5percent_staff_pay = request.POST.get('recuperation_of_SHU_Ins_10point5percent_staff_pay')
            # Get SHUI_21point5percent_company_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.205
                    else: 
                        first_value = combo * 0.205
                    
                    # 2nd if
                    if combo > 93600000:
                        second_value = 93600000 * 0.01
                    else: 
                        second_value = combo * 0.01
                    SHUI_21point5percent_company_pay = round(first_value + second_value)
                else: 
                    SHUI_21point5percent_company_pay = 0
            else:
                SHUI_21point5percent_company_pay = 0
            # Get recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease
            recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
            occupational_accident_and_disease = request.POST.get('occupational_accident_and_disease')
            # Get trade_union_fee_company_pay_2percent
            combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
            if SHUI_10point5percent_employee_pay > 0: 
                if combo > 29800000:
                    SalarytoBH = 29800000
                else:
                    SalarytoBH = combo
            else:
                SalarytoBH = 0
            trade_union_fee_company_pay_2percent = round(SalarytoBH * 2/100)
            # Get trade_union_fee_member
            if trade_union_fee_company_pay_2percent > 0:
                trade_union_fee_member = 4680000 * 1/100
            else:
                trade_union_fee_member = 0
            # Get family_deduction
            family_deduction = payroll_info.family_deduction
            # Get taxable_income
            contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus :
                    sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
                    taxable_income = sum_K_AA - float(lunch) - float(severance_allowance) + float(occupational_accident_and_disease)
                else:
                    taxable_income = sum_K_AA - float(severance_allowance) + float(occupational_accident_and_disease)
            else:
                taxable_income = 0
            # Get taxed_income
            if taxable_income - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction) < 0:
                taxed_income = 0
            else:
                taxed_income = float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction)
            # Get PIT
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus :
                    if 5000000 < taxed_income <= 10000000:
                        PIT_before_round = (taxed_income * 0.1) - 250000
                    elif 10000000 < taxed_income <= 18000000:
                        PIT_before_round = (taxed_income * 0.15) - 750000
                    elif 18000000 < taxed_income <= 32000000:
                        PIT_before_round = (taxed_income * 0.2) - 1650000
                    elif 32000000 < taxed_income <= 52000000:
                    
                        PIT_before_round = (taxed_income * 0.25) - 3250000
                    elif 52000000 < taxed_income <= 80000000:
                        PIT_before_round = (taxed_income * 0.3) - 5850000
                    elif taxed_income > 80000000:
                        PIT_before_round = (taxed_income * 0.35) - 9850000
                    else: 
                        PIT_before_round = taxed_income * 0.05
                elif taxed_income >= 2000000:
                    PIT_before_round = taxed_income * 10/100
                else:
                    PIT_before_round = 0                     
            else:
                PIT_before_round = 0
            PIT = round(PIT_before_round)
            # Get deduct
            deduct = request.POST.get('deduct')
            # Get net_income
            sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
            net_income = sum_K_AA + float(occupational_accident_and_disease) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(PIT) - float(deduct)
            # Get transfer_bank
            transfer_bank = request.POST.get('transfer_bank')
            # Get total_cost
            sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
            total_cost = round((sum_K_AA + float(SHUI_21point5percent_company_pay) + float(recuperation_of_SHU_Ins_21point5percent_company_pay) + float(occupational_accident_and_disease) + float(trade_union_fee_company_pay_2percent) + float(trade_union_fee_member) + float(transfer_bank) - float(deduct)),0)
            # Update and save
            payroll_update_info = Payroll_Tedis(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                                salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,training_fee=training_fee,toxic_allowance=toxic_allowance,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                                SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                                occupational_accident_and_disease=occupational_accident_and_disease,
                                                trade_union_fee_company_pay_2percent=trade_union_fee_company_pay_2percent,trade_union_fee_member=trade_union_fee_member,
                                                family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT=PIT,deduct=deduct,net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
            payroll_update_info.save()
            messages.success(request, 'SUCCESS: Payroll updated')
            return redirect('employee:payroll_tedis_edit',pk=payroll_info.id)
        
        '''HANOI'''
        area_HANOI = Area.objects.get(area='HANOI')
        if payroll_info.employee.area == area_HANOI:
            # Get month,employee,newest_salary,working_days,adjust_percent
            month = payroll_info.month
            employee = payroll_info.employee
            newest_salary = payroll_info.newest_salary
            working_days = payroll_info.working_days
            adjust_percent = payroll_info.adjust_percent
            # Get gross_income
            gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(month_total_working_days) )
            # Get salary_recuperation
            salary_recuperation = request.POST.get('salary_recuperation')
            # Get overtime
            overtime = payroll_info.overtime
            # Get transportation,phone,lunch
            transportation = payroll_info.transportation
            phone = payroll_info.phone
            lunch = payroll_info.lunch
            # Get training_fee
            training_fee = request.POST.get('training_fee')
            # Get toxic_allowance
            toxic_allowance = request.POST.get('toxic_allowance')
            # Get travel,responsibility,seniority_bonus
            travel = payroll_info.travel
            responsibility = payroll_info.responsibility
            seniority_bonus = payroll_info.seniority_bonus
            # Get other,total_allowance_recuperation,benefits,severance_allowance,outstanding_annual_leave,month_13_salary_Pro_ata
            other = request.POST.get('other')
            total_allowance_recuperation = request.POST.get('total_allowance_recuperation')
            benefits = request.POST.get('benefits')
            severance_allowance = request.POST.get('severance_allowance')
            outstanding_annual_leave = request.POST.get('outstanding_annual_leave')
            month_13_salary_Pro_ata = request.POST.get('month_13_salary_Pro_ata')
            # Get SHUI_10point5percent_employee_pay
            combo = newest_salary + responsibility
            # 1st if
            if combo > 29800000:
                first_value = 29800000 * 0.095
            else: 
                first_value = combo * 0.095
            
            # 2nd if
            if combo > 93600000:
                second_value = 93600000 * 0.01
            else: 
                second_value = combo * 0.01
            SHUI_10point5percent_employee_pay = round(first_value + second_value,0)
            # Get recuperation_of_SHU_Ins_10point5percent_staff_pay
            recuperation_of_SHU_Ins_10point5percent_staff_pay = request.POST.get('recuperation_of_SHU_Ins_10point5percent_staff_pay')
            # Get SHUI_21point5percent_company_pay
            combo = newest_salary + responsibility
            # 1st if
            if combo > 29800000:
                first_value = 29800000 * 0.205
            else: 
                first_value = combo * 0.205
            
            # 2nd if
            if combo > 93600000:
                second_value = 93600000 * 0.01
            else: 
                second_value = combo * 0.01
            SHUI_21point5percent_company_pay = round(first_value + second_value,0)
            # Get recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease
            recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
            occupational_accident_and_disease = request.POST.get('occupational_accident_and_disease')
            if SHUI_10point5percent_employee_pay > 0: 
                if newest_salary > 29800000:
                    SalarytoBH = 29800000
                else:
                    SalarytoBH = newest_salary
            else:
                SalarytoBH = 0
            trade_union_fee_company_pay_2percent = round(SalarytoBH * 2/100)
            # Get trade_union_fee_member
            trade_union_fee_member = payroll_info.trade_union_fee_member
            # Get family_deduction
            family_deduction = payroll_info.family_deduction
            # Get taxable_income
            sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
            taxable_income = sum_K_AA - float(lunch) + float(occupational_accident_and_disease)
            # Get taxed_income
            if float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction) < 0:
                taxed_income = 0
            else:
                taxed_income = float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction)
            # Get PIT
            if 5000000 < taxed_income <= 10000000:
                PIT_before_round = (taxed_income * 0.1) - 250000
            elif 10000000 < taxed_income <= 18000000:
                PIT_before_round = (taxed_income * 0.15) - 750000
            elif 18000000 < taxed_income <= 32000000:
                PIT_before_round = (taxed_income * 0.2) - 1650000
            elif 32000000 < taxed_income <= 52000000:
                PIT_before_round = (taxed_income * 0.25) - 3250000
            elif 52000000 < taxed_income <= 80000000:
                PIT_before_round = (taxed_income * 0.3) - 5850000
            elif taxed_income > 80000000:
                PIT_before_round = (taxed_income * 0.35) - 9850000
            else: 
                PIT_before_round = taxed_income * 0.05
            PIT = round(PIT_before_round)
            # Get deduct
            deduct = request.POST.get('deduct')
            # Get net_income
            sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
            net_income = sum_K_AA + float(occupational_accident_and_disease) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(PIT) - float(deduct)
            # Get transfer_bank
            transfer_bank = request.POST.get('transfer_bank')
            # Get total_cost
            sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
            total_cost = round((sum_K_AA + float(SHUI_21point5percent_company_pay) + float(recuperation_of_SHU_Ins_21point5percent_company_pay) + float(occupational_accident_and_disease) + float(trade_union_fee_company_pay_2percent) + float(trade_union_fee_member)),0)
            # Update and save
            payroll_update_info = Payroll_Tedis(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                                salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,training_fee=training_fee,toxic_allowance=toxic_allowance,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                                SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                                occupational_accident_and_disease=occupational_accident_and_disease,
                                                trade_union_fee_company_pay_2percent=trade_union_fee_company_pay_2percent,trade_union_fee_member=trade_union_fee_member,
                                                family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT=PIT,deduct=deduct,net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
            payroll_update_info.save()
            messages.success(request, 'SUCCESS: Payroll updated')
            return redirect('employee:payroll_tedis_edit',pk=payroll_info.id)
        
        
        
    
    return render(request, 'employee/payroll_tedis_edit.html', {
        'payroll_info' : payroll_info,
        'month_total_working_days' : month_total_working_days,
        
    })


def payroll_tedis_vietha(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    

    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    
    
    # Get payroll data
    site_JV = Site.objects.get(site='JV')
    list_employee_tedis_vietha_active = Employee.objects.filter(site=site_JV,active=1)
    list_employee_tedis_vietha = Employee.objects.filter(site=site_JV)
    # # Get total_working_days
    # list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    # daily_work_info = Daily_work_for_employee.objects.filter(employee=list_employee_tedis_vietha[0], daily_work__in=list_work_days)
    # total_working_day = daily_work_info.count()
    # Create payroll dict
    list_payroll_info = []
    for employee in list_employee_tedis_vietha:
        try:
            payroll_info = Payroll_Tedis_Vietha.objects.get(employee=employee,month=period_month)
            payrollExist = 1
            # Make data
            # Get Working day of BO and Working day of WH
            # warehouse_department_e = Department_E.objects.get(department_e='Warehouse')
            # if employee.department_e == warehouse_department_e:
            #     list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0)
            #     working_day_wh = 0
            #     for daily_work_info in list_daily_work_info:
            #         working_day_wh += daily_work_info.work
            # else:
            #     list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0)
            #     working_day_bo = 0
            #     for daily_work_info in list_daily_work_info:
            #         working_day_bo += daily_work_info.work
            working_day_bo = period_month.total_work_days_bo
            working_day_wh = period_month.total_work_days_wh
            # Get payroll info 
            data = {
                'payroll_info': payroll_info,        
            }
            list_payroll_info.append(data)
        except Payroll_Tedis_Vietha.DoesNotExist:
            payrollExist = 0
            working_day_wh = ''
            working_day_bo = ''
        
    # Create payroll data
    if request.POST.get('btn_adjust_percent'):
        # Get % Adjust  
        adjust_percent = float(request.POST.get('adjust_percent'))
        for employee in list_employee_tedis_vietha_active:
            # Get Salary info
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
            if list_contracts.count() == 0:
                newest_salary = 0
            else:
                newest_salary = list_contracts[0].basic_salary
            # Get working days
            '''Get Working day of BO and Working day of WH'''
            list_daily_work_this_month = Daily_work.objects.filter(month=period_month)
            warehouse_department_e = Department_E.objects.get(department_e='Warehouse')
            if employee.department_e == warehouse_department_e:
                list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0, daily_work__in=list_daily_work_this_month)
                total_working_day = 0
                for daily_work_info in list_daily_work_info:
                    total_working_day += daily_work_info.work
            else:
                list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0, daily_work__in=list_daily_work_this_month)
                total_working_day = 0
                for daily_work_info in list_daily_work_info:
                    total_working_day += daily_work_info.work
            
            unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,work__gt=0, unpaid_leave__gt=0, daily_work__in=list_daily_work_this_month)
            working_days = total_working_day - unpaid_leave_info.count()
            # Get gross income
            gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(total_working_day) )
            # Get transportation, phone, lunch, travel, responsibility, seniority_bonus
            if list_contracts.count() == 0:
                transportation = 0
                phone = 0
                lunch = 0
                travel = 0
                responsibility = 0
                seniority_bonus = 0
            else:
                transportation = round(list_contracts[0].transportation_support * working_days / total_working_day)
                phone = round(list_contracts[0].telephone_support * working_days / total_working_day)
                lunch = round(list_contracts[0].lunch_support * working_days / total_working_day)
                travel = round(list_contracts[0].travel_support * working_days / total_working_day)
                responsibility = round(list_contracts[0].responsibility_allowance * working_days / total_working_day)
                seniority_bonus = round(list_contracts[0].seniority_bonus * working_days / total_working_day)
            # Get other, outstanding_annual_leave, OTC_incentive, KPI_achievement, month_13_salary_Pro_ata, incentive_last_month, incentive_last_quy_last_year, taxable_overtime, nontaxable_overtime
            other = 0
            outstanding_annual_leave = 0
            OTC_incentive = 0
            KPI_achievement = 0
            month_13_salary_Pro_ata = 0
            incentive_last_month = 0
            incentive_last_quy_last_year = 0
            taxable_overtime = 0
            nontaxable_overtime = 0
            # Get SHUI_10point5percent_employee_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT and working_days >= 10:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.095
                    else:
                        first_value = combo * 0.095
                    # 2nd if
                    if combo > 83200000:
                        second_value = 83200000 * 0.01
                    else:
                        second_value = combo * 0.01
                    SHUI_10point5percent_employee_pay = round(first_value + second_value)
                else: 
                        SHUI_10point5percent_employee_pay = 0
            else:
                SHUI_10point5percent_employee_pay = 0
            # Get recuperation_of_SHU_Ins_10point5percent_staff_pay
            recuperation_of_SHU_Ins_10point5percent_staff_pay = 0 
            # Get SHUI_21point5percent_company_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT and working_days >= 10:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.205
                    else:
                        first_value = combo * 0.205
                    # 2nd if
                    if combo > 83200000:
                        second_value = 83200000 * 0.01
                    else:
                        second_value = combo * 0.01
                    SHUI_21point5percent_company_pay = round(first_value + second_value)
                elif list_contracts[0].contract_category == contract_category_CTminus and working_days >= 10:
                    combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                    if combo > 29800000:
                        SHUI_21point5percent_company_pay = 29800000 * 0.005
                    else:
                        SHUI_21point5percent_company_pay = combo * 0.005      
                else:
                    SHUI_21point5percent_company_pay = 0    
            else:
                SHUI_21point5percent_company_pay = 0
            # Get recuperation_of_SHU_Ins_21point5percent_company_pay
            recuperation_of_SHU_Ins_21point5percent_company_pay = 0
            # Get occupational_accident_and_disease
            occupational_accident_and_disease = 0
            # Get trade_union_fee_company_pay
            combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
            if SHUI_10point5percent_employee_pay > 0:
                if combo > 29800000:
                    salarytoBH = 29800000
                else:
                    salarytoBH = combo
            else:
                salarytoBH = 0
            trade_union_fee_company_pay = round(salarytoBH* 2/100)
            # Get trade_union_fee_employee_pay
            if trade_union_fee_company_pay > 0:
                trade_union_fee_employee_pay = 4160000 * 1/100
            else:
                trade_union_fee_employee_pay = 0
            # Get family_deduction
            list_of_dependents = Employee_children.objects.filter(employee=employee)
            number_of_dependents = list_of_dependents.count()
            family_deduction = 11000000 + (4400000 * number_of_dependents)
            # Get taxable_income
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
            contract_category_CTminusHUU = Contract_category.objects.get(contract_category='CT-HUU')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus or list_contracts[0].contract_category == contract_category_CTminusHUU:
                    sum_K_Y = gross_income + transportation + phone + lunch + travel + responsibility + seniority_bonus + other + outstanding_annual_leave + OTC_incentive + KPI_achievement + month_13_salary_Pro_ata + incentive_last_month + incentive_last_quy_last_year + taxable_overtime
                    taxable_income = sum_K_Y + occupational_accident_and_disease - lunch
                else:
                    sum_K_Z = gross_income + transportation + phone + lunch + travel + responsibility + seniority_bonus + other + outstanding_annual_leave + OTC_incentive + KPI_achievement + month_13_salary_Pro_ata + incentive_last_month + incentive_last_quy_last_year + taxable_overtime + nontaxable_overtime
                    taxable_income = sum_K_Z + occupational_accident_and_disease
            else: 
                taxable_income = 0   
            # Get taxed_income
            if taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction < 0:
                taxed_income = 0
            else:
                taxed_income = taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction
            # Get PIT_13th_salary
            PIT_13th_salary = 0
            # Get PIT
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus or list_contracts[0].contract_category == contract_category_CTminusHUU :
                    if 5000000 < taxed_income <= 10000000:
                        PIT_before_round = (taxed_income * 0.1) - 250000
                    elif 10000000 < taxed_income <= 18000000:
                        PIT_before_round = (taxed_income * 0.15) - 750000
                    elif 18000000 < taxed_income <= 32000000:
                        PIT_before_round = (taxed_income * 0.2) - 1650000
                    elif 32000000 < taxed_income <= 52000000:
                        PIT_before_round = (taxed_income * 0.25) - 3250000
                    elif 52000000 < taxed_income <= 80000000:
                        PIT_before_round = (taxed_income * 0.3) - 5850000
                    elif taxed_income > 80000000:
                        PIT_before_round = (taxed_income * 0.35) - 9850000
                    else: 
                        PIT_before_round = taxed_income * 0.05
                elif taxed_income >= 2000000:
                    PIT_before_round = taxed_income * 10/100
                else:
                    PIT_before_round = 0                     
            else:
                PIT_before_round = 0
            PIT = round(PIT_before_round)
            # Get PIT_balance
            PIT_balance = PIT - PIT_13th_salary
            # Get first_payment
            first_payment = 0
            # Get net_income
            sum_K_Z = gross_income + transportation + phone + lunch + travel + responsibility + seniority_bonus + other + outstanding_annual_leave + OTC_incentive + KPI_achievement + month_13_salary_Pro_ata + incentive_last_month + incentive_last_quy_last_year + taxable_overtime + nontaxable_overtime
            net_income = sum_K_Z + occupational_accident_and_disease - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - PIT_balance - first_payment
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            total_cost = round(sum_K_Z + SHUI_21point5percent_company_pay + recuperation_of_SHU_Ins_21point5percent_company_pay + occupational_accident_and_disease + trade_union_fee_company_pay + trade_union_fee_employee_pay + transfer_bank)
            
            payroll_employee_info = Payroll_Tedis_Vietha(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,
                                                  gross_income=gross_income,transportation=transportation,phone=phone,lunch=lunch,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                  other=other,outstanding_annual_leave=outstanding_annual_leave,OTC_incentive=OTC_incentive,KPI_achievement=KPI_achievement,month_13_salary_Pro_ata=month_13_salary_Pro_ata,incentive_last_month=incentive_last_month,incentive_last_quy_last_year=incentive_last_quy_last_year,taxable_overtime=taxable_overtime,nontaxable_overtime=nontaxable_overtime,
                                                  SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                                  occupational_accident_and_disease=occupational_accident_and_disease,
                                                  trade_union_fee_company_pay=trade_union_fee_company_pay,trade_union_fee_employee_pay=trade_union_fee_employee_pay,family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT_13th_salary=PIT_13th_salary,PIT=PIT,PIT_balance=PIT_balance,
                                                  first_payment=first_payment,net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
            payroll_employee_info.save()
        messages.success(request, 'SUCCESS: Payroll created')
        return redirect('employee:payroll_tedis_vietha',pk=period_month.id)
            
            
        

    # Export payroll
    if request.POST.get('get_payroll'):   
        file_name = str(period_month.month_name) + '_payroll-Tedis-VietHa.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 640, colour black;' % 'white')
        style_head_small = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 300, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % '67')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Payroll Tedis Viet Ha')

        # Table
        
        # Set col width
        for col in range(0,42):
            ws.col(col).width = 5000
        
        
        # Top
        ws.write_merge(0, 0, 0, 6, 'PAYROLL IN ' + str(period_month.month_name), style_head)
        ws.write_merge(0, 0, 9, 11, 'TEDIS - VIET HA',style_head)
        
        # Body
        # Set row height
        ws.row(2).set_style(xlwt.easyxf('font:height 500;'))
        # Body head
        ws.write(2, 0, 'No.', style_table_head)
        ws.write(2, 1, 'Employee code', style_table_head)
        ws.write(2, 2, 'Full name', style_table_head)
        ws.write(2, 3, 'Joining Date', style_table_head)
        ws.write(2, 4, 'Department', style_table_head)
        ws.write(2, 5, 'Title', style_table_head)
        ws.write(2, 6, 'Salary ' + str(period_month.period.period_year) + ' (VND)', style_table_head)
        ws.write(2, 7, 'Working days', style_table_head)
        ws.write(2, 8, '% Adjust', style_table_head)
        ws.write(2, 9, 'Gross Income', style_table_head)
        ws.write(2, 10, 'Transportation', style_table_head)
        ws.write(2, 11, 'Phone', style_table_head)
        ws.write(2, 12, 'Lunch', style_table_head)
        ws.write(2, 13, 'Travel', style_table_head)
        ws.write(2, 14, 'Responsibility', style_table_head)
        ws.write(2, 15, 'Seniority Bonus', style_table_head)
        ws.write(2, 16, 'Others', style_table_head)
        ws.write(2, 17, 'Outstanding annual leave', style_table_head)
        ws.write(2, 18, 'OTC Incentive', style_table_head)
        ws.write(2, 19, 'KPI Achievement', style_table_head)
        ws.write(2, 20, '13th salary (pro-rata)', style_table_head)
        ws.write(2, 21, 'Incentive last month', style_table_head)
        ws.write(2, 22, 'Incentive last quarter', style_table_head)
        ws.write(2, 23, 'Taxable Overtime', style_table_head)
        ws.write(2, 24, 'Non Taxable Overtime', style_table_head)
        ws.write(2, 25, 'SHUI(10.5%)(Employee pay)', style_table_head)
        ws.write(2, 26, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_table_head)
        ws.write(2, 27, 'SHUI(21.5%)(Company pay)', style_table_head)
        ws.write(2, 28, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_table_head)
        ws.write(2, 29, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_table_head)
        ws.write(2, 30, 'Trade Union fee (Company pay)', style_table_head)
        ws.write(2, 31, 'Trade Union fee (Employee pay)', style_table_head)
        ws.write(2, 32, 'Family deduction', style_table_head)
        ws.write(2, 33, 'Taxable Income', style_table_head)
        ws.write(2, 34, 'Taxed Income', style_table_head)
        ws.write(2, 35, 'PIT 13th salary', style_table_head)
        ws.write(2, 36, 'PIT', style_table_head)
        ws.write(2, 37, 'PIT balance', style_table_head)
        ws.write(2, 38, '1st payment', style_table_head)
        ws.write(2, 39, 'Net Income', style_table_head)
        ws.write(2, 40, 'Transfer Bank', style_table_head)
        ws.write(2, 41, 'Total Cost', style_table_head)
        
        # Body
        # Create total var
        ttnewest_salary = 0
        ttgross_income = 0
        tttransportation = 0
        ttphone = 0
        ttlunch = 0
        tttravel = 0
        ttresponsibility = 0
        ttseniority_bonus = 0
        ttother = 0
        ttoutstanding_annual_leave = 0
        ttOTC_incentive = 0
        ttKPI_achievement = 0
        ttmonth_13_salary_Pro_ata = 0
        ttincentive_last_month = 0
        ttincentive_last_quy_last_year = 0
        tttaxable_overtime = 0
        ttnontaxable_overtime = 0
        ttSHUI_10point5percent_employee_pay = 0
        ttrecuperation_of_SHU_Ins_10point5percent_staff_pay = 0
        ttSHUI_21point5percent_company_pay = 0
        ttrecuperation_of_SHU_Ins_21point5percent_company_pay = 0
        ttoccupational_accident_and_disease = 0
        tttrade_union_fee_company_pay = 0
        tttrade_union_fee_employee_pay = 0
        ttfamily_deduction = 0
        tttaxable_income = 0
        tttaxed_income = 0
        ttPIT_13th_salary = 0
        ttPIT = 0
        ttPIT_balance = 0
        ttfirst_payment = 0
        ttnet_income = 0
        tttransfer_bank = 0
        tttotal_cost = 0
        
        for index, data in enumerate(list_payroll_info):
            # Set row height
            ws.row(3+index).set_style(xlwt.easyxf('font:height 500;'))
            # Write data
            ws.write(3+index, 0, str(index+1),style_normal)
            ws.write(3+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws.write(3+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws.write(3+index, 3, str(data['payroll_info'].employee.joining_date.strftime('%d/%m/%Y')),style_normal)
            ws.write(3+index, 4, str(data['payroll_info'].employee.department_e),style_normal)
            ws.write(3+index, 5, str(data['payroll_info'].employee.position_e),style_normal)
            ws.write(3+index, 6, str("{:,}".format(round(data['payroll_info'].newest_salary))),style_normal)
            ws.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws.write(3+index, 8, str(round(data['payroll_info'].adjust_percent)) + '%',style_normal)
            ws.write(3+index, 9, str("{:,}".format(round(data['payroll_info'].gross_income))),style_normal)
            ws.write(3+index, 10, str("{:,}".format(round(data['payroll_info'].transportation))),style_normal)
            ws.write(3+index, 11, str("{:,}".format(round(data['payroll_info'].phone))),style_normal)
            ws.write(3+index, 12, str("{:,}".format(round(data['payroll_info'].lunch))),style_normal)
            ws.write(3+index, 13, str("{:,}".format(round(data['payroll_info'].travel))),style_normal)
            ws.write(3+index, 14, str("{:,}".format(round(data['payroll_info'].responsibility))),style_normal)
            ws.write(3+index, 15, str("{:,}".format(round(data['payroll_info'].seniority_bonus))),style_normal)
            ws.write(3+index, 16, str("{:,}".format(round(data['payroll_info'].other))),style_normal)
            ws.write(3+index, 17, str("{:,}".format(round(data['payroll_info'].outstanding_annual_leave))),style_normal)
            ws.write(3+index, 18, str("{:,}".format(round(data['payroll_info'].OTC_incentive))),style_normal)
            ws.write(3+index, 19, str("{:,}".format(round(data['payroll_info'].KPI_achievement))),style_normal)
            ws.write(3+index, 20, str("{:,}".format(round(data['payroll_info'].month_13_salary_Pro_ata))),style_normal)
            ws.write(3+index, 21, str("{:,}".format(round(data['payroll_info'].incentive_last_month))),style_normal)
            ws.write(3+index, 22, str("{:,}".format(round(data['payroll_info'].incentive_last_quy_last_year))),style_normal)
            ws.write(3+index, 23, str("{:,}".format(round(data['payroll_info'].taxable_overtime))),style_normal)
            ws.write(3+index, 24, str("{:,}".format(round(data['payroll_info'].nontaxable_overtime))),style_normal)
            ws.write(3+index, 25, str("{:,}".format(round(data['payroll_info'].SHUI_10point5percent_employee_pay))),style_normal)
            ws.write(3+index, 26, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay))),style_normal)
            ws.write(3+index, 27, str("{:,}".format(round(data['payroll_info'].SHUI_21point5percent_company_pay))),style_normal)
            ws.write(3+index, 28, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay))),style_normal)
            ws.write(3+index, 29, str("{:,}".format(round(data['payroll_info'].occupational_accident_and_disease))),style_normal)
            ws.write(3+index, 30, str("{:,}".format(round(data['payroll_info'].trade_union_fee_company_pay))),style_normal)
            ws.write(3+index, 31, str("{:,}".format(round(data['payroll_info'].trade_union_fee_employee_pay))),style_normal)
            ws.write(3+index, 32, str("{:,}".format(round(data['payroll_info'].family_deduction))),style_normal)
            ws.write(3+index, 33, str("{:,}".format(round(data['payroll_info'].taxable_income))),style_normal)
            ws.write(3+index, 34, str("{:,}".format(round(data['payroll_info'].taxed_income))),style_normal)
            ws.write(3+index, 35, str("{:,}".format(round(data['payroll_info'].PIT_13th_salary))),style_normal)
            ws.write(3+index, 36, str("{:,}".format(round(data['payroll_info'].PIT))),style_normal)
            ws.write(3+index, 37, str("{:,}".format(round(data['payroll_info'].PIT_balance))),style_normal)
            ws.write(3+index, 38, str("{:,}".format(round(data['payroll_info'].first_payment))),style_normal)
            ws.write(3+index, 39, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws.write(3+index, 40, str("{:,}".format(round(data['payroll_info'].transfer_bank))),style_normal)
            ws.write(3+index, 41, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 3+index+1
            ttnewest_salary += data['payroll_info'].newest_salary
            ttgross_income += data['payroll_info'].gross_income
            tttransportation += data['payroll_info'].transportation
            ttphone += data['payroll_info'].phone
            ttlunch += data['payroll_info'].lunch
            tttravel += data['payroll_info'].travel
            ttresponsibility += data['payroll_info'].responsibility
            ttseniority_bonus += data['payroll_info'].seniority_bonus
            ttother += data['payroll_info'].other
            ttoutstanding_annual_leave += data['payroll_info'].outstanding_annual_leave
            ttOTC_incentive += data['payroll_info'].OTC_incentive
            ttKPI_achievement += data['payroll_info'].KPI_achievement
            ttmonth_13_salary_Pro_ata += data['payroll_info'].month_13_salary_Pro_ata
            ttincentive_last_month += data['payroll_info'].incentive_last_month
            ttincentive_last_quy_last_year += data['payroll_info'].incentive_last_quy_last_year
            tttaxable_overtime += data['payroll_info'].taxable_overtime
            ttnontaxable_overtime += data['payroll_info'].nontaxable_overtime
            ttSHUI_10point5percent_employee_pay += data['payroll_info'].SHUI_10point5percent_employee_pay
            ttrecuperation_of_SHU_Ins_10point5percent_staff_pay += data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay
            ttSHUI_21point5percent_company_pay += data['payroll_info'].SHUI_21point5percent_company_pay
            ttrecuperation_of_SHU_Ins_21point5percent_company_pay += data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay
            ttoccupational_accident_and_disease += data['payroll_info'].occupational_accident_and_disease
            tttrade_union_fee_company_pay += data['payroll_info'].trade_union_fee_company_pay
            tttrade_union_fee_employee_pay += data['payroll_info'].trade_union_fee_employee_pay
            ttfamily_deduction += data['payroll_info'].family_deduction
            tttaxable_income += data['payroll_info'].taxable_income
            tttaxed_income += data['payroll_info'].taxed_income
            ttPIT_13th_salary += data['payroll_info'].PIT_13th_salary
            ttPIT += data['payroll_info'].PIT
            ttPIT_balance += data['payroll_info'].PIT_balance
            ttfirst_payment += data['payroll_info'].first_payment
            ttnet_income += data['payroll_info'].net_income
            tttransfer_bank += data['payroll_info'].transfer_bank
            tttotal_cost += data['payroll_info'].total_cost
        # Total line in bottom of table 
        ws.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_table_head)
        ws.write(last_row, 6, str("{:,}".format(round(ttnewest_salary))),style_table_head)
        ws.write(last_row, 7, '-',style_table_head)
        ws.write(last_row, 8, '-',style_table_head)
        ws.write(last_row, 9, str("{:,}".format(round(ttgross_income))),style_table_head)
        ws.write(last_row, 10, str("{:,}".format(round(tttransportation))),style_table_head)
        ws.write(last_row, 11, str("{:,}".format(round(ttphone))),style_table_head)
        ws.write(last_row, 12, str("{:,}".format(round(ttlunch))),style_table_head)
        ws.write(last_row, 13, str("{:,}".format(round(tttravel))),style_table_head)
        ws.write(last_row, 14, str("{:,}".format(round(ttresponsibility))),style_table_head)
        ws.write(last_row, 15, str("{:,}".format(round(ttseniority_bonus))),style_table_head)
        ws.write(last_row, 16, str("{:,}".format(round(ttother))),style_table_head)
        ws.write(last_row, 17, str("{:,}".format(round(ttoutstanding_annual_leave))),style_table_head)
        ws.write(last_row, 18, str("{:,}".format(round(ttOTC_incentive))),style_table_head)
        ws.write(last_row, 19, str("{:,}".format(round(ttKPI_achievement))),style_table_head)
        ws.write(last_row, 20, str("{:,}".format(round(ttmonth_13_salary_Pro_ata))),style_table_head)
        ws.write(last_row, 21, str("{:,}".format(round(ttincentive_last_month))),style_table_head)
        ws.write(last_row, 22, str("{:,}".format(round(ttincentive_last_quy_last_year))),style_table_head)
        ws.write(last_row, 23, str("{:,}".format(round(tttaxable_overtime))),style_table_head)
        ws.write(last_row, 24, str("{:,}".format(round(ttnontaxable_overtime))),style_table_head)
        ws.write(last_row, 25, str("{:,}".format(round(ttSHUI_10point5percent_employee_pay))),style_table_head)
        ws.write(last_row, 26, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay))),style_table_head)
        ws.write(last_row, 27, str("{:,}".format(round(ttSHUI_21point5percent_company_pay))),style_table_head)
        ws.write(last_row, 28, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_21point5percent_company_pay))),style_table_head)
        ws.write(last_row, 29, str("{:,}".format(round(ttoccupational_accident_and_disease))),style_table_head)
        ws.write(last_row, 30, str("{:,}".format(round(tttrade_union_fee_company_pay))),style_table_head)
        ws.write(last_row, 31, str("{:,}".format(round(tttrade_union_fee_employee_pay))),style_table_head)
        ws.write(last_row, 32, str("{:,}".format(round(ttfamily_deduction))),style_table_head)
        ws.write(last_row, 33, str("{:,}".format(round(tttaxable_income))),style_table_head)
        ws.write(last_row, 34, str("{:,}".format(round(tttaxed_income))),style_table_head)
        ws.write(last_row, 35, str("{:,}".format(round(ttPIT_13th_salary))),style_table_head)
        ws.write(last_row, 36, str("{:,}".format(round(ttPIT))),style_table_head)
        ws.write(last_row, 37, str("{:,}".format(round(ttPIT_balance))),style_table_head)
        ws.write(last_row, 38, str("{:,}".format(round(ttfirst_payment))),style_table_head)
        ws.write(last_row, 39, str("{:,}".format(round(ttnet_income))),style_table_head)
        ws.write(last_row, 40, str("{:,}".format(round(tttransfer_bank))),style_table_head)
        ws.write(last_row, 41, str("{:,}".format(round(tttotal_cost))),style_table_head)
         


        wb.save(response)
        return response

  
    
    return render(request, 'employee/view_payroll_tedisvietha.html', {
        'period_month' : period_month,
        'payrollExist': payrollExist,
        'list_payroll_info' : list_payroll_info,
        'working_day_wh' : working_day_wh,
        'working_day_bo' : working_day_bo,
    })


def payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    payroll_info = Payroll_Tedis_Vietha.objects.get(pk=pk)
    
    # Get month total working days
    employee = payroll_info.employee
    '''Get Working day of BO and Working day of WH'''
    warehouse_department_e = Department_E.objects.get(department_e='Warehouse')
    if employee.department_e == warehouse_department_e:
        list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0)
        month_total_working_days = 0
        for daily_work_info in list_daily_work_info:
            month_total_working_days += daily_work_info.work
    else:
        list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0)
        month_total_working_days = 0
        for daily_work_info in list_daily_work_info:
            month_total_working_days += daily_work_info.work
    
    # Update payroll info
    if request.POST.get('btnupdatepayroll'):
        # Get month,employee,newest_salary,working_days,adjust_percent
        month = payroll_info.month
        employee = payroll_info.employee
        newest_salary = payroll_info.newest_salary
        working_days = float(request.POST.get('working_days'))
        adjust_percent = payroll_info.adjust_percent
        # Get gross_income
        gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(month_total_working_days) )
        # Get transportation,phone,lunch,travel,responsibility,seniority_bonus
        transportation = payroll_info.transportation
        phone = payroll_info.phone
        lunch = payroll_info.lunch
        travel = payroll_info.travel
        responsibility = payroll_info.responsibility
        seniority_bonus = payroll_info.seniority_bonus
        # Get other,outstanding_annual_leave,OTC_incentive,KPI_achievement,month_13_salary_Pro_ata,incentive_last_month,incentive_last_quy_last_year,taxable_overtime,nontaxable_overtime
        other = request.POST.get('other')
        outstanding_annual_leave = request.POST.get('outstanding_annual_leave')
        OTC_incentive = request.POST.get('OTC_incentive')
        KPI_achievement = request.POST.get('KPI_achievement')
        month_13_salary_Pro_ata = request.POST.get('month_13_salary_Pro_ata')
        incentive_last_month = request.POST.get('incentive_last_month')
        incentive_last_quy_last_year = request.POST.get('incentive_last_quy_last_year')
        taxable_overtime = request.POST.get('taxable_overtime')
        nontaxable_overtime = request.POST.get('nontaxable_overtime')    
        # Get SHUI_10point5percent_employee_pay
        contract_category_CT = Contract_category.objects.get(contract_category='CT')
        list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT and working_days >= 10:
                combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                # 1st if
                if combo > 29800000:
                    first_value = 29800000 * 0.095
                else:
                    first_value = combo * 0.095
                # 2nd if
                if combo > 83200000:
                    second_value = 83200000 * 0.01
                else:
                    second_value = combo * 0.01
                SHUI_10point5percent_employee_pay = round(first_value + second_value)
            else: 
                    SHUI_10point5percent_employee_pay = 0
        else:
            SHUI_10point5percent_employee_pay = 0
        # Get recuperation_of_SHU_Ins_10point5percent_staff_pay
        recuperation_of_SHU_Ins_10point5percent_staff_pay = request.POST.get('recuperation_of_SHU_Ins_10point5percent_staff_pay')
        # Get SHUI_21point5percent_company_pay
        contract_category_CT = Contract_category.objects.get(contract_category='CT')
        contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT and working_days >= 10:
                combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                # 1st if
                if combo > 29800000:
                    first_value = 29800000 * 0.205
                else:
                    first_value = combo * 0.205
                # 2nd if
                if combo > 83200000:
                    second_value = 83200000 * 0.01
                else:
                    second_value = combo * 0.01
                SHUI_21point5percent_company_pay = round(first_value + second_value)
            elif list_contracts[0].contract_category == contract_category_CTminus and working_days >= 10:
                combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                if combo > 29800000:
                    SHUI_21point5percent_company_pay = 29800000 * 0.005
                else:
                    SHUI_21point5percent_company_pay = combo * 0.005      
            else:
                SHUI_21point5percent_company_pay = 0    
        else:
            SHUI_21point5percent_company_pay = 0
        # Get recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease
        recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
        occupational_accident_and_disease = request.POST.get('occupational_accident_and_disease')
        # Get trade_union_fee_company_pay
        combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
        if SHUI_10point5percent_employee_pay > 0:
            if combo > 29800000:
                salarytoBH = 29800000
            else:
                salarytoBH = combo
        else:
            salarytoBH = 0
        trade_union_fee_company_pay = round(salarytoBH* 2/100)
        # Get trade_union_fee_employee_pay
        if trade_union_fee_company_pay > 0:
            trade_union_fee_employee_pay = 4160000 * 1/100
        else:
            trade_union_fee_employee_pay = 0
        # Get family_deduction
        family_deduction = payroll_info.family_deduction
        # Get taxable_income
        contract_category_CT = Contract_category.objects.get(contract_category='CT')
        contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
        contract_category_CTminusHUU = Contract_category.objects.get(contract_category='CT-HUU')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus or list_contracts[0].contract_category == contract_category_CTminusHUU:
                sum_K_Y = float(gross_income) + float(transportation) + float(phone) + float(lunch) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(outstanding_annual_leave) + float(OTC_incentive) + float(KPI_achievement) + float(month_13_salary_Pro_ata) + float(incentive_last_month) + float(incentive_last_quy_last_year) + float(taxable_overtime)
                taxable_income = float(sum_K_Y) + float(occupational_accident_and_disease) - float(lunch)
            else:
                sum_K_Z = float(gross_income) + float(transportation) + float(phone) + float(lunch) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(outstanding_annual_leave) + float(OTC_incentive) + float(KPI_achievement) + float(month_13_salary_Pro_ata) + float(incentive_last_month) + float(incentive_last_quy_last_year) + float(taxable_overtime) + float(nontaxable_overtime)
                taxable_income = float(sum_K_Z) + float(occupational_accident_and_disease)
        else: 
            taxable_income = 0   
        # Get taxed_income
        if float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction) < 0:
            taxed_income = 0
        else:
            taxed_income = float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction)
        # Get PIT_13th_salary
        PIT_13th_salary = request.POST.get('PIT_13th_salary')
        # Get PIT
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus or list_contracts[0].contract_category == contract_category_CTminusHUU :
                if 5000000 < taxed_income <= 10000000:
                    PIT_before_round = (taxed_income * 0.1) - 250000
                elif 10000000 < taxed_income <= 18000000:
                    PIT_before_round = (taxed_income * 0.15) - 750000
                elif 18000000 < taxed_income <= 32000000:
                    PIT_before_round = (taxed_income * 0.2) - 1650000
                elif 32000000 < taxed_income <= 52000000:
                    PIT_before_round = (taxed_income * 0.25) - 3250000
                elif 52000000 < taxed_income <= 80000000:
                    PIT_before_round = (taxed_income * 0.3) - 5850000
                elif taxed_income > 80000000:
                    PIT_before_round = (taxed_income * 0.35) - 9850000
                else: 
                    PIT_before_round = taxed_income * 0.05
            elif taxed_income >= 2000000:
                PIT_before_round = taxed_income * 10/100
            else:
                PIT_before_round = 0                     
        else:
            PIT_before_round = 0
        PIT = round(PIT_before_round)
        # Get PIT_balance
        PIT_balance = float(PIT) - float(PIT_13th_salary)
        # Get first_payment
        first_payment = request.POST.get('first_payment')
        # Get net_income
        sum_K_Z = float(gross_income) + float(transportation) + float(phone) + float(lunch) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(outstanding_annual_leave) + float(OTC_incentive) + float(KPI_achievement) + float(month_13_salary_Pro_ata) + float(incentive_last_month) + float(incentive_last_quy_last_year) + float(taxable_overtime) + float(nontaxable_overtime)
        net_income = sum_K_Z + float(occupational_accident_and_disease) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(PIT_balance) - float(first_payment)
        # Get transfer_bank
        transfer_bank = request.POST.get('transfer_bank')
        # Get total_cost
        total_cost = round(sum_K_Z + float(SHUI_21point5percent_company_pay) + float(recuperation_of_SHU_Ins_21point5percent_company_pay) + float(occupational_accident_and_disease) + float(trade_union_fee_company_pay) + float(trade_union_fee_employee_pay) + float(transfer_bank))
        # Update and save
        payroll_update_info = Payroll_Tedis_Vietha(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                            transportation=transportation,phone=phone,lunch=lunch,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                            other=other,outstanding_annual_leave=outstanding_annual_leave,OTC_incentive=OTC_incentive,KPI_achievement=KPI_achievement,month_13_salary_Pro_ata=month_13_salary_Pro_ata,incentive_last_month=incentive_last_month,incentive_last_quy_last_year=incentive_last_quy_last_year,taxable_overtime=taxable_overtime,nontaxable_overtime=nontaxable_overtime,
                                            SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                            occupational_accident_and_disease=occupational_accident_and_disease,
                                            trade_union_fee_company_pay=trade_union_fee_company_pay,trade_union_fee_employee_pay=trade_union_fee_employee_pay,
                                            family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT_13th_salary=PIT_13th_salary,PIT=PIT,PIT_balance=PIT_balance,first_payment=first_payment,net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
        payroll_update_info.save()
        messages.success(request, 'SUCCESS: Payroll updated')
        return redirect('employee:payroll_tedis_vietha_edit',pk=payroll_info.id)
        
        
        
    
    return render(request, 'employee/payroll_tedis_vietha_edit.html', {
        'payroll_info' : payroll_info,
        'month_total_working_days' : month_total_working_days,
        
    })


def payroll_vietha(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    

    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    
    
    # Get payroll data
    site_vietha = Site.objects.get(site='VH')
    list_employee_vietha = Employee.objects.filter(site=site_vietha)
    # Get total_working_days
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    total_working_day = list_work_days.count()
    # Create payroll dict
    list_payroll_info = []
    for employee in list_employee_vietha:
        try:
            payroll_info = Payroll_Vietha.objects.get(employee=employee,month=period_month)
            payrollExist = 1
            # Make data 
            data = {
                'payroll_info': payroll_info,
                
                
            }
            list_payroll_info.append(data)
        except Payroll_Vietha.DoesNotExist:
            payrollExist = 0
        
    # Create payroll data
    if request.POST.get('btn_adjust_percent'):
        # Get % Adjust  
        adjust_percent = float(request.POST.get('adjust_percent'))
        
        site_vietha = Site.objects.get(site='VH')
        list_employee_vietha = Employee.objects.filter(site=site_vietha)
        for employee in list_employee_vietha:
            # Get Salary info
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
            if list_contracts.count() == 0:
                newest_salary = 0
            else:
                newest_salary = list_contracts[0].basic_salary
            # Get working days
            list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
            daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
            unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
            working_days = daily_work_info.count() - unpaid_leave_info.count()
            total_working_day = daily_work_info.count()
            # Get gross income
            gross_income = round(float(newest_salary) * float(adjust_percent)/100 * float(working_days)/float(total_working_day) )
            # Get salary_recuperation
            salary_recuperation = 0
            # Get OT hour to pay salary
            ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
            total_paid_hour = 0
            for application in ot_applications:
                total_paid_hour += application.ot_paid_hour
            salary_per_hour = newest_salary/total_working_day/8
            overtime = round(salary_per_hour * total_paid_hour)
            # Get transportation,phone,lunch,responsibility
            if list_contracts.count() == 0:
                transportation = 0
                phone = 0
                lunch = 0
                responsibility = 0
            else:
                transportation = round(list_contracts[0].transportation_support * working_days / total_working_day)
                phone = round(list_contracts[0].telephone_support * working_days / total_working_day)
                lunch = round(list_contracts[0].lunch_support * working_days / total_working_day)
                responsibility = round(list_contracts[0].responsibility_allowance * working_days / total_working_day)
            # Get outstanding_annual_leave,bonus_open_new_pharmacy,other,incentive_last_quy_last_year,incentive_last_month,yearly_incentive_last_year,month_13_salary_Pro_ata
            outstanding_annual_leave = 0
            bonus_open_new_pharmacy = 0
            other = 0
            incentive_last_quy_last_year = 0
            incentive_last_month = 0
            yearly_incentive_last_year = 0
            month_13_salary_Pro_ata = 0
            # Get SHUI_10point5percent_employee_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')  
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT and working_days >= 11:
                    combo = newest_salary + responsibility/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.095
                    else:
                        first_value = combo * 0.095
                    # 2nd if
                    if combo > 93600000:
                        second_value = 93600000 * 0.01
                    else:
                        second_value = combo * 0.01
                    SHUI_10point5percent_employee_pay = round(first_value + second_value)
                else: 
                        SHUI_10point5percent_employee_pay = 0
            else:
                SHUI_10point5percent_employee_pay = 0
            # Get SHUI_21point5percent_company_pay
            contract_category_CT = Contract_category.objects.get(contract_category='CT')  
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT and working_days >= 11:
                    combo = newest_salary + responsibility/float(adjust_percent/100)
                    # 1st if
                    if combo > 29800000:
                        first_value = 29800000 * 0.205
                    else:
                        first_value = combo * 0.205
                    # 2nd if
                    if combo > 93600000:
                        second_value = 93600000 * 0.01
                    else:
                        second_value = combo * 0.01
                    SHUI_21point5percent_company_pay = round(first_value + second_value)
                else: 
                        SHUI_21point5percent_company_pay = 0
            else:
                SHUI_21point5percent_company_pay = 0
            # Get occupational_accident_and_disease
            occupational_accident_and_disease = 0
            # Get trade_union_fee_company_pay
            combo = newest_salary + responsibility/float(adjust_percent/100)
            if SHUI_10point5percent_employee_pay > 0:
                if combo > 29800000:
                    salarytoBH = 29800000
                else:
                    salarytoBH = combo
            else:
                salarytoBH = 0
            trade_union_fee_company_pay = round(salarytoBH* 2/100)
            # Get trade_union_fee_staff_pay
            trade_union_fee_staff_pay = 0
            # Get family_deduction
            list_of_dependents = Employee_children.objects.filter(employee=employee)
            number_of_dependents = list_of_dependents.count()
            family_deduction = 11000000 + (4400000 * number_of_dependents)
            # Get taxable_income
            contract_category_CT = Contract_category.objects.get(contract_category='CT')
            contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus:
                    sum_K_X = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year + month_13_salary_Pro_ata
                    taxable_income = sum_K_X + occupational_accident_and_disease - lunch
                else:
                    sum_K_X = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year + month_13_salary_Pro_ata
                    taxable_income = sum_K_X + occupational_accident_and_disease
            else: 
                taxable_income = 0   
            # Get taxed_income
            if taxable_income - SHUI_10point5percent_employee_pay - family_deduction < 0:
                taxed_income = 0
            else:
                taxed_income = taxable_income - SHUI_10point5percent_employee_pay - family_deduction
            # Get PIT_for_13th_salary
            PIT_for_13th_salary = 0
            # Get PIT_this_month
            if list_contracts.count() != 0:
                if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus:
                    if 5000000 < taxed_income <= 10000000:
                        PIT_before_round = (taxed_income * 0.1) - 250000
                    elif 10000000 < taxed_income <= 18000000:
                        PIT_before_round = (taxed_income * 0.15) - 750000
                    elif 18000000 < taxed_income <= 32000000:
                        PIT_before_round = (taxed_income * 0.2) - 1650000
                    elif 32000000 < taxed_income <= 52000000:
                        PIT_before_round = (taxed_income * 0.25) - 3250000
                    elif 52000000 < taxed_income <= 80000000:
                        PIT_before_round = (taxed_income * 0.3) - 5850000
                    elif taxed_income > 80000000:
                        PIT_before_round = (taxed_income * 0.35) - 9850000
                    else: 
                        PIT_before_round = taxed_income * 0.05
                elif taxable_income >= 2000000:
                    PIT_before_round = taxable_income * 10/100
                else:
                    PIT_before_round = 0                     
            else:
                PIT_before_round = 0
            PIT_this_month = round(PIT_before_round)
            # Get PIT_finalization
            PIT_finalization = 0
            # Get PIT_balance
            PIT_balance = PIT_this_month - PIT_for_13th_salary
            # Get net_income
            sum_K_W = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year
            net_income = round(sum_K_W + occupational_accident_and_disease - SHUI_10point5percent_employee_pay - PIT_balance, 0)
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            sum_K_W = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year
            total_cost = round(sum_K_W + SHUI_21point5percent_company_pay + occupational_accident_and_disease + trade_union_fee_company_pay + trade_union_fee_staff_pay + transfer_bank,0)

            
            payroll_employee_info = Payroll_Vietha(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                                   salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,responsibility=responsibility,
                                                   outstanding_annual_leave=outstanding_annual_leave,bonus_open_new_pharmacy=bonus_open_new_pharmacy,other=other,
                                                   incentive_last_quy_last_year=incentive_last_quy_last_year,incentive_last_month=incentive_last_month,yearly_incentive_last_year=yearly_incentive_last_year,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                                   SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,
                                                   occupational_accident_and_disease=occupational_accident_and_disease,
                                                   trade_union_fee_company_pay=trade_union_fee_company_pay,trade_union_fee_staff_pay=trade_union_fee_staff_pay,
                                                   family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,
                                                   PIT_for_13th_salary=PIT_for_13th_salary,PIT_this_month=PIT_this_month,PIT_finalization=PIT_finalization,PIT_balance=PIT_balance,
                                                   net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost
                                                   )
            payroll_employee_info.save()
        messages.success(request, 'SUCCESS: Payroll created')
        return redirect('employee:payroll_vietha',pk=period_month.id)
            
            
        

    # Export payroll
    if request.POST.get('get_payroll'):   
        file_name = str(period_month.month_name) + '_payroll-VietHa.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 640, colour black;' % 'white')
        style_head_small = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 300, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % '67')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Payroll Viet Ha')

        # Table
        
        # Set col width
        for col in range(0,42):
            ws.col(col).width = 5000
        
        
        # Top
        ws.write_merge(0, 0, 0, 6, 'PAYROLL IN ' + str(period_month.month_name), style_head)
        ws.write_merge(0, 0, 9, 11, 'TEDIS - VIET HA',style_head)
        
        # Body
        # Set row height
        ws.row(2).set_style(xlwt.easyxf('font:height 500;'))
        # Body head
        ws.write(2, 0, 'No.', style_table_head)
        ws.write(2, 1, 'Employee code', style_table_head)
        ws.write(2, 2, 'Full name', style_table_head)
        ws.write(2, 3, 'Joining Date', style_table_head)
        ws.write(2, 4, 'Department/Area', style_table_head)
        ws.write(2, 5, 'Job Title', style_table_head)
        ws.write(2, 6, 'Salary', style_table_head)
        ws.write(2, 7, 'Working days', style_table_head)
        ws.write(2, 8, '% Adjust', style_table_head)
        ws.write(2, 9, 'Gross Income', style_table_head)
        ws.write(2, 10, 'Salary recuperation', style_table_head)
        ws.write(2, 11, 'Overtime', style_table_head)
        ws.write(2, 12, 'Transportation', style_table_head)
        ws.write(2, 13, 'Phone', style_table_head)
        ws.write(2, 14, 'Lunch', style_table_head)
        ws.write(2, 15, 'Responsibility', style_table_head)
        ws.write(2, 16, 'Outstanding annual leave', style_table_head)
        ws.write(2, 17, 'Bonus open new pharmacy', style_table_head)
        ws.write(2, 18, 'Others', style_table_head)
        ws.write(2, 19, 'Incentive last quarter', style_table_head)
        ws.write(2, 20, 'Incentive last month', style_table_head)
        ws.write(2, 21, 'Yearly Incentive', style_table_head)
        ws.write(2, 22, '13th salary (pro-rata)', style_table_head)
        ws.write(2, 23, 'SHUI(10.5%)(Employee pay)', style_table_head)
        ws.write(2, 24, 'SHUI(21.5%)(Company pay)', style_table_head)
        ws.write(2, 25, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_table_head)
        ws.write(2, 26, 'Trade Union fee (Company pay)', style_table_head)
        ws.write(2, 27, 'Trade Union fee (Staff pay)', style_table_head)
        ws.write(2, 28, 'Family deduction', style_table_head)
        ws.write(2, 29, 'Taxable Income', style_table_head)
        ws.write(2, 30, 'Taxed Income', style_table_head)
        ws.write(2, 31, 'PIT for 13th salary', style_table_head)
        ws.write(2, 32, 'PIT ' + str(period_month.month_name), style_table_head)
        ws.write(2, 33, 'PIT Finalization', style_table_head)
        ws.write(2, 34, 'PIT balance', style_table_head)
        ws.write(2, 35, 'Net Income', style_table_head)
        ws.write(2, 36, 'Transfer Bank', style_table_head)
        ws.write(2, 37, 'Total Cost', style_table_head)
        
        # Body
        # Create total var
        ttnewest_salary = 0
        ttgross_income = 0
        ttsalary_recuperation = 0
        ttovertime = 0
        tttransportation = 0
        ttphone = 0
        ttlunch = 0
        ttresponsibility = 0
        ttoutstanding_annual_leave = 0
        ttbonus_open_new_pharmacy = 0
        ttother = 0
        ttincentive_last_quy_last_year = 0
        ttincentive_last_month = 0
        ttyearly_incentive_last_year = 0
        ttmonth_13_salary_Pro_ata = 0
        ttSHUI_10point5percent_employee_pay = 0
        ttSHUI_21point5percent_company_pay = 0
        ttoccupational_accident_and_disease = 0
        tttrade_union_fee_company_pay = 0
        tttrade_union_fee_staff_pay = 0
        ttfamily_deduction = 0
        tttaxable_income = 0
        tttaxed_income = 0
        ttPIT_for_13th_salary = 0
        ttPIT_this_month = 0
        ttPIT_finalization = 0
        ttPIT_balance = 0
        ttnet_income = 0
        tttransfer_bank = 0
        tttotal_cost = 0
        
        for index, data in enumerate(list_payroll_info):
            # Set row height
            ws.row(3+index).set_style(xlwt.easyxf('font:height 500;'))
            # Write data
            ws.write(3+index, 0, str(index+1),style_normal)
            ws.write(3+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws.write(3+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws.write(3+index, 3, str(data['payroll_info'].employee.joining_date.strftime('%d/%m/%Y')),style_normal)
            ws.write(3+index, 4, str(data['payroll_info'].employee.department_e),style_normal)
            ws.write(3+index, 5, str(data['payroll_info'].employee.position_e),style_normal)
            ws.write(3+index, 6, str("{:,}".format(round(data['payroll_info'].newest_salary))),style_normal)
            ws.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws.write(3+index, 8, str(round(data['payroll_info'].adjust_percent)) + '%',style_normal)
            ws.write(3+index, 9, str("{:,}".format(round(data['payroll_info'].gross_income))),style_normal)
            ws.write(3+index, 10, str("{:,}".format(round(data['payroll_info'].salary_recuperation))),style_normal)
            ws.write(3+index, 11, str("{:,}".format(round(data['payroll_info'].overtime))),style_normal)
            ws.write(3+index, 12, str("{:,}".format(round(data['payroll_info'].transportation))),style_normal)
            ws.write(3+index, 13, str("{:,}".format(round(data['payroll_info'].phone))),style_normal)
            ws.write(3+index, 14, str("{:,}".format(round(data['payroll_info'].lunch))),style_normal)
            ws.write(3+index, 15, str("{:,}".format(round(data['payroll_info'].responsibility))),style_normal)
            ws.write(3+index, 16, str("{:,}".format(round(data['payroll_info'].outstanding_annual_leave))),style_normal)
            ws.write(3+index, 17, str("{:,}".format(round(data['payroll_info'].bonus_open_new_pharmacy))),style_normal)
            ws.write(3+index, 18, str("{:,}".format(round(data['payroll_info'].other))),style_normal)
            ws.write(3+index, 19, str("{:,}".format(round(data['payroll_info'].incentive_last_quy_last_year))),style_normal)
            ws.write(3+index, 20, str("{:,}".format(round(data['payroll_info'].incentive_last_month))),style_normal)
            ws.write(3+index, 21, str("{:,}".format(round(data['payroll_info'].yearly_incentive_last_year))),style_normal)
            ws.write(3+index, 22, str("{:,}".format(round(data['payroll_info'].month_13_salary_Pro_ata))),style_normal)
            ws.write(3+index, 23, str("{:,}".format(round(data['payroll_info'].SHUI_10point5percent_employee_pay))),style_normal)
            ws.write(3+index, 24, str("{:,}".format(round(data['payroll_info'].SHUI_21point5percent_company_pay))),style_normal)
            ws.write(3+index, 25, str("{:,}".format(round(data['payroll_info'].occupational_accident_and_disease))),style_normal)
            ws.write(3+index, 26, str("{:,}".format(round(data['payroll_info'].trade_union_fee_company_pay))),style_normal)
            ws.write(3+index, 27, str("{:,}".format(round(data['payroll_info'].trade_union_fee_staff_pay))),style_normal)
            ws.write(3+index, 28, str("{:,}".format(round(data['payroll_info'].family_deduction))),style_normal)
            ws.write(3+index, 29, str("{:,}".format(round(data['payroll_info'].taxable_income))),style_normal)
            ws.write(3+index, 30, str("{:,}".format(round(data['payroll_info'].taxed_income))),style_normal)
            ws.write(3+index, 31, str("{:,}".format(round(data['payroll_info'].PIT_for_13th_salary))),style_normal)
            ws.write(3+index, 32, str("{:,}".format(round(data['payroll_info'].PIT_this_month))),style_normal)
            ws.write(3+index, 33, str("{:,}".format(round(data['payroll_info'].PIT_finalization))),style_normal)
            ws.write(3+index, 34, str("{:,}".format(round(data['payroll_info'].PIT_balance))),style_normal)
            ws.write(3+index, 35, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws.write(3+index, 36, str("{:,}".format(round(data['payroll_info'].transfer_bank))),style_normal)
            ws.write(3+index, 37, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 3+index+1
            ttnewest_salary += data['payroll_info'].newest_salary
            ttgross_income += data['payroll_info'].gross_income
            ttsalary_recuperation += data['payroll_info'].salary_recuperation
            ttovertime += data['payroll_info'].overtime
            tttransportation += data['payroll_info'].transportation
            ttphone += data['payroll_info'].phone
            ttlunch += data['payroll_info'].lunch
            ttresponsibility += data['payroll_info'].responsibility
            ttoutstanding_annual_leave += data['payroll_info'].outstanding_annual_leave
            ttbonus_open_new_pharmacy += data['payroll_info'].bonus_open_new_pharmacy
            ttother += data['payroll_info'].other
            ttincentive_last_quy_last_year += data['payroll_info'].incentive_last_quy_last_year
            ttincentive_last_month += data['payroll_info'].incentive_last_month
            ttyearly_incentive_last_year += data['payroll_info'].yearly_incentive_last_year
            ttmonth_13_salary_Pro_ata += data['payroll_info'].month_13_salary_Pro_ata
            ttSHUI_10point5percent_employee_pay += data['payroll_info'].SHUI_10point5percent_employee_pay
            ttSHUI_21point5percent_company_pay += data['payroll_info'].SHUI_21point5percent_company_pay
            ttoccupational_accident_and_disease += data['payroll_info'].occupational_accident_and_disease
            tttrade_union_fee_company_pay += data['payroll_info'].trade_union_fee_company_pay
            tttrade_union_fee_staff_pay += data['payroll_info'].trade_union_fee_staff_pay
            ttfamily_deduction += data['payroll_info'].family_deduction
            tttaxable_income += data['payroll_info'].taxable_income
            tttaxed_income += data['payroll_info'].taxed_income
            ttPIT_for_13th_salary += data['payroll_info'].PIT_for_13th_salary
            ttPIT_this_month += data['payroll_info'].PIT_this_month
            ttPIT_finalization += data['payroll_info'].PIT_finalization
            ttPIT_balance += data['payroll_info'].PIT_balance
            ttnet_income += data['payroll_info'].net_income
            tttransfer_bank += data['payroll_info'].transfer_bank
            tttotal_cost += data['payroll_info'].total_cost
        # Total line in bottom of table 
        ws.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_table_head)
        ws.write(last_row, 6, str("{:,}".format(ttnewest_salary)),style_table_head)
        ws.write(last_row, 7, '-',style_table_head)
        ws.write(last_row, 8, '-',style_table_head)
        ws.write(last_row, 9, str("{:,}".format(ttgross_income)),style_table_head)
        ws.write(last_row, 10, str("{:,}".format(ttsalary_recuperation)),style_table_head)
        ws.write(last_row, 11, str("{:,}".format(ttovertime)),style_table_head)
        ws.write(last_row, 12, str("{:,}".format(tttransportation)),style_table_head)
        ws.write(last_row, 13, str("{:,}".format(ttphone)),style_table_head)
        ws.write(last_row, 14, str("{:,}".format(ttlunch)),style_table_head)
        ws.write(last_row, 15, str("{:,}".format(ttresponsibility)),style_table_head)
        ws.write(last_row, 16, str("{:,}".format(ttoutstanding_annual_leave)),style_table_head)
        ws.write(last_row, 17, str("{:,}".format(ttbonus_open_new_pharmacy)),style_table_head)
        ws.write(last_row, 18, str("{:,}".format(ttother)),style_table_head)
        ws.write(last_row, 19, str("{:,}".format(ttincentive_last_quy_last_year)),style_table_head)
        ws.write(last_row, 20, str("{:,}".format(ttincentive_last_month)),style_table_head)
        ws.write(last_row, 21, str("{:,}".format(ttyearly_incentive_last_year)),style_table_head)
        ws.write(last_row, 22, str("{:,}".format(ttmonth_13_salary_Pro_ata)),style_table_head)
        ws.write(last_row, 23, str("{:,}".format(ttSHUI_10point5percent_employee_pay)),style_table_head)
        ws.write(last_row, 24, str("{:,}".format(ttSHUI_21point5percent_company_pay)),style_table_head)
        ws.write(last_row, 25, str("{:,}".format(ttoccupational_accident_and_disease)),style_table_head)
        ws.write(last_row, 26, str("{:,}".format(tttrade_union_fee_company_pay)),style_table_head)
        ws.write(last_row, 27, str("{:,}".format(tttrade_union_fee_staff_pay)),style_table_head)
        ws.write(last_row, 28, str("{:,}".format(ttfamily_deduction)),style_table_head)
        ws.write(last_row, 29, str("{:,}".format(tttaxable_income)),style_table_head)
        ws.write(last_row, 30, str("{:,}".format(tttaxed_income)),style_table_head)
        ws.write(last_row, 31, str("{:,}".format(ttPIT_for_13th_salary)),style_table_head)
        ws.write(last_row, 32, str("{:,}".format(ttPIT_this_month)),style_table_head)  
        ws.write(last_row, 33, str("{:,}".format(ttPIT_finalization)),style_table_head)
        ws.write(last_row, 34, str("{:,}".format(ttPIT_balance)),style_table_head)
        ws.write(last_row, 35, str("{:,}".format(ttnet_income)),style_table_head)
        ws.write(last_row, 36, str("{:,}".format(tttransfer_bank)),style_table_head)
        ws.write(last_row, 37, str("{:,}".format(tttotal_cost)),style_table_head)
         


        wb.save(response)
        return response

  
    
    return render(request, 'employee/view_payroll_vietha.html', {
        'period_month' : period_month,
        'payrollExist': payrollExist,
        'list_payroll_info' : list_payroll_info,
        'total_working_day' : total_working_day,
    })    


def payroll_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    payroll_info = Payroll_Vietha.objects.get(pk=pk)
    
    # Get month total working days
    list_work_days = Daily_work.objects.filter(month=payroll_info.month,weekend=False,holiday=False)
    month_total_working_days = list_work_days.count()
    
    # Update payroll info
    if request.POST.get('btnupdatepayroll'):
        # Get month,employee,newest_salary,working_days,adjust_percent
        month = payroll_info.month
        employee = payroll_info.employee
        newest_salary = payroll_info.newest_salary
        working_days = payroll_info.working_days
        adjust_percent = payroll_info.adjust_percent
        # Get gross income
        gross_income = payroll_info.gross_income
        # Get salary_recuperation
        salary_recuperation = request.POST.get('salary_recuperation')
        # Get overtime
        overtime = payroll_info.overtime
        # Get transportation,phone,lunch
        transportation = payroll_info.transportation
        phone = payroll_info.phone
        lunch = payroll_info.lunch
        responsibility = payroll_info.responsibility
        # Get outstanding_annual_leave,bonus_open_new_pharmacy,other,incentive_last_quy_last_year,incentive_last_month,yearly_incentive_last_year,month_13_salary_Pro_ata
        outstanding_annual_leave = request.POST.get('outstanding_annual_leave')
        bonus_open_new_pharmacy = request.POST.get('bonus_open_new_pharmacy')
        other = request.POST.get('other')
        incentive_last_quy_last_year = request.POST.get('incentive_last_quy_last_year')
        incentive_last_month = request.POST.get('incentive_last_month')
        yearly_incentive_last_year = request.POST.get('yearly_incentive_last_year')
        month_13_salary_Pro_ata = request.POST.get('month_13_salary_Pro_ata')
        # Get SHUI_10point5percent_employee_pay
        list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
        contract_category_CT = Contract_category.objects.get(contract_category='CT')  
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT and working_days >= 11:
                combo = newest_salary + float(responsibility)/float(adjust_percent/100)
                # 1st if
                if combo > 29800000:
                    first_value = 29800000 * 0.095
                else:
                    first_value = combo * 0.095
                # 2nd if
                if combo > 93600000:
                    second_value = 93600000 * 0.01
                else:
                    second_value = combo * 0.01
                SHUI_10point5percent_employee_pay = round(first_value + second_value)
            else: 
                    SHUI_10point5percent_employee_pay = 0
        else:
            SHUI_10point5percent_employee_pay = 0
        # Get SHUI_21point5percent_company_pay
        contract_category_CT = Contract_category.objects.get(contract_category='CT')  
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT and working_days >= 11:
                combo = newest_salary + responsibility/float(adjust_percent/100)
                # 1st if
                if combo > 29800000:
                    first_value = 29800000 * 0.205
                else:
                    first_value = combo * 0.205
                # 2nd if
                if combo > 93600000:
                    second_value = 93600000 * 0.01
                else:
                    second_value = combo * 0.01
                SHUI_21point5percent_company_pay = round(first_value + second_value)
            else: 
                    SHUI_21point5percent_company_pay = 0
        else:
            SHUI_21point5percent_company_pay = 0
        # Get occupational_accident_and_disease
        occupational_accident_and_disease = request.POST.get('occupational_accident_and_disease')
        # Get trade_union_fee_company_pay
        combo = newest_salary + float(responsibility)/float(adjust_percent/100)
        if SHUI_10point5percent_employee_pay > 0:
            if combo > 29800000:
                salarytoBH = 29800000
            else:
                salarytoBH = combo
        else:
            salarytoBH = 0
        trade_union_fee_company_pay = round(salarytoBH* 2/100)
        # Get trade_union_fee_staff_pay
        trade_union_fee_staff_pay = request.POST.get('trade_union_fee_staff_pay')
        # Get family_deduction
        family_deduction = payroll_info.family_deduction
        # Get taxable_income
        contract_category_CT = Contract_category.objects.get(contract_category='CT')
        contract_category_CTminus = Contract_category.objects.get(contract_category='CT-')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus:
                sum_K_X = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year) + float(month_13_salary_Pro_ata)
                taxable_income = sum_K_X + float(occupational_accident_and_disease) - float(lunch)
            else:
                sum_K_X = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year) + float(month_13_salary_Pro_ata)
                taxable_income = sum_K_X + float(occupational_accident_and_disease)
        else: 
            taxable_income = 0   
        # Get taxed_income
        if taxable_income - float(SHUI_10point5percent_employee_pay) - float(family_deduction) < 0:
            taxed_income = 0
        else:
            taxed_income = float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(family_deduction)
        # Get PIT_for_13th_salary
        PIT_for_13th_salary = request.POST.get('PIT_for_13th_salary')
        # Get PIT_this_month
        if list_contracts.count() != 0:
            if list_contracts[0].contract_category == contract_category_CT or list_contracts[0].contract_category == contract_category_CTminus:
                if 5000000 < taxed_income <= 10000000:
                    PIT_before_round = (taxed_income * 0.1) - 250000
                elif 10000000 < taxed_income <= 18000000:
                    PIT_before_round = (taxed_income * 0.15) - 750000
                elif 18000000 < taxed_income <= 32000000:
                    PIT_before_round = (taxed_income * 0.2) - 1650000
                elif 32000000 < taxed_income <= 52000000:
                    PIT_before_round = (taxed_income * 0.25) - 3250000
                elif 52000000 < taxed_income <= 80000000:
                    PIT_before_round = (taxed_income * 0.3) - 5850000
                elif taxed_income > 80000000:
                    PIT_before_round = (taxed_income * 0.35) - 9850000
                else: 
                    PIT_before_round = taxed_income * 0.05
            elif taxable_income >= 2000000:
                PIT_before_round = taxable_income * 10/100
            else:
                PIT_before_round = 0                     
        else:
            PIT_before_round = 0
        PIT_this_month = round(PIT_before_round)
        # Get PIT_finalization
        PIT_finalization = request.POST.get('PIT_finalization')
        # Get PIT_balance
        PIT_balance = PIT_this_month - float(PIT_for_13th_salary)
        # Get net_income
        sum_K_W = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year)
        net_income = round(sum_K_W + float(occupational_accident_and_disease) - float(SHUI_10point5percent_employee_pay) - float(PIT_balance), 0)
        # Get transfer_bank
        transfer_bank = request.POST.get('transfer_bank')
        # Get total_cost
        sum_K_W = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year)
        total_cost = round(sum_K_W + float(SHUI_21point5percent_company_pay) + float(occupational_accident_and_disease) + float(trade_union_fee_company_pay) + float(trade_union_fee_staff_pay) + float(transfer_bank),0)
        
        # Update and save
        payroll_update_info = Payroll_Vietha(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                            salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,responsibility=responsibility,
                                            outstanding_annual_leave=outstanding_annual_leave,bonus_open_new_pharmacy=bonus_open_new_pharmacy,other=other,
                                            incentive_last_quy_last_year=incentive_last_quy_last_year,incentive_last_month=incentive_last_month,yearly_incentive_last_year=yearly_incentive_last_year,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                            SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,
                                            occupational_accident_and_disease=occupational_accident_and_disease,
                                            trade_union_fee_company_pay=trade_union_fee_company_pay,trade_union_fee_staff_pay=trade_union_fee_staff_pay,
                                            family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,
                                            PIT_for_13th_salary=PIT_for_13th_salary,PIT_this_month=PIT_this_month,PIT_finalization=PIT_finalization,PIT_balance=PIT_balance,
                                            net_income=net_income,transfer_bank=transfer_bank,total_cost=total_cost)
        payroll_update_info.save()
        messages.success(request, 'SUCCESS: Payroll updated')
        return redirect('employee:payroll_vietha_edit',pk=payroll_info.id)
        
        
        
    
    return render(request, 'employee/payroll_vietha_edit.html', {
        'payroll_info' : payroll_info,
        'month_total_working_days' : month_total_working_days,
        
    })
    
    
# Payroll report
def report_payroll_tedis(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    
    # Get report data
    site_RO = Site.objects.get(site='RO')
    area_HCM = Area.objects.get(area='HCMC')
    list_employee_tedis_HCM = Employee.objects.filter(site=site_RO, area=area_HCM)
    # PIT
    report_pit_payroll = Report_PIT_Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
    if report_pit_payroll.count() > 0:
        report_payrollExist = 1
    else:
        report_pit_payroll = ''
        report_payrollExist = 0    
    # Transfer HCM
    report_transfer_payroll = Report_TransferHCM_Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
    if report_transfer_payroll.count() > 0:
        report_payrollExist = 1
    else:
        report_transfer_payroll = ''
        report_payrollExist = 0 
    # Payment
    item_order = {'SALARY': 1, 'SHUI': 2, 'PIT': 3, 'TRADE UNION': 4}
    report_payment_payroll = Report_Payment_Payroll_Tedis.objects.filter(month=period_month).order_by(Case(*[When(item=item, then=Value(order)) for item, order in item_order.items()], default=Value(999)))
    if report_payment_payroll.count() > 0:
        report_payrollExist = 1
    else:
        report_payment_payroll = ''
        report_payrollExist = 0 
    
    
        
    # Create report 
    if request.POST.get('btn_create_report'): 
        # Create PIT
        payroll_tedis = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis: 
            # thu_nhap_chiu_thue
            thu_nhap_chiu_thue = payroll.taxable_income
            # tong_tnct_khau_tru_thue
            if payroll.PIT > 0:
                tong_tnct_khau_tru_thue = payroll.taxable_income
            else:
                tong_tnct_khau_tru_thue = 0
            # bao_hiem_bat_buoc
            bao_hiem_bat_buoc = payroll.SHUI_10point5percent_employee_pay
            # khau_tru
            khau_tru = payroll.family_deduction
            # thu_nhap_tinh_thue
            thu_nhap_tinh_thue = payroll.taxed_income
            # thuong,khac,cong
            thuong = 0
            khac = 0
            cong = 0
            # thue_tnct_phai_nop
            thue_tnct_phai_nop = payroll.PIT
            # ghi_chu 
            ghi_chu = ''
            
            pit_info = Report_PIT_Payroll_Tedis(month=period_month,payroll=payroll,employee=payroll.employee,
                                                thu_nhap_chiu_thue=thu_nhap_chiu_thue,tong_tnct_khau_tru_thue=tong_tnct_khau_tru_thue,bao_hiem_bat_buoc=bao_hiem_bat_buoc,khau_tru=khau_tru,
                                                thu_nhap_tinh_thue=thu_nhap_tinh_thue,thuong=thuong,khac=khac,cong=cong,
                                                thue_tnct_phai_nop=thue_tnct_phai_nop,ghi_chu=ghi_chu)
            pit_info.save()
            
        # Create Report_TransferHCM_Payroll_Tedis
        payroll_tedis = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis: 
            transferHCM_info = Report_TransferHCM_Payroll_Tedis(month=period_month,payroll=payroll,employee=payroll.employee,
                                                amount=payroll.net_income)
            transferHCM_info.save()
            
        
        # Create Report_Payment_Payroll_Tedis
        '''Salary'''
        # Salary Employee HCM
        amount = 0
        payroll_tedis_HCM = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis_HCM:
            amount += round(payroll.net_income, 0)
        month_string = str(period_month.month_number) + '.' + str(period_month.period.period_year)
        payment_salary_employee_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                        item='SALARY',description='EMPLOYEES',area='HCM',amount=amount,
                                                                        paidby='Transfer',paidto='Employees',account_no='Lương tháng ' + month_string)
        payment_salary_employee_HCM_info.save()
        # Salary Employee HANOI
        amount = 0
        site_RO = Site.objects.get(site='RO')
        area_HANOI = Area.objects.get(area='HANOI')
        list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
        payroll_tedis_HANOI = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HANOI,month=period_month)
        for payroll in payroll_tedis_HANOI:
            amount += round(payroll.net_income, 0)
        month_string = str(period_month.month_number) + '/' + str(period_month.period.period_year)
        payment_salary_employee_HANOI_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                        item='SALARY',description='EMPLOYEES',area='HANOI',amount=amount,
                                                                        paidby='Transfer',paidto='Employees',account_no='Lương tháng ' + month_string)
        payment_salary_employee_HANOI_info.save()
        # Salary MARJORIE HCM
        payment_salary_MARJORIE_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                        item='SALARY',description='MARJORIE',area='HCM',amount=0,
                                                                        paidby='Cash',paidto='Marjorie',account_no='')
        payment_salary_MARJORIE_HCM_info.save()
        '''SHUI'''
        # SHUI Company HCM
        SHUI_Company_amount = 0
        payroll_tedis_HCM = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis_HCM:
            SHUI_Company_amount += round(payroll.SHUI_21point5percent_company_pay)
        payment_SHUI_Company_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                    item='SHUI',description='SHUI Company',area='HCM',amount=SHUI_Company_amount,
                                                                    paidby='Transfer',paidto='District 7 SI',account_no='BHXH Quận 7 - 018.100.978.9789 - Vietcombank (Mã đơn vị: YV0047G, VPĐD Tedis tại TP.HCM)')
        payment_SHUI_Company_HCM_info.save()
        # SHUI Employees HCM
        SHUI_Employees_amount = 0
        payroll_tedis_HCM = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis_HCM:
            SHUI_Employees_amount += round(payroll.SHUI_10point5percent_employee_pay)
        payment_SHUI_Employees_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                    item='SHUI',description='SHUI Employees',area='HCM',amount=SHUI_Employees_amount,
                                                                    paidby='Transfer',paidto='',account_no='BHXH Quận 7 - 018.100.978.9789 - Vietcombank (Mã đơn vị: YV0047G, VPĐD Tedis tại TP.HCM)')
        payment_SHUI_Employees_HCM_info.save()
        # SHUI Company HANOI
        SHUI_Company_amount = 0
        site_RO = Site.objects.get(site='RO')
        area_HANOI = Area.objects.get(area='HANOI')
        list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
        payroll_tedis_HANOI = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HANOI,month=period_month)
        for payroll in payroll_tedis_HANOI:
            SHUI_Company_amount += round(payroll.SHUI_21point5percent_company_pay)
        payment_SHUI_Company_HANOI_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                    item='SHUI',description='SHUI Company',area='HANOI',amount=SHUI_Company_amount,
                                                                    paidby='Transfer',paidto='',account_no='BHXH Quận Ba Đình - 144.02.02.901.025 - Agribank - CN Bắc HN (Mã đơn vị: YV0043A, VPDĐ Công ty Tedis tại TP. Hà Nội)')
        payment_SHUI_Company_HANOI_info.save()
        # SHUI Employees HANOI
        SHUI_Employees_amount = 0
        site_RO = Site.objects.get(site='RO')
        area_HANOI = Area.objects.get(area='HANOI')
        list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
        payroll_tedis_HANOI = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HANOI,month=period_month)
        for payroll in payroll_tedis_HANOI:
            SHUI_Employees_amount += round(payroll.SHUI_10point5percent_employee_pay)
        payment_SHUI_Employees_HANOI_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                    item='SHUI',description='SHUI Employees',area='HANOI',amount=SHUI_Employees_amount,
                                                                    paidby='Transfer',paidto='',account_no='BHXH Quận Ba Đình - 144.02.02.901.025 - Agribank - CN Bắc HN (Mã đơn vị: YV0043A, VPDĐ Công ty Tedis tại TP. Hà Nội)')
        payment_SHUI_Employees_HANOI_info.save()
        '''PIT'''
        # PIT HCM
        PIT_HCM_amount = 0
        payroll_tedis_HCM = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis_HCM:
            PIT_HCM_amount += round(payroll.PIT)
        payment_PIT_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                            item='PIT',description='PIT HCM',area='HCM',amount=PIT_HCM_amount,
                                                            paidby='Transfer',paidto='Tax HCM',account_no='Cục thuế TP.HCM - 7111.1056137 - KBNN TP.HCM')
        payment_PIT_HCM_info.save()
        # PIT HANOI
        PIT_HANOI_amount = 0
        site_RO = Site.objects.get(site='RO')
        area_HANOI = Area.objects.get(area='HANOI')
        list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
        payroll_tedis_HANOI = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HANOI,month=period_month)
        for payroll in payroll_tedis_HANOI:
            PIT_HANOI_amount += round(payroll.PIT)
        payment_PIT_HANOI_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                            item='PIT',description='PIT HANOI',area='HANOI',amount=PIT_HANOI_amount,
                                                            paidby='Transfer',paidto='Tax Hanoi',account_no='Cục thuế TP.Hà Nội - 7111 - KBNN TP.Hà Nội  NH Vietcombank')
        payment_PIT_HANOI_info.save()
        # PIT MARJORIE
        month_string = str(period_month.month_number) + '/' + str(period_month.period.period_year)
        payment_PIT_MARJORIE_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                                item='PIT',description='PIT Ms. MARJORIE',area='HCM',amount=0,
                                                                paidby='Transfer',paidto='Tax HCM ',account_no='Cục thuế TP.HCM - 7111.1056137 - KBNN TP.HCM  MST 0310648270  tháng ' + month_string)
        payment_PIT_MARJORIE_info.save()
        '''TRADE UNION'''
        # Trade Union fee HCM
        trade_union_fee_company_HCM_amount = 0
        payroll_tedis_HCM = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis_HCM:
            trade_union_fee_company_HCM_amount += round(payroll.trade_union_fee_company_pay_2percent)
        payment_trade_union_fee_company_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                            item='TRADE UNION',description='Trade Union fee HCM',area='HCM',amount=trade_union_fee_company_HCM_amount,
                                                            paidby='Transfer',paidto='Trade Union',account_no='Công đoàn Việt Nam - 117001366668 - NH Vietinbank - CN Hoàng Mai - Hà Nội  Nội dung: MST 0304653674 VPĐD TEDIS tại TP.HCM đóng KPCĐ 2% tháng 03/2023')
        payment_trade_union_fee_company_HCM_info.save()
        # Trade Union HCM (member fee)
        trade_union_fee_member_HCM_amount = 0
        payroll_tedis_HCM = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HCM,month=period_month)
        for payroll in payroll_tedis_HCM:
            trade_union_fee_member_HCM_amount += round(payroll.trade_union_fee_member)
        payment_trade_union_fee_member_HCM_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                            item='TRADE UNION',description='Trade Union HCM (member fee)',area='HCM',amount=trade_union_fee_member_HCM_amount,
                                                            paidby='Transfer',paidto='Trade Union',account_no='BCH CONG DOAN VPDD TEDIS TAI TPHCM - 127000041929 - NH TMCP Công thương Việt Nam - CN 4 - HCM  Nội dung: MST 0304653674 VPĐD TEDIS tại TP.HCM đóng ĐPCĐ 1% tháng 03/2023')
        payment_trade_union_fee_member_HCM_info.save()
        # Trade Union fee HA NOI
        trade_union_fee_company_HANOI_amount = 0
        site_RO = Site.objects.get(site='RO')
        area_HANOI = Area.objects.get(area='HANOI')
        list_employee_tedis_HANOI = Employee.objects.filter(site=site_RO, area=area_HANOI)
        payroll_tedis_HANOI = Payroll_Tedis.objects.filter(employee__in=list_employee_tedis_HANOI,month=period_month)
        for payroll in payroll_tedis_HANOI:
            trade_union_fee_company_HANOI_amount += round(payroll.trade_union_fee_company_pay_2percent)
        payment_trade_union_fee_company_HANOI_info = Report_Payment_Payroll_Tedis(month=period_month,
                                                            item='TRADE UNION',description='Trade Union fee HA NOI',area='HANOI',amount=trade_union_fee_company_HANOI_amount,
                                                            paidby='Transfer',paidto='Trade Union',account_no='Liên đoàn lao động Quận Ba Đình - 111000000272 - NH Vietinbank - CN Ba Đình - Hà Nội  Nội dung: MST 0102666127 VPĐD CÔNG TY TEDIS TẠI TP. HÀ NỘI nộp KPCĐ 2% tháng 03/2023')
        payment_trade_union_fee_company_HANOI_info.save()
        
        
        
        messages.success(request, 'SUCCESS: Report created!')
        return redirect('employee:report_payroll_tedis',pk=period_month.id)

    # Add payment record 
    if request.POST.get('btnAddPayment'):
        month_id = request.POST.get('month')
        month = Month_in_period.objects.get(id=month_id)
        item = request.POST.get('item')
        description = request.POST.get('description')
        area = request.POST.get('area')
        amount = request.POST.get('amount')
        paidby = request.POST.get('paidby')
        paidto = request.POST.get('paidto')
        account_no = request.POST.get('account_no')
        payment_newrecord_info = Report_Payment_Payroll_Tedis(month=month,
                                                            item=item,description=description,area=area,amount=amount,
                                                            paidby=paidby,paidto=paidto,account_no=account_no)
        payment_newrecord_info.save()
        messages.success(request, 'SUCCESS: Payment record created')
        return redirect('employee:report_payroll_tedis',pk=period_month.id)
        
    
    
    # Export report
    if request.POST.get('export'):   
        # Export excel
        file_name = str(period_month.month_number) + ' Salary ' + str(period_month.month_name) + '_TD.xlsx'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_total_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 200, name Arial, colour red; align: horiz center, vert center' % 'white')
        style_total_red_onlyvertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 200, name Arial, colour red; align: vert center' % 'white')
        style_head_11pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                           'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Times New Roman, colour black; align: horiz center, vert center' % 'white')
        style_head_11pt_bold.alignment.wrap = 1
        style_head_11pt_bold_left = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                           'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Times New Roman, colour black; align: horiz left, vert center' % 'white')
        style_head_11pt_bold_green = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                           'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Times New Roman, colour black; align: horiz center, vert center' % 'lime')
        style_head_small = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 300, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'pale_blue')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        
        
        '''Sheet PIT'''
        # Create sheet
        ws_PIT = wb.add_sheet('PIT')
        # Set col width
        ws_PIT.col(0).width = 2000
        ws_PIT.col(1).width = 3500
        for col in range(2,14):
            ws_PIT.col(col).width = 5000
        
        # Set row height
        ws_PIT.row(0).height_mismatch = True
        ws_PIT.row(0).height = 330
        ws_PIT.row(1).height_mismatch = True
        ws_PIT.row(1).height = 670
        # Top
        ws_PIT.write_merge(0, 1, 0, 0, 'STT', style_head_11pt_bold)
        ws_PIT.write_merge(0, 1, 1, 1, 'Mã nhân viên', style_head_11pt_bold)
        ws_PIT.write_merge(0, 1, 2, 2, 'Họ và tên', style_head_11pt_bold_left)
        ws_PIT.write_merge(0, 1, 3, 3, 'CCCD', style_head_11pt_bold)
        ws_PIT.write_merge(0, 1, 4, 4, 'MST cá nhân', style_head_11pt_bold)
        ws_PIT.write_merge(0, 0, 5, 8, 'Thu nhập chịu thuế', style_head_11pt_bold)
        ws_PIT.write(1, 5, 'Thu nhập chịu thuế', style_head_11pt_bold_green)
        ws_PIT.write(1, 6, 'Tổng TNCT thuộc diện khấu trừ thuế', style_head_11pt_bold)
        ws_PIT.write(1, 7, 'Bảo hiểm bắt buộc', style_head_11pt_bold)
        ws_PIT.write(1, 8, 'Khấu trừ', style_head_11pt_bold)
        ws_PIT.write_merge(0, 0, 9, 12, 'Thu nhập tính thuế', style_head_11pt_bold)
        ws_PIT.write(1, 9, 'Thu nhập tính thuế', style_head_11pt_bold_green)
        ws_PIT.write(1, 10, 'Thưởng', style_head_11pt_bold)  
        ws_PIT.write(1, 11, 'Khác', style_head_11pt_bold) 
        ws_PIT.write(1, 12, 'Cộng', style_head_11pt_bold)        
        ws_PIT.write_merge(0, 1, 13, 13, 'Thuế TNCN phải nộp', style_head_11pt_bold_green)
        ws_PIT.write_merge(0, 1, 14, 14, 'Ghi Chú', style_head_11pt_bold_left)
        # Body
        # A
        ws_PIT.write(2, 0, 'A', style_head_11pt_bold)
        ws_PIT.write(2, 2, 'Người Việt Nam', style_head_11pt_bold)
        for col_row2 in range(3,15):
            ws_PIT.write(2, col_row2, '', style_head_11pt_bold)
        # PIT data
        # Khai báo total
        ttthu_nhap_chiu_thue = 0
        tttong_tnct_khau_tru_thue = 0
        ttbao_hiem_bat_buoc = 0
        ttkhau_tru = 0
        ttthu_nhap_tinh_thue = 0
        ttthuong = 0
        ttkhac = 0
        ttcong = 0
        ttthue_tnct_phai_nop = 0
        ttghichu = 0
        
        for index, pit_data in enumerate(report_pit_payroll):
            # Set row height
            ws_PIT.row(3+index).height_mismatch = True
            ws_PIT.row(3+index).height = 400
            # Write data
            ws_PIT.write(3+index, 0, str(index+1),style_normal)
            ws_PIT.write(3+index, 1, str(pit_data.employee.employee_code),style_normal)
            ws_PIT.write(3+index, 2, str(pit_data.employee.full_name),style_normal)
            ws_PIT.write(3+index, 3, str(pit_data.employee.id_card_no),style_normal)
            ws_PIT.write(3+index, 4, str(pit_data.employee.personal_income_tax),style_normal)
            ws_PIT.write(3+index, 5, str("{:,}".format(round(pit_data.thu_nhap_chiu_thue),0)),style_normal)
            ws_PIT.write(3+index, 6, str("{:,}".format(round(pit_data.tong_tnct_khau_tru_thue),0)),style_normal)
            ws_PIT.write(3+index, 7, str("{:,}".format(round(pit_data.bao_hiem_bat_buoc),0)),style_normal)
            ws_PIT.write(3+index, 8, str("{:,}".format(round(pit_data.khau_tru),0)),style_normal)
            ws_PIT.write(3+index, 9, str("{:,}".format(round(pit_data.thu_nhap_tinh_thue),0)),style_normal)
            ws_PIT.write(3+index, 10, str("{:,}".format(round(pit_data.thuong),0)),style_normal)
            ws_PIT.write(3+index, 11, str("{:,}".format(round(pit_data.khac),0)),style_normal)
            ws_PIT.write(3+index, 12, str("{:,}".format(round(pit_data.cong),0)),style_normal)
            ws_PIT.write(3+index, 13, str("{:,}".format(round(pit_data.thue_tnct_phai_nop),0)),style_normal)
            ws_PIT.write(3+index, 14, str(pit_data.ghi_chu),style_normal)
            # Total
            ttthu_nhap_chiu_thue += round(pit_data.thu_nhap_chiu_thue,0)
            tttong_tnct_khau_tru_thue += round(pit_data.tong_tnct_khau_tru_thue,0)
            ttbao_hiem_bat_buoc += round(pit_data.bao_hiem_bat_buoc,0) 
            ttkhau_tru += round(pit_data.khau_tru,0)
            ttthu_nhap_tinh_thue += round(pit_data.thu_nhap_tinh_thue,0)
            ttthuong += round(pit_data.thuong,0)
            ttkhac += round(pit_data.khac,0)
            ttcong += round(pit_data.cong,0)
            ttthue_tnct_phai_nop += round(pit_data.thue_tnct_phai_nop,0)
            if pit_data.thue_tnct_phai_nop > 0:
                ttghichu += 1
            last_row = 3+index+1
        # Total
        # Set row height
        ws_PIT.row(last_row).height_mismatch = True
        ws_PIT.row(last_row).height = 400
        # data
        ws_PIT.write(last_row, 0, str(index+1), style_total_red)
        ws_PIT.write_merge(last_row, last_row, 1, 4, 'Tổng Cộng A', style_total_red_onlyvertcen)
        ws_PIT.write(last_row, 5, str("{:,}".format(round(ttthu_nhap_chiu_thue),0)), style_total_red)
        ws_PIT.write(last_row, 6, str("{:,}".format(round(tttong_tnct_khau_tru_thue),0)), style_total_red)
        ws_PIT.write(last_row, 7, str("{:,}".format(round(ttbao_hiem_bat_buoc),0)), style_total_red)
        ws_PIT.write(last_row, 8, str("{:,}".format(round(ttkhau_tru),0)), style_total_red)
        ws_PIT.write(last_row, 9, str("{:,}".format(round(ttthu_nhap_tinh_thue),0)), style_total_red)
        ws_PIT.write(last_row, 10, str("{:,}".format(round(ttthuong),0)), style_total_red)
        ws_PIT.write(last_row, 11, str("{:,}".format(round(ttkhac),0)), style_total_red)
        ws_PIT.write(last_row, 12, str("{:,}".format(round(ttcong),0)), style_total_red)
        ws_PIT.write(last_row, 13, str("{:,}".format(round(ttthue_tnct_phai_nop),0)), style_total_red)
        ws_PIT.write(last_row, 14, str(ttghichu), style_total_red)

        
        '''Sheet Transfer HCM'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_12pt_bold_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: vert center' % 'white')
        style_head_24pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 480, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left medium, right medium, top medium, bottom medium;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert center' % 'white')
        
        # Create sheet
        ws_TransferHCM = wb.add_sheet('Transfer HCM')
        # Set col width
        ws_TransferHCM.col(0).width = 2000
        ws_TransferHCM.col(1).width = 3500
        for col in range(2,7):
            if col == 4:
                ws_TransferHCM.col(col).width = 9000
            else:
                ws_TransferHCM.col(col).width = 5000
        
        # Set row height
        ws_TransferHCM.row(0).height_mismatch = True
        ws_TransferHCM.row(0).height = 700
        ws_TransferHCM.row(1).height_mismatch = True
        ws_TransferHCM.row(1).height = 670
        ws_TransferHCM.row(2).height_mismatch = True
        ws_TransferHCM.row(2).height = 800
        ws_TransferHCM.row(3).height_mismatch = True
        ws_TransferHCM.row(3).height = 400
        ws_TransferHCM.row(4).height_mismatch = True
        ws_TransferHCM.row(4).height = 700
        # Head
        # img = Image.open("hr/static/hr/images/logo/logo_tedis_white.png")
        # image_parts = img.split()
        # r = image_parts[0]
        # g = image_parts[1]
        # b = image_parts[2]
        # img = Image.merge("RGB", (r, g, b))
        # fo = BytesIO()
        # img.save(fo, format='bmp')
        # ws_TransferHCM.insert_bitmap_data(fo.getvalue(),1,1)
        # img.close()
        ws_TransferHCM.write(0, 3, 'TEDIS REP. OFFICE IN HO CHI MINH', style_head_12pt_bold_vertbot)
        ws_TransferHCM.write(1, 3, 'Room 2B, Floor 2 & 4 - 150 Nguyen Luong Bang, Tan Phu Ward, District 7', style_head_12pt_vertcen)
        ws_TransferHCM.write_merge(2, 2, 0, 6, 'SALARY TRANSFER LIST', style_head_24pt_bold)
        ws_TransferHCM.write(3, 5, 'Date:', style_11pt_horizright)
        ws_TransferHCM.write(3, 6, datetime.now().strftime('%d/%m/%Y'), style_11pt_horizleft)
        
        # Table
        # Table-head
        ws_TransferHCM.write(4, 0, 'No', style_tablehead_grey25)
        ws_TransferHCM.write(4, 1, 'Employee Code', style_tablehead_grey25)
        ws_TransferHCM.write(4, 2, 'Full Name', style_tablehead_grey25)
        ws_TransferHCM.write(4, 3, 'Bank Account No.', style_tablehead_grey25)
        ws_TransferHCM.write(4, 4, 'With Bank', style_tablehead_grey25)
        ws_TransferHCM.write(4, 5, "Bank's Address", style_tablehead_grey25)
        ws_TransferHCM.write(4, 6, 'Amount', style_tablehead_grey25)
        # Table-Body
        total_amount = 0
        for index, transfer_data in enumerate(report_transfer_payroll):
            # Set row height
            ws_TransferHCM.row(5+index).height_mismatch = True
            ws_TransferHCM.row(5+index).height = 650
            # Write data
            ws_TransferHCM.write(5+index, 0, str(index+1),style_tablebody)
            ws_TransferHCM.write(5+index, 1, str(transfer_data.employee.employee_code),style_tablebody_onlyvertcenter)
            ws_TransferHCM.write(5+index, 2, str(transfer_data.employee.full_name),style_tablebody_onlyvertcenter)
            ws_TransferHCM.write(5+index, 3, str(transfer_data.employee.account_no),style_tablebody_onlyvertcenter)
            ws_TransferHCM.write(5+index, 4, str(transfer_data.employee.bank) + ' - ' + str(transfer_data.employee.branch),style_tablebody_onlyvertcenter)
            ws_TransferHCM.write(5+index, 5, str(transfer_data.employee.bank_address),style_tablebody_onlyvertcenter)
            ws_TransferHCM.write(5+index, 6, str("{:,}".format(round(transfer_data.amount),0)),style_normal)
            total_amount += round(transfer_data.amount, 0)
            last_row = 5 + index + 1
        # Table-footer
        ws_TransferHCM.row(last_row).height_mismatch = True
        ws_TransferHCM.row(last_row).height = 700
        ws_TransferHCM.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_tablehead_grey25)
        ws_TransferHCM.write(last_row, 6, str("{:,}".format(round(total_amount),0)), style_tablehead_grey25) 
        # Footer
        # Set row height
        for i in range(last_row+1, last_row+6):
            if i == last_row+3:
                ws_TransferHCM.row(i).height_mismatch = True
                ws_TransferHCM.row(i).height = 2000
            else: 
                ws_TransferHCM.row(i).height_mismatch = True
                ws_TransferHCM.row(i).height = 650
        ws_TransferHCM.write(last_row+2, 5, 'Approved by', style_footer)
        ws_TransferHCM.write(last_row+4, 5, 'Vũ Châu Kim Anh', style_footer) 
            
    
    
        '''Sheet Payment HCM'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_16pt_bold_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 320, name Arial, colour black; align: vert center' % 'white')
        style_head_12pt_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: vert center' % 'white')
        style_head_20pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 400, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody_vertcen_horizcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 260, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody_vertcen_horizcen.alignment.wrap = 1
        style_tablebody_vertcen_horizcen_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody_vertcen_horizcen_bold.alignment.wrap = 1
        style_tablebody_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 260, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablebody_vertcen_horizleft.alignment.wrap = 1
        style_tablebody_vertcen_horizleft_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablebody_vertcen_horizleft_bold.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 260, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_date = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 260, name Arial, colour black; align: horiz center, vert center' % 'white')

        # Create sheet
        ws_PaymentHCM = wb.add_sheet('Payment')
        # Set col width
        ws_PaymentHCM.col(0).width = 2000
        for col in range(1,8):
            if col == 5:
                ws_PaymentHCM.col(col).width = 4000
            elif col == 6:
                ws_PaymentHCM.col(col).width = 4000 
            elif col == 7:
                ws_PaymentHCM.col(col).width = 30000 
            else:
                ws_PaymentHCM.col(col).width = 6000

        # Set row height
        ws_PaymentHCM.row(0).height_mismatch = True
        ws_PaymentHCM.row(0).height = 800
        ws_PaymentHCM.row(1).height_mismatch = True
        ws_PaymentHCM.row(1).height = 300
        ws_PaymentHCM.row(2).height_mismatch = True
        ws_PaymentHCM.row(2).height = 300
        ws_PaymentHCM.row(3).height_mismatch = True
        ws_PaymentHCM.row(3).height = 600
        ws_PaymentHCM.row(4).height_mismatch = True
        ws_PaymentHCM.row(4).height = 300
        # Head
        ws_PaymentHCM.write(0, 2, 'TEDIS REP. OFFICE IN HO CHI MINH', style_head_16pt_bold_vertcen)
        ws_PaymentHCM.write(1, 2, 'Room 2B, Floor 2 & 4 - 150 Nguyen Luong Bang, Tan Phu Ward, District 7', style_head_12pt_vertcen)
        ws_PaymentHCM.write_merge(3, 3, 0, 7, 'PAYMENT REPORT IN ' + str(period_month.month_name), style_head_20pt_bold)

        # Table
        # Table-head
        ws_PaymentHCM.write_merge(5, 6, 0, 0, 'No.', style_tablehead_grey25)
        ws_PaymentHCM.write_merge(5, 6, 1, 1, 'ITEM', style_tablehead_grey25)
        ws_PaymentHCM.write_merge(5, 6, 2, 2, 'DESCRIPTION', style_tablehead_grey25)
        ws_PaymentHCM.write_merge(5, 5, 3, 4, 'AMOUNT', style_tablehead_grey25)
        ws_PaymentHCM.write(6, 3, 'HCM (VND)', style_tablehead_grey25)
        ws_PaymentHCM.write(6, 4, 'HANOI (VND)', style_tablehead_grey25)
        ws_PaymentHCM.write_merge(5, 6, 5, 5, 'PAID BY', style_tablehead_grey25)
        ws_PaymentHCM.write_merge(5, 6, 6, 6, 'PAID TO', style_tablehead_grey25)
        ws_PaymentHCM.write_merge(5, 6, 7, 7, 'ACCOUNT NO.', style_tablehead_grey25)
        # Table-Body
        '''SALARY'''
        report_payment_payroll_SALARY = Report_Payment_Payroll_Tedis.objects.filter(month=period_month, item='SALARY').order_by('description')
        # Write NO. and ITEM column
        no_salary = report_payment_payroll_SALARY.count()
        ws_PaymentHCM.write_merge(7, 7+no_salary , 0, 0, '1', style_tablebody_vertcen_horizcen)
        ws_PaymentHCM.write_merge(7, 7+no_salary , 1, 1, 'SALARY', style_tablebody_vertcen_horizcen_bold)
        # Make subtotal var
        subtotal_salary_hcm = 0
        subtotal_salary_hanoi = 0
        for index, payment_data in enumerate(report_payment_payroll_SALARY):    
            # Set row height
            ws_PaymentHCM.row(7+index).height_mismatch = True
            ws_PaymentHCM.row(7+index).height = 800
            # Write data
            ws_PaymentHCM.write(7+index, 2, str(payment_data.description),style_tablebody_vertcen_horizleft)
            if payment_data.area == 'HCM':
                ws_PaymentHCM.write(7+index, 3, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(7+index, 4, '',style_tablebody_onlyvertcenter)
                # Make subtotal
                subtotal_salary_hcm += payment_data.amount
            elif payment_data.area == 'HANOI':
                ws_PaymentHCM.write(7+index, 3, '',style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(7+index, 4, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)    
                # Make subtotal
                subtotal_salary_hanoi += payment_data.amount
            ws_PaymentHCM.write(7+index, 5, str(payment_data.paidby),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(7+index, 6, str(payment_data.paidto),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(7+index, 7, str(payment_data.account_no),style_tablebody_vertcen_horizleft)
        # SUBTOTAL
        ws_PaymentHCM.write(7+no_salary, 2, 'SUBTOTAL',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(7+no_salary, 3, str("{:,}".format(round(subtotal_salary_hcm),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(7+no_salary, 4, str("{:,}".format(round(subtotal_salary_hanoi),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(7+no_salary, 5, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(7+no_salary, 6, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(7+no_salary, 7, '',style_tablebody_vertcen_horizleft_bold)
        last_row_salary = 7 + no_salary + 1
        '''SHUI'''
        report_payment_payroll_SHUI = Report_Payment_Payroll_Tedis.objects.filter(month=period_month, item='SHUI').order_by('-area')
        # Write NO. and ITEM column
        no_shui = report_payment_payroll_SHUI.count()
        ws_PaymentHCM.write_merge(last_row_salary, last_row_salary+no_shui , 0, 0, '2', style_tablebody_vertcen_horizcen)
        ws_PaymentHCM.write_merge(last_row_salary, last_row_salary+no_shui , 1, 1, 'SHUI', style_tablebody_vertcen_horizcen_bold)
        # Make subtotal var
        subtotal_shui_hcm = 0
        subtotal_shui_hanoi = 0
        for index, payment_data in enumerate(report_payment_payroll_SHUI):    
            # Set row height
            ws_PaymentHCM.row(last_row_salary+index).height_mismatch = True
            ws_PaymentHCM.row(last_row_salary+index).height = 800
            # Write data
            ws_PaymentHCM.write(last_row_salary+index, 2, str(payment_data.description),style_tablebody_vertcen_horizleft)
            if payment_data.area == 'HCM':
                ws_PaymentHCM.write(last_row_salary+index, 3, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(last_row_salary+index, 4, '',style_tablebody_onlyvertcenter)
                # Make subtotal
                subtotal_shui_hcm += payment_data.amount
            elif payment_data.area == 'HANOI':
                ws_PaymentHCM.write(last_row_salary+index, 3, '',style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(last_row_salary+index, 4, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)  
                # Make subtotal
                subtotal_shui_hanoi += payment_data.amount  
            ws_PaymentHCM.write(last_row_salary+index, 5, str(payment_data.paidby),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(last_row_salary+index, 6, str(payment_data.paidto),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(last_row_salary+index, 7, str(payment_data.account_no),style_tablebody_vertcen_horizleft)
        # SUBTOTAL
        ws_PaymentHCM.write(last_row_salary+no_shui, 2, 'SUBTOTAL',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_salary+no_shui, 3, str("{:,}".format(round(subtotal_shui_hcm),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_salary+no_shui, 4, str("{:,}".format(round(subtotal_shui_hanoi),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_salary+no_shui, 5, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_salary+no_shui, 6, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_salary+no_shui, 7, '',style_tablebody_vertcen_horizleft_bold)
        last_row_SHUI = last_row_salary + no_shui + 1
        '''PIT'''
        report_payment_payroll_PIT = Report_Payment_Payroll_Tedis.objects.filter(month=period_month, item='PIT').order_by('-area')
        # Write NO. and ITEM column
        no_pit = report_payment_payroll_PIT.count()
        ws_PaymentHCM.write_merge(last_row_SHUI, last_row_SHUI+no_pit , 0, 0, '3', style_tablebody_vertcen_horizcen)
        ws_PaymentHCM.write_merge(last_row_SHUI, last_row_SHUI+no_pit , 1, 1, 'PIT', style_tablebody_vertcen_horizcen_bold)
        # Make subtotal var
        subtotal_pit_hcm = 0
        subtotal_pit_hanoi = 0
        for index, payment_data in enumerate(report_payment_payroll_PIT):    
            # Set row height
            ws_PaymentHCM.row(last_row_SHUI+index).height_mismatch = True
            ws_PaymentHCM.row(last_row_SHUI+index).height = 800
            # Write data
            ws_PaymentHCM.write(last_row_SHUI+index, 2, str(payment_data.description),style_tablebody_vertcen_horizleft)
            if payment_data.area == 'HCM':
                ws_PaymentHCM.write(last_row_SHUI+index, 3, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(last_row_SHUI+index, 4, '',style_tablebody_onlyvertcenter)
                # Make subtotal
                subtotal_pit_hcm += payment_data.amount
            elif payment_data.area == 'HANOI':
                ws_PaymentHCM.write(last_row_SHUI+index, 3, '',style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(last_row_SHUI+index, 4, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)  
                # Make subtotal
                subtotal_pit_hanoi += payment_data.amount  
            ws_PaymentHCM.write(last_row_SHUI+index, 5, str(payment_data.paidby),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(last_row_SHUI+index, 6, str(payment_data.paidto),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(last_row_SHUI+index, 7, str(payment_data.account_no),style_tablebody_vertcen_horizleft)
        # SUBTOTAL
        ws_PaymentHCM.write(last_row_SHUI+no_pit, 2, 'SUBTOTAL',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_SHUI+no_pit, 3, str("{:,}".format(round(subtotal_pit_hcm),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_SHUI+no_pit, 4, str("{:,}".format(round(subtotal_pit_hanoi),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_SHUI+no_pit, 5, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_SHUI+no_pit, 6, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_SHUI+no_pit, 7, '',style_tablebody_vertcen_horizleft_bold)
        last_row_pit = last_row_SHUI + no_pit + 1
        '''Trade union'''
        report_payment_payroll_TRADE_UNION = Report_Payment_Payroll_Tedis.objects.filter(month=period_month, item='TRADE UNION').order_by('-area')
        # Write NO. and ITEM column
        no_trade_union = report_payment_payroll_TRADE_UNION.count()
        ws_PaymentHCM.write_merge(last_row_pit, last_row_pit+no_trade_union , 0, 0, '4', style_tablebody_vertcen_horizcen)
        ws_PaymentHCM.write_merge(last_row_pit, last_row_pit+no_trade_union , 1, 1, 'TRADE UNION', style_tablebody_vertcen_horizcen_bold)
        # Make subtotal var
        subtotal_trade_union_hcm = 0
        subtotal_trade_union_hanoi = 0
        for index, payment_data in enumerate(report_payment_payroll_TRADE_UNION):    
            # Set row height
            ws_PaymentHCM.row(last_row_pit+index).height_mismatch = True
            ws_PaymentHCM.row(last_row_pit+index).height = 800
            # Write data
            ws_PaymentHCM.write(last_row_pit+index, 2, str(payment_data.description),style_tablebody_vertcen_horizleft)
            if payment_data.area == 'HCM':
                ws_PaymentHCM.write(last_row_pit+index, 3, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(last_row_pit+index, 4, '',style_tablebody_onlyvertcenter)
                # Make subtotal
                subtotal_trade_union_hcm += payment_data.amount
            elif payment_data.area == 'HANOI':
                ws_PaymentHCM.write(last_row_pit+index, 3, '',style_tablebody_onlyvertcenter)
                ws_PaymentHCM.write(last_row_pit+index, 4, str("{:,}".format(round(payment_data.amount),0)),style_tablebody_onlyvertcenter)  
                # Make subtotal
                subtotal_trade_union_hanoi += payment_data.amount  
            ws_PaymentHCM.write(last_row_pit+index, 5, str(payment_data.paidby),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(last_row_pit+index, 6, str(payment_data.paidto),style_tablebody_vertcen_horizleft)
            ws_PaymentHCM.write(last_row_pit+index, 7, str(payment_data.account_no),style_tablebody_vertcen_horizleft)
        # SUBTOTAL
        ws_PaymentHCM.write(last_row_pit+no_trade_union, 2, 'SUBTOTAL',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_pit+no_trade_union, 3, str("{:,}".format(round(subtotal_trade_union_hcm),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_pit+no_trade_union, 4, str("{:,}".format(round(subtotal_trade_union_hanoi),0)),style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_pit+no_trade_union, 5, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_pit+no_trade_union, 6, '',style_tablebody_vertcen_horizleft_bold)
        ws_PaymentHCM.write(last_row_pit+no_trade_union, 7, '',style_tablebody_vertcen_horizleft_bold)
        last_row_trade_union = last_row_pit + no_trade_union + 1
        '''TOTAL COST BY SITE'''
        # Make total var
        total_cost_hcm = subtotal_salary_hcm + subtotal_shui_hcm + subtotal_pit_hcm + subtotal_trade_union_hcm
        total_cost_hanoi = subtotal_salary_hanoi + subtotal_shui_hanoi + subtotal_pit_hanoi + subtotal_trade_union_hanoi
        # Set row height
        ws_PaymentHCM.row(last_row_trade_union).height_mismatch = True
        ws_PaymentHCM.row(last_row_trade_union).height = 650
        # Write data
        ws_PaymentHCM.write_merge(last_row_trade_union, last_row_trade_union , 0, 2, 'TOTAL COST BY SITE', style_tablehead_grey25) 
        ws_PaymentHCM.write(last_row_trade_union, 3, str("{:,}".format(round(total_cost_hcm),0)),style_tablehead_grey25) 
        ws_PaymentHCM.write(last_row_trade_union, 4, str("{:,}".format(round(total_cost_hanoi),0)),style_tablehead_grey25)
        ws_PaymentHCM.write_merge(last_row_trade_union, last_row_trade_union , 5, 7, '', style_tablehead_grey25)
        '''TOTAL'''
        # Make total var
        total = total_cost_hcm + total_cost_hanoi
        # Set row height
        ws_PaymentHCM.row(last_row_trade_union + 1).height_mismatch = True
        ws_PaymentHCM.row(last_row_trade_union + 1).height = 650
        # Write data
        ws_PaymentHCM.write_merge(last_row_trade_union + 1, last_row_trade_union + 1 , 0, 2, 'TOTAL', style_tablehead_grey25) 
        ws_PaymentHCM.write_merge(last_row_trade_union + 1, last_row_trade_union + 1 , 3, 4, str("{:,}".format(round(total),0)), style_tablehead_grey25) 
        ws_PaymentHCM.write_merge(last_row_trade_union + 1, last_row_trade_union + 1 , 5, 7, '', style_tablehead_grey25)               
        
        # Footer
        # Set row height
        ws_PaymentHCM.row(last_row_trade_union + 2).height_mismatch = True
        ws_PaymentHCM.row(last_row_trade_union + 2).height = 650
        ws_PaymentHCM.row(last_row_trade_union + 3).height_mismatch = True
        ws_PaymentHCM.row(last_row_trade_union + 3).height = 650
        ws_PaymentHCM.row(last_row_trade_union + 4).height_mismatch = True
        ws_PaymentHCM.row(last_row_trade_union + 4).height = 1500
        # Write data
        ws_PaymentHCM.write_merge(last_row_trade_union + 3, last_row_trade_union + 3 , 1, 2, 'Reviewed by', style_footer)  
        ws_PaymentHCM.write(last_row_trade_union + 3, 7, 'Verified by', style_footer)
        ws_PaymentHCM.write_merge(last_row_trade_union + 5, last_row_trade_union + 5 , 1, 2, 'Le Thi Thanh Tuyen', style_footer)  
        ws_PaymentHCM.write(last_row_trade_union + 5, 7, 'Vu Chau Kim Anh', style_footer)
        ws_PaymentHCM.write_merge(last_row_trade_union + 6, last_row_trade_union + 6 , 1, 2, datetime.now().strftime('%d/%m/%Y'), style_date)  
        ws_PaymentHCM.write(last_row_trade_union + 6, 7, datetime.now().strftime('%d/%m/%Y'), style_date)      
            

        wb.save(response)
        return response
        
        
        
    
    return render(request, 'employee/view_report_payroll_tedis.html', {
        'period_month' : period_month,
        'report_payrollExist' : report_payrollExist,
        'report_pit_payroll' : report_pit_payroll,
        'report_transfer_payroll' : report_transfer_payroll,
        'report_payment_payroll' : report_payment_payroll,
        
    })



def PIT_report_payroll_tedis_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    pit_info = Report_PIT_Payroll_Tedis.objects.get(pk=pk)
    
    
    # Update payroll info
    if request.POST.get('btnupdatepit'):
        thuong = request.POST.get('thuong')
        khac = request.POST.get('khac')
        cong = request.POST.get('cong')
        ghi_chu = request.POST.get('ghi_chu')
        # Get unchange data
        month = pit_info.month
        payroll = pit_info.payroll
        employee = pit_info.employee
        
        thu_nhap_chiu_thue = pit_info.thu_nhap_chiu_thue
        tong_tnct_khau_tru_thue = pit_info.tong_tnct_khau_tru_thue
        bao_hiem_bat_buoc = pit_info.bao_hiem_bat_buoc
        khau_tru = pit_info.khau_tru
        
        thu_nhap_tinh_thue = pit_info.thu_nhap_tinh_thue
        
        thue_tnct_phai_nop = pit_info.thue_tnct_phai_nop
        
        
        # Update and save
        pit_update_info = Report_PIT_Payroll_Tedis(id=pit_info.id,thuong=thuong,khac=khac,cong=cong,ghi_chu=ghi_chu,
                                                   month=month,payroll=payroll,employee=employee,
                                                   thu_nhap_chiu_thue=thu_nhap_chiu_thue,tong_tnct_khau_tru_thue=tong_tnct_khau_tru_thue,bao_hiem_bat_buoc=bao_hiem_bat_buoc,khau_tru=khau_tru,
                                                   thu_nhap_tinh_thue=thu_nhap_tinh_thue,
                                                   thue_tnct_phai_nop=thue_tnct_phai_nop)
        pit_update_info.save()
        messages.success(request, 'SUCCESS: PIT updated')
        return redirect('employee:PIT_report_payroll_tedis_edit',pk=pit_info.id)
        
        
        
    
    return render(request, 'employee/edit_PIT_report_payroll_tedis.html', {
        'pit_info' : pit_info,
        
    })


def payment_report_payroll_tedis_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    payment_info = Report_Payment_Payroll_Tedis.objects.get(pk=pk)
    
    # Create lists
    list_items = ['---','SALARY','SHUI','PIT','TRADE UNION']
    list_descriptions = ['---','EMPLOYEES','MARJORIE','SHUI Company','SHUI Employees','PIT','PIT Ms. MARJORIE',
                         'Trade Union fee','Trade Union (member fee)']
    list_areas = ['---','HCM','HANOI']
    list_paidbys = ['---','Transfer','Cash']
    
    # Update payroll info
    if request.POST.get('btnupdatepayment'):
        month = payment_info.month
        item = request.POST.get('item')
        description = request.POST.get('description')
        area = request.POST.get('area')
        amount = request.POST.get('amount')
        paidby = request.POST.get('paidby')
        paidto = request.POST.get('paidto')
        account_no = request.POST.get('account_no')
    
        # Update and save
        payment_update_info = Report_Payment_Payroll_Tedis(id=payment_info.id,month=month,
                                                   item=item,description=description,area=area,
                                                   amount=amount,paidby=paidby,paidto=paidto,
                                                   account_no=account_no)
        payment_update_info.save()
        messages.success(request, 'SUCCESS: Payment updated')
        return redirect('employee:payment_report_payroll_tedis_edit',pk=payment_info.id)
        
        
        
    
    return render(request, 'employee/edit_payment_report_payroll_tedis.html', {
        'payment_info' : payment_info,
        'list_items' : list_items,
        'list_descriptions' : list_descriptions,
        'list_areas' : list_areas,
        'list_paidbys' : list_paidbys,
        
    })

def payment_report_payroll_tedis_delete(request, pk):
    try:
        payment_info = Report_Payment_Payroll_Tedis.objects.get(id = pk)
        payment_info.delete()
        messages.success(request, 'SUCCESS: Payment deleted')
    except Report_Payment_Payroll_Tedis.DoesNotExist:
        messages.error(request, 'Error: Please try again')
    return redirect('employee:report_payroll_tedis',pk=payment_info.month.id)
    


def report_payroll_tedis_vietha(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    try:
        last_period_month = Month_in_period.objects.get(pk=pk-1)
        # Get start date of previous month
        start_date = datetime(last_period_month.period.period_year, last_period_month.month_number, 1)
    except Month_in_period.DoesNotExist:
        last_period_month = ''
        # Get start date of previous month
        start_date = datetime(period_month.period.period_year, period_month.month_number, 1)


    # Get end date of present month
    if period_month.month_number == 12:
        end_date = datetime(period_month.period.period_year + 1, 1, 1)
    else:
        end_date = datetime(period_month.period.period_year, period_month.month_number + 1, 1)

    # Trừ đi 1 ngày để lấy ngày cuối cùng của tháng hiện tại
    end_date = end_date - timedelta(days=1)
    
    # Get report data
    site_JV = Site.objects.get(site='JV')
    list_employee_tedis_vietha = Employee.objects.filter(site=site_JV,active=1)
    list_employee_tedis_vietha_include_inactive = Employee.objects.filter(Q(site=site_JV) & (Q(out_date__range=(start_date, end_date)) | Q(out_date=None)))
    # PIT
    report_pit_payroll = Report_PIT_Payroll_Tedis_VietHa.objects.filter(month=period_month,individual_type='')
    report_pit_payroll_canhancutru = Report_PIT_Payroll_Tedis_VietHa.objects.filter(month=period_month,individual_type='Cá Nhân Cư Trú')
    report_pit_payroll_canhankhongcutru = Report_PIT_Payroll_Tedis_VietHa.objects.filter(month=period_month,individual_type='Cá Nhân Không Cư Trú')
    if report_pit_payroll.count() > 0:
        report_payrollExist = 1
    else:
        report_pit_payroll = ''
        report_payrollExist = 0    
    # Transfer 
    report_transfer_payroll = Report_Transfer_Payroll_Tedis_VietHa.objects.filter(month=period_month)
    report_transferStaff_payroll = Report_Transfer_Payroll_Tedis_VietHa.objects.filter(month=period_month,employee_type='STAFF')
    report_transferColl_payroll = Report_Transfer_Payroll_Tedis_VietHa.objects.filter(month=period_month,employee_type='COLL')
    if report_transfer_payroll.count() > 0:
        report_payrollExist = 1
    else:
        report_transfer_payroll = ''
        report_payrollExist = 0 
    # Payroll
    # Get staff and coll employee:
    list_staff = []
    list_coll = []
    contact_category_CTV = Contract_category.objects.get(contract_category='CTV')
    for employee in list_employee_tedis_vietha_include_inactive:
        list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at') 
        if list_contracts[0].contract_category == contact_category_CTV:   
            # Make data    
            data = {
                'employee': employee
            }
            list_coll.append(data)
        else:
            # Make data    
            data = {
                'employee': list_contracts[0].employee
            }
            list_staff.append(data)
            
    # Get Working day of BO and Working day of WH
    working_day_bo = period_month.total_work_days_bo
    working_day_wh = period_month.total_work_days_wh
    # Get payroll
    list_payroll_staff_info = []
    for data in list_staff:
        payroll_info = Payroll_Tedis_Vietha.objects.get(employee=data['employee'].id,month=period_month)
        payroll_data = {
                'payroll_info': payroll_info,
            }
        list_payroll_staff_info.append(payroll_data)
    list_payroll_coll_info = []
    for data in list_coll:
        payroll_info = Payroll_Tedis_Vietha.objects.get(employee=data['employee'].id,month=period_month)
        payroll_data = {
                'payroll_info': payroll_info,
            }
        list_payroll_coll_info.append(payroll_data)
    # Get payroll SER
    try:
        payroll_ser = Payroll_Ser.objects.get(month=period_month)
        report_payrollExist = 1 
    except Payroll_Ser.DoesNotExist:
        payroll_ser = ''
        report_payrollExist = 0    
        
    # Payment
    item_order = {'SALARY': 1, 'SALARY + ALLOWANCE' : 2,'SHUI': 3, 'PIT': 4, 'TRADE UNION': 5}
    report_payment_payroll = Report_Payment_Payroll_Tedis_VietHa.objects.filter(month=period_month).order_by(Case(*[When(item=item, then=Value(order)) for item, order in item_order.items()], default=Value(999)))
    if report_payment_payroll.count() > 0:
        report_payrollExist = 1
    else:
        report_payment_payroll = ''
        report_payrollExist = 0 
    
    '''Infor.Payroll'''
    # New Staff
    new_staff_reports = Report_new_staff_Tedis_VietHa.objects.filter(month=period_month)
    # Confirmed after probation
    confirmed_after_probation_reports = Report_confirmed_after_probation_Tedis_VietHa.objects.filter(month=period_month)
    # Resigned staff
    resigned_staff_reports = Report_resigned_staff_Tedis_VietHa.objects.filter(month=period_month)
    # Other changes
    other_changes_reports = Report_other_changes_Tedis_VietHa.objects.filter(month=period_month)
    # Maternity leave
    maternity_leave_reports = Report_maternity_leave_Tedis_VietHa.objects.filter(month=period_month)
    
    '''reconcile'''
    try:
        last_period_month = Month_in_period.objects.get(pk=pk-1)
        # Get staff and coll employee:
        list_staff = []
        list_collaborator = []
        contact_category_CTV = Contract_category.objects.get(contract_category='CTV')
        for employee in list_employee_tedis_vietha_include_inactive:
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at') 
            if list_contracts[0].contract_category == contact_category_CTV: 
                list_collaborator.append(employee.id)  
            else:
                list_staff.append(list_contracts[0].employee.id)
        
                
        # Last month staff
        list_last_month_payroll_staff = Payroll_Tedis_Vietha.objects.filter(employee__in=list_staff,month=pk-1)
        # Define total_var
        total_head_count = list_last_month_payroll_staff.count()
        total_gross_income = 0
        total_transportation = 0
        total_phone = 0
        total_lunch = 0
        total_outstanding_annual_leave = 0
        total_responsibility = 0
        total_travel = 0
        total_seniority_bonus = 0
        total_other = 0
        total_OTC_incentive = 0
        total_KPI_achievement = 0
        total_incentive_last_month = 0
        total_month_13_salary_Pro_ata = 0
        total_incentive_last_quy_last_year = 0
        total_taxable_overtime = 0
        total_nontaxable_overtime = 0
        total_SHUI_10point5percent_employee_pay = 0
        total_SHUI_21point5percent_company_pay = 0
        total_occupational_accident_and_disease = 0
        total_trade_union_fee_company_pay = 0
        total_trade_union_fee_employee_pay = 0
        total_family_deduction = 0
        total_taxable_income = 0
        total_taxed_income = 0
        total_PIT = 0
        total_net_income = 0
        total_total_cost = 0
        # Get total_var += payroll.
        for payroll in list_last_month_payroll_staff:
            total_gross_income += round(payroll.gross_income)
            total_transportation += round(payroll.transportation)
            total_phone += round(payroll.phone)
            total_lunch += round(payroll.lunch)
            total_outstanding_annual_leave += round(payroll.outstanding_annual_leave)
            total_responsibility += round(payroll.responsibility)
            total_travel += round(payroll.travel)
            total_seniority_bonus += round(payroll.seniority_bonus)
            total_other += round(payroll.other)
            total_OTC_incentive += round(payroll.OTC_incentive)
            total_KPI_achievement += round(payroll.KPI_achievement)
            total_incentive_last_month += round(payroll.incentive_last_month)
            total_month_13_salary_Pro_ata += round(payroll.month_13_salary_Pro_ata)
            total_incentive_last_quy_last_year += round(payroll.incentive_last_quy_last_year)
            total_taxable_overtime += round(payroll.taxable_overtime)
            total_nontaxable_overtime += round(payroll.nontaxable_overtime)
            total_SHUI_10point5percent_employee_pay += round(payroll.SHUI_10point5percent_employee_pay)
            total_SHUI_21point5percent_company_pay += round(payroll.SHUI_21point5percent_company_pay)
            total_occupational_accident_and_disease += round(payroll.occupational_accident_and_disease)
            total_trade_union_fee_company_pay += round(payroll.trade_union_fee_company_pay)
            total_trade_union_fee_employee_pay += round(payroll.trade_union_fee_employee_pay)
            total_family_deduction += round(payroll.family_deduction)
            total_taxable_income += round(payroll.taxable_income)
            total_taxed_income += round(payroll.taxed_income)
            total_PIT += round(payroll.PIT)
            total_net_income += round(payroll.net_income)
            total_total_cost += round(payroll.total_cost)
        # Make data
        payroll_staff_last_month = {
            'head_count' : total_head_count,
            'gross_income' : total_gross_income,
            'transportation' : total_transportation,
            'phone' : total_phone,
            'lunch' : total_lunch,
            'outstanding_annual_leave' : total_outstanding_annual_leave,
            'responsibility' : total_responsibility,
            'travel' : total_travel,
            'seniority_bonus' : total_seniority_bonus,
            'other' : total_other,
            'OTC_incentive' : total_OTC_incentive,
            'KPI_achievement' : total_KPI_achievement,
            'incentive_last_month' : total_incentive_last_month,
            'month_13_salary_Pro_ata' : total_month_13_salary_Pro_ata,
            'incentive_last_quy_last_year' : total_incentive_last_quy_last_year,
            'taxable_overtime' : total_taxable_overtime,
            'nontaxable_overtime' : total_nontaxable_overtime,
            'SHUI_10point5percent_employee_pay' : total_SHUI_10point5percent_employee_pay,
            'SHUI_21point5percent_company_pay' : total_SHUI_21point5percent_company_pay,
            'occupational_accident_and_disease' : total_occupational_accident_and_disease,
            'trade_union_fee_company_pay' : total_trade_union_fee_company_pay,
            'trade_union_fee_employee_pay' : total_trade_union_fee_employee_pay,
            'family_deduction' : total_family_deduction,
            'taxable_income' : total_taxable_income,
            'taxed_income' : total_taxed_income,
            'PIT' : total_PIT,
            'net_income' : total_net_income,
            'total_cost' : total_total_cost
        }
        
        # Last month coll
        list_last_month_payroll_coll = Payroll_Tedis_Vietha.objects.filter(employee__in=list_collaborator,month=pk-1)
        # Define total_var
        total_head_count = list_last_month_payroll_coll.count()
        total_gross_income = 0
        total_transportation = 0
        total_phone = 0
        total_lunch = 0
        total_outstanding_annual_leave = 0
        total_responsibility = 0
        total_travel = 0
        total_seniority_bonus = 0
        total_other = 0
        total_OTC_incentive = 0
        total_KPI_achievement = 0
        total_incentive_last_month = 0
        total_month_13_salary_Pro_ata = 0
        total_incentive_last_quy_last_year = 0
        total_taxable_overtime = 0
        total_nontaxable_overtime = 0
        total_SHUI_10point5percent_employee_pay = 0
        total_SHUI_21point5percent_company_pay = 0
        total_occupational_accident_and_disease = 0
        total_trade_union_fee_company_pay = 0
        total_trade_union_fee_employee_pay = 0
        total_family_deduction = 0
        total_taxable_income = 0
        total_taxed_income = 0
        total_PIT = 0
        total_net_income = 0
        total_total_cost = 0
        # Get total_var += payroll.
        for payroll in list_last_month_payroll_coll:
            total_gross_income += round(payroll.gross_income)
            total_transportation += round(payroll.transportation)
            total_phone += round(payroll.phone)
            total_lunch += round(payroll.lunch)
            total_outstanding_annual_leave += round(payroll.outstanding_annual_leave)
            total_responsibility += round(payroll.responsibility)
            total_travel += round(payroll.travel)
            total_seniority_bonus += round(payroll.seniority_bonus)
            total_other += round(payroll.other)
            total_OTC_incentive += round(payroll.OTC_incentive)
            total_KPI_achievement += round(payroll.KPI_achievement)
            total_incentive_last_month += round(payroll.incentive_last_month)
            total_month_13_salary_Pro_ata += round(payroll.month_13_salary_Pro_ata)
            total_incentive_last_quy_last_year += round(payroll.incentive_last_quy_last_year)
            total_taxable_overtime += round(payroll.taxable_overtime)
            total_nontaxable_overtime += round(payroll.nontaxable_overtime)
            total_SHUI_10point5percent_employee_pay += round(payroll.SHUI_10point5percent_employee_pay)
            total_SHUI_21point5percent_company_pay += round(payroll.SHUI_21point5percent_company_pay)
            total_occupational_accident_and_disease += round(payroll.occupational_accident_and_disease)
            total_trade_union_fee_company_pay += round(payroll.trade_union_fee_company_pay)
            total_trade_union_fee_employee_pay += round(payroll.trade_union_fee_employee_pay)
            total_family_deduction += round(payroll.family_deduction)
            total_taxable_income += round(payroll.taxable_income)
            total_taxed_income += round(payroll.taxed_income)
            total_PIT += round(payroll.PIT)
            total_net_income += round(payroll.net_income)
            total_total_cost += round(payroll.total_cost)
        # Make data
        payroll_coll_last_month = {
            'head_count' : total_head_count,
            'gross_income' : total_gross_income,
            'transportation' : total_transportation,
            'phone' : total_phone,
            'lunch' : total_lunch,
            'outstanding_annual_leave' : total_outstanding_annual_leave,
            'responsibility' : total_responsibility,
            'travel' : total_travel,
            'seniority_bonus' : total_seniority_bonus,
            'other' : total_other,
            'OTC_incentive' : total_OTC_incentive,
            'KPI_achievement' : total_KPI_achievement,
            'incentive_last_month' : total_incentive_last_month,
            'month_13_salary_Pro_ata' : total_month_13_salary_Pro_ata,
            'incentive_last_quy_last_year' : total_incentive_last_quy_last_year,
            'taxable_overtime' : total_taxable_overtime,
            'nontaxable_overtime' : total_nontaxable_overtime,
            'SHUI_10point5percent_employee_pay' : total_SHUI_10point5percent_employee_pay,
            'SHUI_21point5percent_company_pay' : total_SHUI_21point5percent_company_pay,
            'occupational_accident_and_disease' : total_occupational_accident_and_disease,
            'trade_union_fee_company_pay' : total_trade_union_fee_company_pay,
            'trade_union_fee_employee_pay' : total_trade_union_fee_employee_pay,
            'family_deduction' : total_family_deduction,
            'taxable_income' : total_taxable_income,
            'taxed_income' : total_taxed_income,
            'PIT' : total_PIT,
            'net_income' : total_net_income,
            'total_cost' : total_total_cost
        }
        
        # Last month ser
        try:
            last_month_payroll_ser = Payroll_Ser.objects.get(month=pk-1)
            # Make data
            payroll_ser_last_month = {
            'employee' : last_month_payroll_ser.employee,
            'head_count' : 1,
            'gross_income' : round(last_month_payroll_ser.gross_income) + round(last_month_payroll_ser.housing_vnd),
            'SHUI_21point5percent_company_pay' : round(last_month_payroll_ser.SHUI_9point5percent_employee_pay) + round(last_month_payroll_ser.SHUI_20point5percent_employer_pay),
            'trade_union_fee_company_pay' : round(last_month_payroll_ser.trade_union_fee_company_pay),
            'PIT' : round(last_month_payroll_ser.PIT),
            'net_income' : round(last_month_payroll_ser.net_income * last_month_payroll_ser.exchange_rate_euro),
            'total_cost' : round(last_month_payroll_ser.total_cost_vnd)
        }  
        except Payroll_Ser.DoesNotExist:
            payroll_ser_last_month = {
            'head_count' : 0,
            'gross_income' : 0,
            'SHUI_21point5percent_company_pay' : 0,
            'trade_union_fee_company_pay' : 0,
            'PIT' : 0,
            'net_income' : 0,
            'total_cost' : 0
            }
        
        
        # This month staff
        list_this_month_payroll_staff = Payroll_Tedis_Vietha.objects.filter(employee__in=list_staff,month=pk)
        # Define total_var
        total_head_count = list_this_month_payroll_staff.count()
        total_gross_income = 0
        total_transportation = 0
        total_phone = 0
        total_lunch = 0
        total_outstanding_annual_leave = 0
        total_responsibility = 0
        total_travel = 0
        total_seniority_bonus = 0
        total_other = 0
        total_OTC_incentive = 0
        total_KPI_achievement = 0
        total_incentive_last_month = 0
        total_month_13_salary_Pro_ata = 0
        total_incentive_last_quy_last_year = 0
        total_taxable_overtime = 0
        total_nontaxable_overtime = 0
        total_SHUI_10point5percent_employee_pay = 0
        total_SHUI_21point5percent_company_pay = 0
        total_occupational_accident_and_disease = 0
        total_trade_union_fee_company_pay = 0
        total_trade_union_fee_employee_pay = 0
        total_family_deduction = 0
        total_taxable_income = 0
        total_taxed_income = 0
        total_PIT = 0
        total_net_income = 0
        total_total_cost = 0
        # Get total_var += payroll.
        for payroll in list_this_month_payroll_staff:
            total_gross_income += round(payroll.gross_income)
            total_transportation += round(payroll.transportation)
            total_phone += round(payroll.phone)
            total_lunch += round(payroll.lunch)
            total_outstanding_annual_leave += round(payroll.outstanding_annual_leave)
            total_responsibility += round(payroll.responsibility)
            total_travel += round(payroll.travel)
            total_seniority_bonus += round(payroll.seniority_bonus)
            total_other += round(payroll.other)
            total_OTC_incentive += round(payroll.OTC_incentive)
            total_KPI_achievement += round(payroll.KPI_achievement)
            total_incentive_last_month += round(payroll.incentive_last_month)
            total_month_13_salary_Pro_ata += round(payroll.month_13_salary_Pro_ata)
            total_incentive_last_quy_last_year += round(payroll.incentive_last_quy_last_year)
            total_taxable_overtime += round(payroll.taxable_overtime)
            total_nontaxable_overtime += round(payroll.nontaxable_overtime)
            total_SHUI_10point5percent_employee_pay += round(payroll.SHUI_10point5percent_employee_pay)
            total_SHUI_21point5percent_company_pay += round(payroll.SHUI_21point5percent_company_pay)
            total_occupational_accident_and_disease += round(payroll.occupational_accident_and_disease)
            total_trade_union_fee_company_pay += round(payroll.trade_union_fee_company_pay)
            total_trade_union_fee_employee_pay += round(payroll.trade_union_fee_employee_pay)
            total_family_deduction += round(payroll.family_deduction)
            total_taxable_income += round(payroll.taxable_income)
            total_taxed_income += round(payroll.taxed_income)
            total_PIT += round(payroll.PIT)
            total_net_income += round(payroll.net_income)
            total_total_cost += round(payroll.total_cost)
        # Make data
        payroll_staff_this_month = {
            'head_count' : total_head_count,
            'gross_income' : total_gross_income,
            'transportation' : total_transportation,
            'phone' : total_phone,
            'lunch' : total_lunch,
            'outstanding_annual_leave' : total_outstanding_annual_leave,
            'responsibility' : total_responsibility,
            'travel' : total_travel,
            'seniority_bonus' : total_seniority_bonus,
            'other' : total_other,
            'OTC_incentive' : total_OTC_incentive,
            'KPI_achievement' : total_KPI_achievement,
            'incentive_last_month' : total_incentive_last_month,
            'month_13_salary_Pro_ata' : total_month_13_salary_Pro_ata,
            'incentive_last_quy_last_year' : total_incentive_last_quy_last_year,
            'taxable_overtime' : total_taxable_overtime,
            'nontaxable_overtime' : total_nontaxable_overtime,
            'SHUI_10point5percent_employee_pay' : total_SHUI_10point5percent_employee_pay,
            'SHUI_21point5percent_company_pay' : total_SHUI_21point5percent_company_pay,
            'occupational_accident_and_disease' : total_occupational_accident_and_disease,
            'trade_union_fee_company_pay' : total_trade_union_fee_company_pay,
            'trade_union_fee_employee_pay' : total_trade_union_fee_employee_pay,
            'family_deduction' : total_family_deduction,
            'taxable_income' : total_taxable_income,
            'taxed_income' : total_taxed_income,
            'PIT' : total_PIT,
            'net_income' : total_net_income,
            'total_cost' : total_total_cost
        }
        
        # This month coll
        list_this_month_payroll_coll = Payroll_Tedis_Vietha.objects.filter(employee__in=list_collaborator,month=pk)
        # Define total_var
        total_head_count = list_this_month_payroll_coll.count()
        total_gross_income = 0
        total_transportation = 0
        total_phone = 0
        total_lunch = 0
        total_outstanding_annual_leave = 0
        total_responsibility = 0
        total_travel = 0
        total_seniority_bonus = 0
        total_other = 0
        total_OTC_incentive = 0
        total_KPI_achievement = 0
        total_incentive_last_month = 0
        total_month_13_salary_Pro_ata = 0
        total_incentive_last_quy_last_year = 0
        total_taxable_overtime = 0
        total_nontaxable_overtime = 0
        total_SHUI_10point5percent_employee_pay = 0
        total_SHUI_21point5percent_company_pay = 0
        total_occupational_accident_and_disease = 0
        total_trade_union_fee_company_pay = 0
        total_trade_union_fee_employee_pay = 0
        total_family_deduction = 0
        total_taxable_income = 0
        total_taxed_income = 0
        total_PIT = 0
        total_net_income = 0
        total_total_cost = 0
        # Get total_var += payroll.
        for payroll in list_this_month_payroll_coll:
            total_gross_income += round(payroll.gross_income)
            total_transportation += round(payroll.transportation)
            total_phone += round(payroll.phone)
            total_lunch += round(payroll.lunch)
            total_outstanding_annual_leave += round(payroll.outstanding_annual_leave)
            total_responsibility += round(payroll.responsibility)
            total_travel += round(payroll.travel)
            total_seniority_bonus += round(payroll.seniority_bonus)
            total_other += round(payroll.other)
            total_OTC_incentive += round(payroll.OTC_incentive)
            total_KPI_achievement += round(payroll.KPI_achievement)
            total_incentive_last_month += round(payroll.incentive_last_month)
            total_month_13_salary_Pro_ata += round(payroll.month_13_salary_Pro_ata)
            total_incentive_last_quy_last_year += round(payroll.incentive_last_quy_last_year)
            total_taxable_overtime += round(payroll.taxable_overtime)
            total_nontaxable_overtime += round(payroll.nontaxable_overtime)
            total_SHUI_10point5percent_employee_pay += round(payroll.SHUI_10point5percent_employee_pay)
            total_SHUI_21point5percent_company_pay += round(payroll.SHUI_21point5percent_company_pay)
            total_occupational_accident_and_disease += round(payroll.occupational_accident_and_disease)
            total_trade_union_fee_company_pay += round(payroll.trade_union_fee_company_pay)
            total_trade_union_fee_employee_pay += round(payroll.trade_union_fee_employee_pay)
            total_family_deduction += round(payroll.family_deduction)
            total_taxable_income += round(payroll.taxable_income)
            total_taxed_income += round(payroll.taxed_income)
            total_PIT += round(payroll.PIT)
            total_net_income += round(payroll.net_income)
            total_total_cost += round(payroll.total_cost)
        # Make data
        payroll_coll_this_month = {
            'head_count' : total_head_count,
            'gross_income' : total_gross_income,
            'transportation' : total_transportation,
            'phone' : total_phone,
            'lunch' : total_lunch,
            'outstanding_annual_leave' : total_outstanding_annual_leave,
            'responsibility' : total_responsibility,
            'travel' : total_travel,
            'seniority_bonus' : total_seniority_bonus,
            'other' : total_other,
            'OTC_incentive' : total_OTC_incentive,
            'KPI_achievement' : total_KPI_achievement,
            'incentive_last_month' : total_incentive_last_month,
            'month_13_salary_Pro_ata' : total_month_13_salary_Pro_ata,
            'incentive_last_quy_last_year' : total_incentive_last_quy_last_year,
            'taxable_overtime' : total_taxable_overtime,
            'nontaxable_overtime' : total_nontaxable_overtime,
            'SHUI_10point5percent_employee_pay' : total_SHUI_10point5percent_employee_pay,
            'SHUI_21point5percent_company_pay' : total_SHUI_21point5percent_company_pay,
            'occupational_accident_and_disease' : total_occupational_accident_and_disease,
            'trade_union_fee_company_pay' : total_trade_union_fee_company_pay,
            'trade_union_fee_employee_pay' : total_trade_union_fee_employee_pay,
            'family_deduction' : total_family_deduction,
            'taxable_income' : total_taxable_income,
            'taxed_income' : total_taxed_income,
            'PIT' : total_PIT,
            'net_income' : total_net_income,
            'total_cost' : total_total_cost
        }
        
        # This month ser
        try:
            this_month_payroll_ser = Payroll_Ser.objects.get(month=pk)
            # Make data
            payroll_ser_this_month = {
            'employee' : this_month_payroll_ser.employee,
            'head_count' : 1,
            'gross_income' : round(this_month_payroll_ser.gross_income) + round(this_month_payroll_ser.housing_vnd),
            'SHUI_21point5percent_company_pay' : round(this_month_payroll_ser.SHUI_9point5percent_employee_pay) + round(this_month_payroll_ser.SHUI_20point5percent_employer_pay),
            'trade_union_fee_company_pay' : round(this_month_payroll_ser.trade_union_fee_company_pay),
            'PIT' : round(this_month_payroll_ser.PIT),
            'net_income' : round(this_month_payroll_ser.net_income * this_month_payroll_ser.exchange_rate_euro),
            'total_cost' : round(this_month_payroll_ser.total_cost_vnd)
        }  
        except Payroll_Ser.DoesNotExist:
            serverine = Employee.objects.get(full_name='SEVERINE EDGARD-ROSA')
            payroll_ser_this_month = {
            'employee' : serverine,
            'head_count' : 0,
            'gross_income' : 0,
            'SHUI_21point5percent_company_pay' : 0,
            'trade_union_fee_company_pay' : 0,
            'PIT' : 0,
            'net_income' : 0,
            'total_cost' : 0
            }
        
        
        # Difference btw last month and this month
        difference_last_this = {
            'head_count' : payroll_staff_this_month['head_count'] + payroll_coll_this_month['head_count'] + payroll_ser_this_month['head_count'] - payroll_staff_last_month['head_count'] - payroll_coll_last_month['head_count'] - payroll_ser_last_month['head_count'],
            'gross_income' : payroll_staff_this_month['gross_income'] + payroll_coll_this_month['gross_income'] + payroll_ser_this_month['gross_income'] - payroll_staff_last_month['gross_income'] - payroll_coll_last_month['gross_income'] - payroll_ser_last_month['gross_income'],
            'transportation' : payroll_staff_this_month['transportation'] + payroll_coll_this_month['transportation'] - payroll_staff_last_month['transportation'] - payroll_coll_last_month['transportation'],
            'phone' : payroll_staff_this_month['phone'] + payroll_coll_this_month['phone'] - payroll_staff_last_month['phone'] - payroll_coll_last_month['phone'],
            'lunch' : payroll_staff_this_month['lunch'] + payroll_coll_this_month['lunch'] - payroll_staff_last_month['lunch'] - payroll_coll_last_month['lunch'],
            'outstanding_annual_leave' : payroll_staff_this_month['outstanding_annual_leave'] + payroll_coll_this_month['outstanding_annual_leave'] - payroll_staff_last_month['outstanding_annual_leave'] - payroll_coll_last_month['outstanding_annual_leave'],
            'responsibility' : payroll_staff_this_month['responsibility'] + payroll_coll_this_month['responsibility'] - payroll_staff_last_month['responsibility'] - payroll_coll_last_month['responsibility'],
            'travel' : payroll_staff_this_month['travel'] + payroll_coll_this_month['travel'] - payroll_staff_last_month['travel'] - payroll_coll_last_month['travel'],
            'seniority_bonus' : payroll_staff_this_month['seniority_bonus'] + payroll_coll_this_month['seniority_bonus'] - payroll_staff_last_month['seniority_bonus'] - payroll_coll_last_month['seniority_bonus'],
            'other' : payroll_staff_this_month['other'] + payroll_coll_this_month['other'] - payroll_staff_last_month['other'] - payroll_coll_last_month['other'],
            'OTC_incentive' : payroll_staff_this_month['OTC_incentive'] + payroll_coll_this_month['OTC_incentive'] - payroll_staff_last_month['OTC_incentive'] - payroll_coll_last_month['OTC_incentive'],
            'KPI_achievement' : payroll_staff_this_month['KPI_achievement'] + payroll_coll_this_month['KPI_achievement'] - payroll_staff_last_month['KPI_achievement'] - payroll_coll_last_month['KPI_achievement'],
            'incentive_last_month' : payroll_staff_this_month['incentive_last_month'] + payroll_coll_this_month['incentive_last_month'] - payroll_staff_last_month['incentive_last_month'] - payroll_coll_last_month['incentive_last_month'],
            'month_13_salary_Pro_ata' : payroll_staff_this_month['month_13_salary_Pro_ata'] + payroll_coll_this_month['month_13_salary_Pro_ata'] - payroll_staff_last_month['month_13_salary_Pro_ata'] - payroll_coll_last_month['month_13_salary_Pro_ata'],
            'incentive_last_quy_last_year' : payroll_staff_this_month['incentive_last_quy_last_year'] + payroll_coll_this_month['incentive_last_quy_last_year'] - payroll_staff_last_month['incentive_last_quy_last_year'] - payroll_coll_last_month['incentive_last_quy_last_year'],
            'taxable_overtime' : payroll_staff_this_month['taxable_overtime'] + payroll_coll_this_month['taxable_overtime'] - payroll_staff_last_month['taxable_overtime'] - payroll_coll_last_month['taxable_overtime'],
            'nontaxable_overtime' : payroll_staff_this_month['nontaxable_overtime'] + payroll_coll_this_month['nontaxable_overtime'] - payroll_staff_last_month['nontaxable_overtime'] - payroll_coll_last_month['nontaxable_overtime'],
            'SHUI_10point5percent_employee_pay' : payroll_staff_this_month['SHUI_10point5percent_employee_pay'] + payroll_coll_this_month['SHUI_10point5percent_employee_pay'] - payroll_staff_last_month['SHUI_10point5percent_employee_pay'] - payroll_coll_last_month['SHUI_10point5percent_employee_pay'],
            'SHUI_21point5percent_company_pay' : payroll_staff_this_month['SHUI_21point5percent_company_pay'] + payroll_coll_this_month['SHUI_21point5percent_company_pay'] + payroll_ser_this_month['SHUI_21point5percent_company_pay'] - payroll_staff_last_month['SHUI_21point5percent_company_pay'] - payroll_coll_last_month['SHUI_21point5percent_company_pay'] - payroll_ser_last_month['SHUI_21point5percent_company_pay'],
            'occupational_accident_and_disease' : payroll_staff_this_month['occupational_accident_and_disease'] + payroll_coll_this_month['occupational_accident_and_disease'] - payroll_staff_last_month['occupational_accident_and_disease'] - payroll_coll_last_month['occupational_accident_and_disease'],
            'trade_union_fee_company_pay' : payroll_staff_this_month['trade_union_fee_company_pay'] + payroll_coll_this_month['trade_union_fee_company_pay'] + payroll_ser_this_month['trade_union_fee_company_pay'] - payroll_staff_last_month['trade_union_fee_company_pay'] - payroll_coll_last_month['trade_union_fee_company_pay'] - payroll_ser_last_month['trade_union_fee_company_pay'],
            'trade_union_fee_employee_pay' : payroll_staff_this_month['trade_union_fee_employee_pay'] + payroll_coll_this_month['trade_union_fee_employee_pay'] - payroll_staff_last_month['trade_union_fee_employee_pay'] - payroll_coll_last_month['trade_union_fee_employee_pay'],
            'family_deduction' : payroll_staff_this_month['family_deduction'] + payroll_coll_this_month['family_deduction'] - payroll_staff_last_month['family_deduction'] - payroll_coll_last_month['family_deduction'],
            'taxable_income' : payroll_staff_this_month['taxable_income'] + payroll_coll_this_month['taxable_income'] - payroll_staff_last_month['taxable_income'] - payroll_coll_last_month['taxable_income'],
            'taxed_income' : payroll_staff_this_month['taxed_income'] + payroll_coll_this_month['taxed_income'] - payroll_staff_last_month['taxed_income'] - payroll_coll_last_month['taxed_income'],
            'PIT' : payroll_staff_this_month['PIT'] + payroll_coll_this_month['PIT'] + payroll_ser_this_month['PIT'] - payroll_staff_last_month['PIT'] - payroll_coll_last_month['PIT'] - payroll_ser_last_month['PIT'],
            'net_income' : payroll_staff_this_month['net_income'] + payroll_coll_this_month['net_income'] + payroll_ser_this_month['net_income'] - payroll_staff_last_month['net_income'] - payroll_coll_last_month['net_income'] - payroll_ser_last_month['net_income'],
            'total_cost' : payroll_staff_this_month['total_cost'] + payroll_coll_this_month['total_cost'] + payroll_ser_this_month['total_cost'] - payroll_staff_last_month['total_cost'] - payroll_coll_last_month['total_cost'] - payroll_ser_last_month['total_cost'],
        }
        
        
        # Explain
        list_data = []
        for employee in list_employee_tedis_vietha_include_inactive:
            # Get payroll last month
            try:
                payroll_last_month = Payroll_Tedis_Vietha.objects.get(employee=employee,month=pk-1)
                head_count_last_month = 1
                gross_income_last_month = payroll_last_month.gross_income
                transportation_last_month = payroll_last_month.transportation
                phone_last_month = payroll_last_month.phone
                lunch_last_month = payroll_last_month.lunch
                outstanding_annual_leave_last_month = payroll_last_month.outstanding_annual_leave
                responsibility_last_month = payroll_last_month.responsibility
                travel_last_month = payroll_last_month.travel
                seniority_bonus_last_month = payroll_last_month.seniority_bonus
                other_last_month = payroll_last_month.other
                OTC_incentive_last_month = payroll_last_month.OTC_incentive
                KPI_achievement_last_month = payroll_last_month.KPI_achievement
                incentive_last_month_last_month = payroll_last_month.incentive_last_month
                month_13_salary_Pro_ata_last_month = payroll_last_month.month_13_salary_Pro_ata
                incentive_last_quy_last_year_last_month = payroll_last_month.incentive_last_quy_last_year
                taxable_overtime_last_month = payroll_last_month.taxable_overtime
                nontaxable_overtime_last_month = payroll_last_month.nontaxable_overtime
                SHUI_10point5percent_employee_pay_last_month = payroll_last_month.SHUI_10point5percent_employee_pay
                SHUI_21point5percent_company_pay_last_month = payroll_last_month.SHUI_21point5percent_company_pay
                occupational_accident_and_disease_last_month = payroll_last_month.occupational_accident_and_disease
                trade_union_fee_company_pay_last_month = payroll_last_month.trade_union_fee_company_pay
                trade_union_fee_employee_pay_last_month = payroll_last_month.trade_union_fee_employee_pay
                family_deduction_last_month = payroll_last_month.family_deduction
                taxable_income_last_month = payroll_last_month.taxable_income
                taxed_income_last_month = payroll_last_month.taxed_income
                PIT_last_month = payroll_last_month.PIT
                net_income_last_month = payroll_last_month.net_income
                total_cost_last_month = payroll_last_month.total_cost
            except Payroll_Tedis_Vietha.DoesNotExist:
                head_count_last_month = 0
                gross_income_last_month = 0
                transportation_last_month = 0
                phone_last_month = 0
                lunch_last_month = 0
                outstanding_annual_leave_last_month = 0
                responsibility_last_month = 0
                travel_last_month = 0
                seniority_bonus_last_month = 0
                other_last_month = 0
                OTC_incentive_last_month = 0
                KPI_achievement_last_month = 0
                incentive_last_month_last_month = 0
                month_13_salary_Pro_ata_last_month = 0
                incentive_last_quy_last_year_last_month = 0
                taxable_overtime_last_month = 0
                nontaxable_overtime_last_month = 0
                SHUI_10point5percent_employee_pay_last_month = 0
                SHUI_21point5percent_company_pay_last_month = 0
                occupational_accident_and_disease_last_month = 0
                trade_union_fee_company_pay_last_month = 0
                trade_union_fee_employee_pay_last_month = 0
                family_deduction_last_month = 0
                taxable_income_last_month = 0
                taxed_income_last_month = 0
                PIT_last_month = 0
                net_income_last_month = 0
                total_cost_last_month = 0
            # Get payroll this month
            try:
                payroll_this_month = Payroll_Tedis_Vietha.objects.get(employee=employee,month=pk)
                head_count_this_month = 1
                gross_income_this_month = payroll_this_month.gross_income
                transportation_this_month = payroll_this_month.transportation
                phone_this_month = payroll_this_month.phone
                lunch_this_month = payroll_this_month.lunch
                outstanding_annual_leave_this_month = payroll_this_month.outstanding_annual_leave
                responsibility_this_month = payroll_this_month.responsibility
                travel_this_month = payroll_this_month.travel
                seniority_bonus_this_month = payroll_this_month.seniority_bonus
                other_this_month = payroll_this_month.other
                OTC_incentive_this_month = payroll_this_month.OTC_incentive
                KPI_achievement_this_month = payroll_this_month.KPI_achievement
                incentive_last_month_this_month = payroll_this_month.incentive_last_month
                month_13_salary_Pro_ata_this_month = payroll_this_month.month_13_salary_Pro_ata
                incentive_last_quy_last_year_this_month = payroll_this_month.incentive_last_quy_last_year
                taxable_overtime_this_month = payroll_this_month.taxable_overtime
                nontaxable_overtime_this_month = payroll_this_month.nontaxable_overtime
                SHUI_10point5percent_employee_pay_this_month = payroll_this_month.SHUI_10point5percent_employee_pay
                SHUI_21point5percent_company_pay_this_month = payroll_this_month.SHUI_21point5percent_company_pay
                occupational_accident_and_disease_this_month = payroll_this_month.occupational_accident_and_disease
                trade_union_fee_company_pay_this_month = payroll_this_month.trade_union_fee_company_pay
                trade_union_fee_employee_pay_this_month = payroll_this_month.trade_union_fee_employee_pay
                family_deduction_this_month = payroll_this_month.family_deduction
                taxable_income_this_month = payroll_this_month.taxable_income
                taxed_income_this_month = payroll_this_month.taxed_income
                PIT_this_month = payroll_this_month.PIT
                net_income_this_month = payroll_this_month.net_income
                total_cost_this_month = payroll_this_month.total_cost
            except Payroll_Tedis_Vietha.DoesNotExist:
                head_count_this_month = 0
                gross_income_this_month = 0
                transportation_this_month = 0
                phone_this_month = 0
                lunch_this_month = 0
                outstanding_annual_leave_this_month = 0
                responsibility_this_month = 0
                travel_this_month = 0
                seniority_bonus_this_month = 0
                other_this_month = 0
                OTC_incentive_this_month = 0
                KPI_achievement_this_month = 0
                incentive_last_month_this_month = 0
                month_13_salary_Pro_ata_this_month = 0
                incentive_last_quy_last_year_this_month = 0
                taxable_overtime_this_month = 0
                nontaxable_overtime_this_month = 0
                SHUI_10point5percent_employee_pay_this_month = 0
                SHUI_21point5percent_company_pay_this_month = 0
                occupational_accident_and_disease_this_month = 0
                trade_union_fee_company_pay_this_month = 0
                trade_union_fee_employee_pay_this_month = 0
                family_deduction_this_month = 0
                taxable_income_this_month = 0
                taxed_income_this_month = 0
                PIT_this_month = 0
                net_income_this_month = 0
                total_cost_this_month = 0
                
            # Get reconcile remark
            try:
                reconcile_report = Report_reconcile_Tedis_VietHa.objects.get(employee=employee,month=pk)
                remark = reconcile_report.remark
                remark_id = reconcile_report.id
            except Report_reconcile_Tedis_VietHa.DoesNotExist:
                remark = ''
                remark_id = 0
                
            # Make data
            if head_count_last_month == 0 and head_count_this_month == 0:
                pass
            else:
                if round(head_count_this_month-head_count_last_month) == 0:
                    diff_head_count = ''
                else: 
                    diff_head_count = round(head_count_this_month-head_count_last_month)
                data = {
                    'employee' : employee,
                    'remark' : remark,
                    'remark_id' : remark_id,
                    'head_count' : diff_head_count,
                    'gross_income' : round(gross_income_this_month-gross_income_last_month),
                    'transportation' : round(transportation_this_month-transportation_last_month),
                    'phone' : round(phone_this_month-phone_last_month),
                    'lunch' : round(lunch_this_month-lunch_last_month),
                    'outstanding_annual_leave' : round(outstanding_annual_leave_this_month-outstanding_annual_leave_last_month),
                    'responsibility' : round(responsibility_this_month-responsibility_last_month),
                    'travel' : round(travel_this_month-travel_last_month),
                    'seniority_bonus' : round(seniority_bonus_this_month-seniority_bonus_last_month),
                    'other' : round(other_this_month-other_last_month),
                    'OTC_incentive' : round(OTC_incentive_this_month-OTC_incentive_last_month),
                    'KPI_achievement' : round(KPI_achievement_this_month-KPI_achievement_last_month),
                    'incentive_last_month' : round(incentive_last_month_this_month-incentive_last_month_last_month),
                    'month_13_salary_Pro_ata' : round(month_13_salary_Pro_ata_this_month-month_13_salary_Pro_ata_last_month),
                    'incentive_last_quy_last_year' : round(incentive_last_quy_last_year_this_month-incentive_last_quy_last_year_last_month),
                    'taxable_overtime' : round(taxable_overtime_this_month-taxable_overtime_last_month),
                    'nontaxable_overtime' : round(nontaxable_overtime_this_month-nontaxable_overtime_last_month),
                    'SHUI_10point5percent_employee_pay' : round(SHUI_10point5percent_employee_pay_this_month-SHUI_10point5percent_employee_pay_last_month),
                    'SHUI_21point5percent_company_pay' : round(SHUI_21point5percent_company_pay_this_month-SHUI_21point5percent_company_pay_last_month),
                    'occupational_accident_and_disease' : round(occupational_accident_and_disease_this_month-occupational_accident_and_disease_last_month),
                    'trade_union_fee_company_pay' : round(trade_union_fee_company_pay_this_month-trade_union_fee_company_pay_last_month),
                    'trade_union_fee_employee_pay' : round(trade_union_fee_employee_pay_this_month-trade_union_fee_employee_pay_last_month),
                    'family_deduction' : round(family_deduction_this_month-family_deduction_last_month),
                    'taxable_income' : round(taxable_income_this_month-taxable_income_last_month),
                    'taxed_income' : round(taxed_income_this_month-taxed_income_last_month),
                    'PIT' : round(PIT_this_month-PIT_last_month),
                    'net_income' : round(net_income_this_month-net_income_last_month),
                    'total_cost' : round(total_cost_this_month-total_cost_last_month)
                }
                list_data.append(data)
        # Make data for Ser
        try:
            reconcile_report_ser = Report_reconcile_Tedis_VietHa.objects.get(employee=payroll_ser_this_month['employee'],month=pk)
            remark_ser = reconcile_report_ser.remark
            remark_ser_id = reconcile_report_ser.id
        except Report_reconcile_Tedis_VietHa.DoesNotExist:
            remark_ser = ''
            remark_ser_id = 0
        
        if round(payroll_ser_this_month['head_count'] - payroll_ser_last_month['head_count']) == 0:
            diff_head_count_ser = ''
        else: 
            diff_head_count_ser = round(payroll_ser_this_month['head_count'] - payroll_ser_last_month['head_count'])
        ser_data = {
                'employee' : payroll_ser_this_month['employee'],
                'remark' : remark_ser,
                'remark_id' : remark_ser_id,
                'head_count' : diff_head_count_ser,
                'gross_income' : round(payroll_ser_this_month['gross_income'] - payroll_ser_last_month['gross_income']),
                'transportation' : 0,
                'phone' : 0,
                'lunch' : 0,
                'outstanding_annual_leave' : 0,
                'responsibility' : 0,
                'travel' : 0,
                'seniority_bonus' : 0,
                'other' : 0,
                'OTC_incentive' : 0,
                'KPI_achievement' : 0,
                'incentive_last_month' : 0,
                'month_13_salary_Pro_ata' : 0,
                'incentive_last_quy_last_year' : 0,
                'taxable_overtime' : 0,
                'nontaxable_overtime' : 0,
                'SHUI_10point5percent_employee_pay' : 0,
                'SHUI_21point5percent_company_pay' : round(payroll_ser_this_month['SHUI_21point5percent_company_pay'] - payroll_ser_last_month['SHUI_21point5percent_company_pay']),
                'occupational_accident_and_disease' : 0,
                'trade_union_fee_company_pay' : round(payroll_ser_this_month['trade_union_fee_company_pay'] - payroll_ser_last_month['trade_union_fee_company_pay']),
                'trade_union_fee_employee_pay' : 0,
                'family_deduction' : 0,
                'taxable_income' : 0,
                'taxed_income' : 0,
                'PIT' : round(payroll_ser_this_month['PIT'] - payroll_ser_last_month['PIT']),
                'net_income' : round(payroll_ser_this_month['net_income'] - payroll_ser_last_month['net_income']),
                'total_cost' : round(payroll_ser_this_month['total_cost'] - payroll_ser_last_month['total_cost'])
            }
        list_data.append(ser_data)        
                

        # Total 
        # Define total_var
        total_gross_income = 0
        total_transportation = 0
        total_phone = 0
        total_lunch = 0
        total_outstanding_annual_leave = 0
        total_responsibility = 0
        total_travel = 0
        total_seniority_bonus = 0
        total_other = 0
        total_OTC_incentive = 0
        total_KPI_achievement = 0
        total_incentive_last_month = 0
        total_month_13_salary_Pro_ata = 0
        total_incentive_last_quy_last_year = 0
        total_taxable_overtime = 0
        total_nontaxable_overtime = 0
        total_SHUI_10point5percent_employee_pay = 0
        total_SHUI_21point5percent_company_pay = 0
        total_occupational_accident_and_disease = 0
        total_trade_union_fee_company_pay = 0
        total_trade_union_fee_employee_pay = 0
        total_family_deduction = 0
        total_taxable_income = 0
        total_taxed_income = 0
        total_PIT = 0
        total_net_income = 0
        total_total_cost = 0
        # Get total data
        for data in list_data:
            if data['head_count'] == '':
                total_head_count += 0
            else: 
                total_head_count += (data['head_count'])
            total_gross_income += data['gross_income']
            total_transportation += data['transportation']
            total_phone += data['phone']
            total_lunch += data['lunch']
            total_outstanding_annual_leave += data['outstanding_annual_leave']
            total_responsibility += data['responsibility']
            total_travel += data['travel']
            total_seniority_bonus += data['seniority_bonus']
            total_other += data['other']
            total_OTC_incentive += data['OTC_incentive']
            total_KPI_achievement += data['KPI_achievement']
            total_incentive_last_month += data['incentive_last_month']
            total_month_13_salary_Pro_ata += data['month_13_salary_Pro_ata']
            total_incentive_last_quy_last_year += data['incentive_last_quy_last_year']
            total_taxable_overtime += data['taxable_overtime']
            total_nontaxable_overtime += data['nontaxable_overtime']
            total_SHUI_10point5percent_employee_pay += data['SHUI_10point5percent_employee_pay']
            total_SHUI_21point5percent_company_pay += data['SHUI_21point5percent_company_pay']
            total_occupational_accident_and_disease += data['occupational_accident_and_disease']
            total_trade_union_fee_company_pay += data['trade_union_fee_company_pay']
            total_trade_union_fee_employee_pay += data['trade_union_fee_employee_pay']
            total_family_deduction += data['family_deduction']
            total_taxable_income += data['taxable_income']
            total_taxed_income += data['taxed_income']
            total_PIT += data['PIT']
            total_net_income += data['net_income']
            total_total_cost += data['total_cost']
        # Make total data
        total_data = {
            'head_count' : total_head_count,
            'gross_income' : total_gross_income,
            'transportation' : total_transportation,
            'phone' : total_phone,
            'lunch' : total_lunch,
            'outstanding_annual_leave' : total_outstanding_annual_leave,
            'responsibility' : total_responsibility,
            'travel' : total_travel,
            'seniority_bonus' : total_seniority_bonus,
            'other' : total_other,
            'OTC_incentive' : total_OTC_incentive,
            'KPI_achievement' : total_KPI_achievement,
            'incentive_last_month' : total_incentive_last_month,
            'month_13_salary_Pro_ata' : total_month_13_salary_Pro_ata,
            'incentive_last_quy_last_year' : total_incentive_last_quy_last_year,
            'taxable_overtime' : total_taxable_overtime,
            'nontaxable_overtime' : total_nontaxable_overtime,
            'SHUI_10point5percent_employee_pay' : total_SHUI_10point5percent_employee_pay,
            'SHUI_21point5percent_company_pay' : total_SHUI_21point5percent_company_pay,
            'occupational_accident_and_disease' : total_occupational_accident_and_disease,
            'trade_union_fee_company_pay' : total_trade_union_fee_company_pay,
            'trade_union_fee_employee_pay' : total_trade_union_fee_employee_pay,
            'family_deduction' : total_family_deduction,
            'taxable_income' : total_taxable_income,
            'taxed_income' : total_taxed_income,
            'PIT' : total_PIT,
            'net_income' : total_net_income,
            'total_cost' : total_total_cost
        }
    except Month_in_period.DoesNotExist:
        payroll_staff_last_month=''
        payroll_coll_last_month=''
        payroll_ser_last_month=''
        payroll_staff_this_month=''
        payroll_coll_this_month=''
        payroll_ser_this_month=''
        difference_last_this=''
        list_data=''
        total_data=''

    # Create report 
    if request.POST.get('btn_create_report'): 
        # Create PIT
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha_include_inactive,month=period_month)
        for payroll in payroll_tedis_vietha: 
            # thu_nhap_chiu_thue
            thu_nhap_chiu_thue = payroll.taxable_income
            # tong_tnct_khau_tru_thue
            if payroll.PIT > 0:
                tong_tnct_khau_tru_thue = payroll.taxable_income
            else:
                tong_tnct_khau_tru_thue = 0
            # bao_hiem_bat_buoc
            bao_hiem_bat_buoc = payroll.SHUI_10point5percent_employee_pay
            # khau_tru
            khau_tru = payroll.family_deduction
            # thu_nhap_tinh_thue
            thu_nhap_tinh_thue = payroll.taxed_income
            # thuong,khac,cong
            thuong = 0
            khac = 0
            cong = 0
            # thue_tnct_phai_nop
            thue_tnct_phai_nop = payroll.PIT
            # ghi_chu 
            ghi_chu = ''
            # Get individual_type
            list_contracts = Employee_contract.objects.filter(employee=payroll.employee).order_by('-created_at') 
            contact_category_CTV = Contract_category.objects.get(contract_category='CTV')
            if list_contracts[0].contract_category == contact_category_CTV:
                individual_type = 'Cá Nhân Cư Trú'
            else:
                individual_type = ''
            
            
            pit_info = Report_PIT_Payroll_Tedis_VietHa(month=period_month,payroll=payroll,employee=payroll.employee,individual_type=individual_type,
                                                thu_nhap_chiu_thue=thu_nhap_chiu_thue,tong_tnct_khau_tru_thue=tong_tnct_khau_tru_thue,bao_hiem_bat_buoc=bao_hiem_bat_buoc,khau_tru=khau_tru,
                                                thu_nhap_tinh_thue=thu_nhap_tinh_thue,thuong=thuong,khac=khac,cong=cong,
                                                thue_tnct_phai_nop=thue_tnct_phai_nop,ghi_chu=ghi_chu)
            pit_info.save()
            
        # Create Report_Transfer_Payroll_Tedis_VietHa
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(month=period_month)
        for payroll in payroll_tedis_vietha: 
            list_contracts = Employee_contract.objects.filter(employee=payroll.employee).order_by('-created_at') 
            contact_category_CTV = Contract_category.objects.get(contract_category='CTV')
            if list_contracts[0].contract_category == contact_category_CTV:
                transfer_Coll_info = Report_Transfer_Payroll_Tedis_VietHa(month=period_month,payroll=payroll,employee=payroll.employee,employee_type='COLL',
                                                    amount=payroll.net_income)
                transfer_Coll_info.save()
            else:
                transfer_Staff_info = Report_Transfer_Payroll_Tedis_VietHa(month=period_month,payroll=payroll,employee=payroll.employee,employee_type='STAFF',
                                                    amount=payroll.net_income)
                transfer_Staff_info.save()
        
        # Create Payroll Ser
        serverine = Employee.objects.get(full_name='SEVERINE EDGARD-ROSA')
        
        exchange_rate_usd = request.POST.get('exchange_rate_usd')
        exchange_rate_euro = request.POST.get('exchange_rate_euro')
        
        salary_usd = request.POST.get('salary_usd')
        salary_vnd = request.POST.get('salary_vnd')
        working_days = request.POST.get('working_days')
        gross_income = request.POST.get('gross_income')
        salary_recuperation = request.POST.get('salary_recuperation')
        housing_euro = request.POST.get('housing_euro')
        housing_vnd = request.POST.get('housing_vnd')
        phone = request.POST.get('phone')
        lunch = request.POST.get('lunch')
        training_fee = request.POST.get('training_fee')
        toxic_allowance = request.POST.get('toxic_allowance')
        travel = request.POST.get('travel')
        responsibility = request.POST.get('responsibility')
        seniority_bonus = request.POST.get('seniority_bonus')
        other = request.POST.get('other')
        total_allowance_recuperation = request.POST.get('total_allowance_recuperation')
        benefits = request.POST.get('benefits')
        severance_allowance = request.POST.get('severance_allowance')
        outstanding_annual_leave = request.POST.get('outstanding_annual_leave')
        month_13_salary_Pro_ata = request.POST.get('month_13_salary_Pro_ata')
        SHUI_9point5percent_employee_pay = request.POST.get('SHUI_9point5percent_employee_pay')
        recuperation_of_SHU_Ins_10point5percent_staff_pay = request.POST.get('recuperation_of_SHU_Ins_10point5percent_staff_pay')
        SHUI_20point5percent_employer_pay = request.POST.get('SHUI_20point5percent_employer_pay')
        recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
        occupational_accident_and_disease = request.POST.get('occupational_accident_and_disease')
        trade_union_fee_company_pay = request.POST.get('trade_union_fee_company_pay')
        trade_union_fee_member = request.POST.get('trade_union_fee_member')
        family_deduction = request.POST.get('family_deduction')
        taxable_income = request.POST.get('taxable_income')
        taxed_income = request.POST.get('taxed_income')
        PIT = request.POST.get('PIT')
        first_payment_cash_advance_euro = request.POST.get('first_payment_cash_advance_euro')
        second_payment_net_income_vnd = request.POST.get('second_payment_net_income_vnd')
        second_payment_net_income_euro = request.POST.get('second_payment_net_income_euro')
        net_income = request.POST.get('net_income')
        total_cost_vnd = request.POST.get('total_cost_vnd')
        total_cost_usd = request.POST.get('total_cost_usd')
        note = request.POST.get('note')
        payroll_ser_info = Payroll_Ser(month=period_month,employee=serverine,
                                       exchange_rate_usd=exchange_rate_usd,exchange_rate_euro=exchange_rate_euro,
                                       salary_usd=salary_usd,salary_vnd=salary_vnd,
                                       working_days=working_days,
                                       gross_income=gross_income,salary_recuperation=salary_recuperation,
                                       housing_euro=housing_euro,housing_vnd=housing_vnd,
                                       phone=phone,lunch=lunch,training_fee=training_fee,toxic_allowance=toxic_allowance,travel=travel,
                                       responsibility=responsibility,seniority_bonus=seniority_bonus,other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,
                                       severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata,SHUI_9point5percent_employee_pay=SHUI_9point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,
                                       SHUI_20point5percent_employer_pay=SHUI_20point5percent_employer_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease=occupational_accident_and_disease,trade_union_fee_company_pay=trade_union_fee_company_pay,trade_union_fee_member=trade_union_fee_member,
                                       family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT=PIT,first_payment_cash_advance_euro=first_payment_cash_advance_euro,
                                       second_payment_net_income_vnd=second_payment_net_income_vnd,second_payment_net_income_euro=second_payment_net_income_euro,net_income=net_income,total_cost_vnd=total_cost_vnd,total_cost_usd=total_cost_usd,
                                       note=note)  
        payroll_ser_info.save()

                
        # Create Report_Payment_Payroll_Tedis_VietHa
        # Get staff and coll employee:
        list_employees = []
        list_collaborator = []
        contact_category_CTV = Contract_category.objects.get(contract_category='CTV')
        for employee in list_employee_tedis_vietha_include_inactive:
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at') 
            if list_contracts[0].contract_category == contact_category_CTV: 
                list_collaborator.append(employee.id)  
            else:
                list_employees.append(list_contracts[0].employee.id)
        '''Salary'''
        # Salary Employee 
        amount_vnd = 0
        payroll_employee_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employees,month=period_month)
        for payroll in payroll_employee_tedis_vietha:
            amount_vnd += round(payroll.net_income, 0)
        month_string = str(period_month.month_number) + '/' + str(period_month.period.period_year)
        payment_salary_employee_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                        item='SALARY',description='Employees',amount_vnd=amount_vnd,amount_euro=0,
                                                                        paidby='Transfer',paidto='Employees',account_no='Lương tháng ' + month_string)
        payment_salary_employee_info.save()
        # Salary collaborator
        amount_vnd = 0
        payroll_collaborator_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_collaborator,month=period_month)
        for payroll in payroll_collaborator_tedis_vietha:
            amount_vnd += round(payroll.net_income, 0)
        month_string = str(period_month.month_number) + '/' + str(period_month.period.period_year)
        payment_salary_collaborator_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                        item='SALARY',description='Collaborator',amount_vnd=amount_vnd,amount_euro=0,
                                                                        paidby='Transfer',paidto='Collaborator',account_no='Lương tháng ' + month_string)
        payment_salary_collaborator_info.save()
        
        # Salary + allowance serverine
        payroll_ser = Payroll_Ser.objects.get(month=period_month)
        payment_salary_and_allowance_ser_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                        item='SALARY + ALLOWANCE',description='Severine',amount_vnd=0,amount_euro=float(payroll_ser.net_income),
                                                                        paidby='Transfer',paidto='Severine',account_no='EDGARD-ROSA JONVILLE SEVERINE CECILE HSBC Ho Chi Minh 001-099563-148 Nội dung ck: Lương & Phụ cấp tháng ' + month_string)
        payment_salary_and_allowance_ser_info.save()
        '''SHUI'''
        # Get CT and CT- employees
        list_employees_ct = []
        list_employees_ctminus = []
        contact_category_CT = Contract_category.objects.get(contract_category='CT')
        contact_category_CTminus = Contract_category.objects.get(contract_category='CT-')
        contact_category_CTV = Contract_category.objects.get(contract_category='CTV')
        for employee in list_employee_tedis_vietha_include_inactive:            
            list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at') 
            if list_contracts[0].contract_category == contact_category_CTminus:   
                list_employees_ctminus.append(employee.id)
            if list_contracts[0].contract_category == contact_category_CT: 
                list_employees_ct.append(employee.id) 
        # SHUI Company CT       
        total_SHUI_Company_CT_amount = 0
        payroll_employee_ct = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employees_ct,month=period_month)
        for payroll in payroll_employee_ct:
            total_SHUI_Company_CT_amount += round(payroll.SHUI_21point5percent_company_pay)
        payment_SHUI_Company_employeeCT_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='SHUI',description='SHUI Company',amount_vnd=total_SHUI_Company_CT_amount,amount_euro=0,
                                                                    paidby='Transfer',paidto='Long An SI',account_no='BHXH Huyện Cần Giuộc Số tài khoản: 063.100.0456416 Ngân hàng: Vietcombank - CN Long An Nội dung: TT BHXH, BHYT, BHTN, TNLD & BNN tháng ' + month_string + ' - Mã đơn vị TM0330M')
        payment_SHUI_Company_employeeCT_info.save()
        # SHUI Employees
        SHUI_Employees_amount = 0
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha_include_inactive,month=period_month)
        for payroll in payroll_tedis_vietha:
            SHUI_Employees_amount += round(payroll.SHUI_10point5percent_employee_pay)
        payment_SHUI_Employee_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='SHUI',description='SHUI Employee',amount_vnd=SHUI_Employees_amount,amount_euro=0,
                                                                    paidby='Transfer',paidto='Long An SI',account_no='BHXH Huyện Cần Giuộc Số tài khoản: 063.100.0456416 Ngân hàng: Vietcombank - CN Long An Nội dung: TT BHXH, BHYT, BHTN, TNLD & BNN tháng ' + month_string + ' - Mã đơn vị TM0330M')
        payment_SHUI_Employee_info.save()
        # SHUI Company CT-       
        total_SHUI_Company_CTminus_amount = 0
        payroll_employee_ctminus = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employees_ctminus,month=period_month)
        for payroll in payroll_employee_ctminus:
            total_SHUI_Company_CTminus_amount += round(payroll.SHUI_21point5percent_company_pay)
        payment_SHUI_Company_employeeCTminus_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='SHUI',description='SHUI Company',amount_vnd=total_SHUI_Company_CTminus_amount,amount_euro=0,
                                                                    paidby='Transfer',paidto='Long An SI',account_no='BHXH Huyện Cần Giuộc Số tài khoản: 063.100.0456416 Ngân hàng: Vietcombank - CN Long An Nội dung: TT TNLD & BNN tháng ' + month_string + ' - Mã đơn vị ZC0330M')
        payment_SHUI_Company_employeeCTminus_info.save()
        # SHUI Company ser      
        payroll_ser = Payroll_Ser.objects.get(month=period_month)
        payment_SHUI_Company_ser_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='SHUI',description='SHUI Company',amount_vnd=float(payroll_ser.SHUI_9point5percent_employee_pay) + float(payroll_ser.SHUI_20point5percent_employer_pay),amount_euro=0,
                                                                    paidby='Transfer',paidto='Long An SI',account_no='BHXH Huyện Cần Giuộc Số tài khoản: 063.100.0456416 Ngân hàng: Vietcombank - CN Long An Nội dung: TT BHXH, BHYT, TNLD & BNN tháng ' + month_string + ' - Mã đơn vị IC0330M')
        payment_SHUI_Company_ser_info.save()
        '''PIT'''
        PIT_amount = 0
        payroll_ser = Payroll_Ser.objects.get(month=period_month)
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha_include_inactive,month=period_month)
        for payroll in payroll_tedis_vietha:
            PIT_amount += round(payroll.PIT_balance)
        PIT_amount += float(payroll_ser.PIT)
        payment_PIT_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='PIT',description='Salary PIT',amount_vnd=PIT_amount,amount_euro=0,
                                                                    paidby='Transfer',paidto='Tax Long An',account_no='Cục thuế tỉnh Long An - KBNN tỉnh Long An - 7111 (MST 1101247615)')
        payment_PIT_info.save()
        '''TRADE UNION'''
        # TRADE UNION company
        trade_union_company_amount = 0
        payroll_ser = Payroll_Ser.objects.get(month=period_month)
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha_include_inactive,month=period_month)
        for payroll in payroll_tedis_vietha:
            trade_union_company_amount += round(payroll.trade_union_fee_company_pay)
        trade_union_company_amount += float(payroll_ser.trade_union_fee_company_pay)
        payment_trade_union_company_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='TRADE UNION',description='Trade Union fee',amount_vnd=trade_union_company_amount,amount_euro=0,
                                                                    paidby='Transfer',paidto='Trade Union',account_no='Công đoàn Việt Nam - 117001366668 - NH Vietinbank - CN Hoàng Mai - Hà Nội Nội dung: MST 1101247615 Cty Cổ phần dược phẩm Tedis - Việt Hà đóng KPCĐ 2% tháng ' + month_string)
        payment_trade_union_company_info.save()
        # TRADE UNION member
        trade_union_member_amount = 0
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha_include_inactive,month=period_month)
        for payroll in payroll_tedis_vietha:
            trade_union_member_amount += round(payroll.trade_union_fee_employee_pay)
        payment_trade_union_member_info = Report_Payment_Payroll_Tedis_VietHa(month=period_month,
                                                                    item='TRADE UNION',description='Trade Union (member fee)',amount_vnd=trade_union_member_amount,amount_euro=0,
                                                                    paidby='Transfer',paidto='Trade Union',account_no='BCH CD CT DUOC PHAM TEDIS VIET HA - 120000074478 - NH Vietinbank - CN4 Nội dung: MST 1101247615 Cty Cổ phần dược phẩm Tedis - Việt Hà đóng ĐPCĐ 1% tháng ' + month_string)
        payment_trade_union_member_info.save()
        
        
        # '''Infor.Payroll'''
        # NEW STAFF
        for employee in list_employee_tedis_vietha_include_inactive:
            joining_month_year_str = employee.joining_date.strftime('%#m/%Y')
            # Get period month str
            month_str = str(period_month.month_number) + '/' + str(period_month.period.period_year)
            # Compare month_str and joining_month_year_str to get new employee
            if joining_month_year_str == month_str: 
                # Get Salary info
                payroll_info = Payroll_Tedis_Vietha.objects.get(month=period_month,employee=employee)
                new_straff_info = Report_new_staff_Tedis_VietHa(month=period_month,employee=employee,
                                                                    department=employee.department_e,joining_date=employee.joining_date,
                                                                    gross_salary=payroll_info.newest_salary,allowance=0,dependant_deduction=payroll_info.family_deduction,hospital_for_HI=employee.hi_medical_place,
                                                                    account_no=employee.account_no,bank_name=employee.bank)
                new_straff_info.save()
            else: 
                pass
        # RESIGNED STAFF
        for employee in list_employee_tedis_vietha_include_inactive:
            if employee.out_date == None:
                pass
            else:
                leaving_month_year_str = employee.out_date.strftime('%#m/%Y')
                # Get period month str
                month_str = str(period_month.month_number) + '/' + str(period_month.period.period_year)
                # Compare month_str and leaving_month_year_str to get new employee
                if leaving_month_year_str == month_str: 
                    # Get Salary info
                    resigned_straff_info = Report_resigned_staff_Tedis_VietHa(month=period_month,employee=employee,
                                                                        department=employee.department_e,joining_date=employee.joining_date,
                                                                        leaving_date=employee.out_date)
                    resigned_straff_info.save()
                else: 
                    pass
                
        # MATERNITY LEAVE
        for employee in list_employee_tedis_vietha_include_inactive:
            list_leave_applications = Leave_application.objects.filter(employee=employee)
            for leave_application in list_leave_applications:
                if leave_application.maternity_obstetric_from != '':
                    maternity_obstetric_from_month_year_str_before_format = datetime.strptime(leave_application.maternity_obstetric_from, "%Y-%m-%d")
                    maternity_obstetric_from_month_year_str_after_format = maternity_obstetric_from_month_year_str_before_format.strftime('%#m/%Y')
                    # Get period month str
                    month_str = str(period_month.month_number) + '/' + str(period_month.period.period_year)
                    # Compare month_str and leaving_month_year_str to create Report_maternity_leave_Tedis_VietHa
                    if maternity_obstetric_from_month_year_str_after_format == month_str:
                        maternity_leave_info = Report_maternity_leave_Tedis_VietHa(month=period_month,employee=employee,
                                                                        department=employee.department_e,from_date=datetime.strptime(leave_application.maternity_obstetric_from, "%Y-%m-%d"),
                                                                        to_date=datetime.strptime(leave_application.maternity_obstetric_to, "%Y-%m-%d"))
                        maternity_leave_info.save()
                else: 
                    pass
                
        # Reconcile remark
        for employee in list_employee_tedis_vietha_include_inactive:
            reconcile_remark_info = Report_reconcile_Tedis_VietHa(month=period_month,employee=employee,remark='',
                                                                  created_by=s_user[2],created_at=datetime.now())
            reconcile_remark_info.save()
            
        serverine = Employee.objects.get(full_name='SEVERINE EDGARD-ROSA')
        reconcile_remark_ser_info = Report_reconcile_Tedis_VietHa(month=period_month,employee=serverine,remark='',
                                                                  created_by=s_user[2],created_at=datetime.now())
        reconcile_remark_ser_info.save()
            
                
            
        messages.success(request, 'SUCCESS: Report created!')
        return redirect('employee:report_payroll_tedis_vietha',pk=period_month.id)
    
    '''ADD record'''
    # PIT
    list_individual_types = ['','Cá Nhân Cư Trú','Cá Nhân Không Cư Trú']
    if request.POST.get('btnAddPIT'):
        month_id = request.POST.get('month')
        month = Month_in_period.objects.get(id=month_id)
        employee_id = request.POST.get('employee')
        employee = Employee.objects.get(id=employee_id)
        individual_type = request.POST.get('individual_type')
        thu_nhap_chiu_thue = request.POST.get('thu_nhap_chiu_thue')
        tong_tnct_khau_tru_thue = request.POST.get('tong_tnct_khau_tru_thue')
        bao_hiem_bat_buoc = request.POST.get('bao_hiem_bat_buoc')
        khau_tru = request.POST.get('khau_tru')
        thu_nhap_tinh_thue = request.POST.get('thu_nhap_tinh_thue')
        thuong = request.POST.get('thuong')
        khac = request.POST.get('khac')
        cong = request.POST.get('cong')
        thue_tnct_phai_nop = request.POST.get('thue_tnct_phai_nop')
        ghi_chu = request.POST.get('ghi_chu')
        pit_newrecord_info = Report_PIT_Payroll_Tedis_VietHa(month=month,employee=employee,individual_type=individual_type,
                                                            thu_nhap_chiu_thue=thu_nhap_chiu_thue,tong_tnct_khau_tru_thue=tong_tnct_khau_tru_thue,bao_hiem_bat_buoc=bao_hiem_bat_buoc,khau_tru=khau_tru,
                                                            thu_nhap_tinh_thue=thu_nhap_tinh_thue,thuong=thuong,khac=khac,cong=cong,
                                                            thue_tnct_phai_nop=thue_tnct_phai_nop,ghi_chu=ghi_chu)
        pit_newrecord_info.save()
        messages.success(request, 'SUCCESS: Record created')
        return redirect('employee:report_payroll_tedis_vietha',pk=period_month.id)
    
    # Report_confirmed_after_probation_Tedis_VietHa
    if request.POST.get('btnAddConfirmedAfterProbation'):
        month_id = request.POST.get('month')
        month = Month_in_period.objects.get(id=month_id)
        employee_id = request.POST.get('employee')
        employee = Employee.objects.get(id=employee_id)
        sign_LC_date = request.POST.get('sign_LC_date')
        allowance = request.POST.get('allowance')
        salary_after_probation = request.POST.get('salary_after_probation')
        confirmedafterprobation_newrecord_info = Report_confirmed_after_probation_Tedis_VietHa(month=month,employee=employee,
                                                            department=employee.department_e,joining_date=employee.joining_date,
                                                            sign_LC_date=sign_LC_date,allowance=allowance,salary_after_probation=salary_after_probation,
                                                            SI_book_no=employee.social_insurrance_book,hospital_for_HI=employee.hi_medical_place)
        confirmedafterprobation_newrecord_info.save()
        messages.success(request, 'SUCCESS: Record created')
        return redirect('employee:report_payroll_tedis_vietha',pk=period_month.id)
    
    # Report_other_changes_Tedis_VietHa
    if request.POST.get('btnAddOtherChanges'):
        month_id = request.POST.get('month')
        month = Month_in_period.objects.get(id=month_id)
        employee_id = request.POST.get('employee')
        employee = Employee.objects.get(id=employee_id)
        new_salary = request.POST.get('new_salary')
        allowance = request.POST.get('allowance')
        effective_date = request.POST.get('effective_date')
        remark = request.POST.get('remark')
        other_changes_newrecord_info = Report_other_changes_Tedis_VietHa(month=month,employee=employee,
                                                            new_salary=new_salary,allowance=allowance,effective_date=effective_date,remark=remark)
        other_changes_newrecord_info.save()
        messages.success(request, 'SUCCESS: Record created')
        return redirect('employee:report_payroll_tedis_vietha',pk=period_month.id)
    
    
    '''Delete record'''
    # Report_confirmed_after_probation_Tedis_VietHa
    if request.POST.get('btnDeleteConfirmedAfterProbation'):
        ConfirmedAfterProbation_id = request.POST.get('ConfirmedAfterProbation_id')
        try:
            confirmedafterprobation_info = Report_confirmed_after_probation_Tedis_VietHa.objects.get(id=ConfirmedAfterProbation_id)
            confirmedafterprobation_info.delete()
            messages.success(request, 'SUCCESS: Object deleted')
        except Report_confirmed_after_probation_Tedis_VietHa.DoesNotExist:
            messages.error(request, 'Error: Failed to delete object')
        return redirect('employee:report_payroll_tedis_vietha',pk=period_month.id)

    # Report_other_changes_Tedis_VietHa
    if request.POST.get('btnDeleteOtherChanges'):
        OtherChanges_id = request.POST.get('OtherChanges_id')
        try:
            otherchanges_info = Report_other_changes_Tedis_VietHa.objects.get(id=OtherChanges_id)
            otherchanges_info.delete()
            messages.success(request, 'SUCCESS: Object deleted')
        except Report_other_changes_Tedis_VietHa.DoesNotExist:
            messages.error(request, 'Error: Failed to delete object')
        return redirect('employee:report_payroll_tedis_vietha',pk=period_month.id)
    
        
    
    
    # Export report
    if request.POST.get('export'):   
        # Export excel
        file_name = str(period_month.month_number) + ' Payroll ' + str(period_month.month_name) + ' Tedis-Vietha.xlsx'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_total_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 200, name Arial, colour red; align: horiz center, vert center' % 'white')
        style_total_red_onlyvertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 200, name Arial, colour red; align: vert center' % 'white')
        style_head_11pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                           'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Times New Roman, colour black; align: horiz center, vert center' % 'white')
        style_head_11pt_bold.alignment.wrap = 1
        style_head_11pt_bold_left = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                           'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Times New Roman, colour black; align: horiz left, vert center' % 'white')
        style_head_11pt_bold_green = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                           'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Times New Roman, colour black; align: horiz center, vert center' % 'lime')
        style_head_small = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 300, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'pale_blue')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        
        
        '''Sheet PIT'''
        # Create sheet
        ws_PIT = wb.add_sheet('PIT')
        # Set col width
        ws_PIT.col(0).width = 2000
        ws_PIT.col(1).width = 3500
        ws_PIT.col(2).width = 8000
        for col in range(3,14):
            ws_PIT.col(col).width = 5000
        
        # Set row height
        ws_PIT.row(0).height_mismatch = True
        ws_PIT.row(0).height = 330
        ws_PIT.row(1).height_mismatch = True
        ws_PIT.row(1).height = 670
        # Top
        ws_PIT.write_merge(0, 1, 0, 0, 'STT', style_head_11pt_bold)
        ws_PIT.write_merge(0, 1, 1, 1, 'Mã nhân viên', style_head_11pt_bold)
        ws_PIT.write_merge(0, 1, 2, 2, 'Họ và tên', style_head_11pt_bold_left)
        ws_PIT.write_merge(0, 1, 3, 3, 'CCCD', style_head_11pt_bold)
        ws_PIT.write_merge(0, 1, 4, 4, 'MST cá nhân', style_head_11pt_bold)
        ws_PIT.write_merge(0, 0, 5, 8, 'Thu nhập chịu thuế', style_head_11pt_bold)
        ws_PIT.write(1, 5, 'Thu nhập chịu thuế', style_head_11pt_bold_green)
        ws_PIT.write(1, 6, 'Tổng TNCT thuộc diện khấu trừ thuế', style_head_11pt_bold)
        ws_PIT.write(1, 7, 'Bảo hiểm bắt buộc', style_head_11pt_bold)
        ws_PIT.write(1, 8, 'Khấu trừ', style_head_11pt_bold)
        ws_PIT.write_merge(0, 0, 9, 12, 'Thu nhập tính thuế', style_head_11pt_bold)
        ws_PIT.write(1, 9, 'Thu nhập tính thuế', style_head_11pt_bold_green)
        ws_PIT.write(1, 10, 'Thưởng', style_head_11pt_bold)  
        ws_PIT.write(1, 11, 'Khác', style_head_11pt_bold) 
        ws_PIT.write(1, 12, 'Cộng', style_head_11pt_bold)        
        ws_PIT.write_merge(0, 1, 13, 13, 'Thuế TNCN phải nộp', style_head_11pt_bold_green)
        ws_PIT.write_merge(0, 1, 14, 14, 'Ghi Chú', style_head_11pt_bold_left)
        # Body
        # A
        ws_PIT.write(2, 0, 'A', style_head_11pt_bold)
        ws_PIT.write(2, 2, 'Người Việt Nam', style_head_11pt_bold)
        for col_row2 in range(3,15):
            ws_PIT.write(2, col_row2, '', style_head_11pt_bold)
        # PIT A data
        # Khai báo total
        ttAthu_nhap_chiu_thue = 0
        ttAtong_tnct_khau_tru_thue = 0
        ttAbao_hiem_bat_buoc = 0
        ttAkhau_tru = 0
        ttAthu_nhap_tinh_thue = 0
        ttAthuong = 0
        ttAkhac = 0
        ttAcong = 0
        ttAthue_tnct_phai_nop = 0
        ttAghichu = 0
        for index, pit_data in enumerate(report_pit_payroll):
            # Set row height
            ws_PIT.row(3+index).height_mismatch = True
            ws_PIT.row(3+index).height = 400
            # Write data
            ws_PIT.write(3+index, 0, str(index+1),style_normal)
            ws_PIT.write(3+index, 1, str(pit_data.employee.employee_code),style_normal)
            ws_PIT.write(3+index, 2, str(pit_data.employee.full_name),style_normal)
            ws_PIT.write(3+index, 3, str(pit_data.employee.id_card_no),style_normal)
            ws_PIT.write(3+index, 4, str(pit_data.employee.personal_income_tax),style_normal)
            ws_PIT.write(3+index, 5, str("{:,}".format(round(pit_data.thu_nhap_chiu_thue),0)),style_normal)
            ws_PIT.write(3+index, 6, str("{:,}".format(round(pit_data.tong_tnct_khau_tru_thue),0)),style_normal)
            ws_PIT.write(3+index, 7, str("{:,}".format(round(pit_data.bao_hiem_bat_buoc),0)),style_normal)
            ws_PIT.write(3+index, 8, str("{:,}".format(round(pit_data.khau_tru),0)),style_normal)
            ws_PIT.write(3+index, 9, str("{:,}".format(round(pit_data.thu_nhap_tinh_thue),0)),style_normal)
            ws_PIT.write(3+index, 10, str("{:,}".format(round(pit_data.thuong),0)),style_normal)
            ws_PIT.write(3+index, 11, str("{:,}".format(round(pit_data.khac),0)),style_normal)
            ws_PIT.write(3+index, 12, str("{:,}".format(round(pit_data.cong),0)),style_normal)
            ws_PIT.write(3+index, 13, str("{:,}".format(round(pit_data.thue_tnct_phai_nop),0)),style_normal)
            ws_PIT.write(3+index, 14, str(pit_data.ghi_chu),style_normal)
            # Total
            ttAthu_nhap_chiu_thue += round(pit_data.thu_nhap_chiu_thue,0)
            ttAtong_tnct_khau_tru_thue += round(pit_data.tong_tnct_khau_tru_thue,0)
            ttAbao_hiem_bat_buoc += round(pit_data.bao_hiem_bat_buoc,0) 
            ttAkhau_tru += round(pit_data.khau_tru,0)
            ttAthu_nhap_tinh_thue += round(pit_data.thu_nhap_tinh_thue,0)
            ttAthuong += round(pit_data.thuong,0)
            ttAkhac += round(pit_data.khac,0)
            ttAcong += round(pit_data.cong,0)
            ttAthue_tnct_phai_nop += round(pit_data.thue_tnct_phai_nop,0)
            if pit_data.thue_tnct_phai_nop > 0:
                ttAghichu += 1
            last_A_row = 3+index+1
        # Total
        # Set row height
        ws_PIT.row(last_A_row).height_mismatch = True
        ws_PIT.row(last_A_row).height = 400
        # data
        ws_PIT.write(last_A_row, 0, str(index+1), style_total_red)
        ws_PIT.write_merge(last_A_row, last_A_row, 1, 4, 'Tổng Cộng A', style_total_red_onlyvertcen)
        ws_PIT.write(last_A_row, 5, str("{:,}".format(round(ttAthu_nhap_chiu_thue),0)), style_total_red)
        ws_PIT.write(last_A_row, 6, str("{:,}".format(round(ttAtong_tnct_khau_tru_thue),0)), style_total_red)
        ws_PIT.write(last_A_row, 7, str("{:,}".format(round(ttAbao_hiem_bat_buoc),0)), style_total_red)
        ws_PIT.write(last_A_row, 8, str("{:,}".format(round(ttAkhau_tru),0)), style_total_red)
        ws_PIT.write(last_A_row, 9, str("{:,}".format(round(ttAthu_nhap_tinh_thue),0)), style_total_red)
        ws_PIT.write(last_A_row, 10, str("{:,}".format(round(ttAthuong),0)), style_total_red)
        ws_PIT.write(last_A_row, 11, str("{:,}".format(round(ttAkhac),0)), style_total_red)
        ws_PIT.write(last_A_row, 12, str("{:,}".format(round(ttAcong),0)), style_total_red)
        ws_PIT.write(last_A_row, 13, str("{:,}".format(round(ttAthue_tnct_phai_nop),0)), style_total_red)
        ws_PIT.write(last_A_row, 14, str(ttAghichu), style_total_red)
        last_A_total_row = last_A_row + 1
        # B
        ws_PIT.write(last_A_total_row, 0, 'B', style_head_11pt_bold)
        ws_PIT.write(last_A_total_row, 2, 'Cá Nhân Cư Trú', style_head_11pt_bold)
        for col_row in range(3,15):
            ws_PIT.write(last_A_total_row, col_row, '', style_head_11pt_bold)
        # PIT B data
        # Khai báo total
        ttBthu_nhap_chiu_thue = 0
        ttBtong_tnct_khau_tru_thue = 0
        ttBbao_hiem_bat_buoc = 0
        ttBkhau_tru = 0
        ttBthu_nhap_tinh_thue = 0
        ttBthuong = 0
        ttBkhac = 0
        ttBcong = 0
        ttBthue_tnct_phai_nop = 0
        ttBghichu = 0
        if report_pit_payroll_canhancutru.exists():
            for index, pit_data in enumerate(report_pit_payroll_canhancutru):
                # Set row height
                ws_PIT.row(last_A_total_row+1+index).height_mismatch = True
                ws_PIT.row(last_A_total_row+1+index).height = 400
                # Write data
                ws_PIT.write(last_A_total_row+1+index, 0, str(index+1),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 1, str(pit_data.employee.employee_code),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 2, str(pit_data.employee.full_name),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 3, str(pit_data.employee.id_card_no),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 4, str(pit_data.employee.personal_income_tax),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 5, str("{:,}".format(round(pit_data.thu_nhap_chiu_thue),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 6, str("{:,}".format(round(pit_data.tong_tnct_khau_tru_thue),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 7, str("{:,}".format(round(pit_data.bao_hiem_bat_buoc),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 8, str("{:,}".format(round(pit_data.khau_tru),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 9, str("{:,}".format(round(pit_data.thu_nhap_tinh_thue),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 10, str("{:,}".format(round(pit_data.thuong),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 11, str("{:,}".format(round(pit_data.khac),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 12, str("{:,}".format(round(pit_data.cong),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 13, str("{:,}".format(round(pit_data.thue_tnct_phai_nop),0)),style_normal)
                ws_PIT.write(last_A_total_row+1+index, 14, str(pit_data.ghi_chu),style_normal)
                # Total
                ttBthu_nhap_chiu_thue += round(pit_data.thu_nhap_chiu_thue,0)
                ttBtong_tnct_khau_tru_thue += round(pit_data.tong_tnct_khau_tru_thue,0)
                ttBbao_hiem_bat_buoc += round(pit_data.bao_hiem_bat_buoc,0) 
                ttBkhau_tru += round(pit_data.khau_tru,0)
                ttBthu_nhap_tinh_thue += round(pit_data.thu_nhap_tinh_thue,0)
                ttBthuong += round(pit_data.thuong,0)
                ttBkhac += round(pit_data.khac,0)
                ttBcong += round(pit_data.cong,0)
                ttBthue_tnct_phai_nop += round(pit_data.thue_tnct_phai_nop,0)
                if pit_data.thue_tnct_phai_nop > 0:
                    ttBghichu += 1
                last_B_row = last_A_total_row+index+1
        else:
            last_B_row = last_A_row + 1
        # Total
        # Set row height
        ws_PIT.row(last_B_row+1).height_mismatch = True
        ws_PIT.row(last_B_row+1).height = 400
        # # data
        ws_PIT.write(last_B_row+1, 0, str(index+1), style_total_red)
        ws_PIT.write_merge(last_B_row+1, last_B_row+1, 1, 4, 'Tổng Cộng B', style_total_red_onlyvertcen)
        ws_PIT.write(last_B_row+1, 5, str("{:,}".format(round(ttBthu_nhap_chiu_thue),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 6, str("{:,}".format(round(ttBtong_tnct_khau_tru_thue),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 7, str("{:,}".format(round(ttBbao_hiem_bat_buoc),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 8, str("{:,}".format(round(ttBkhau_tru),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 9, str("{:,}".format(round(ttBthu_nhap_tinh_thue),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 10, str("{:,}".format(round(ttBthuong),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 11, str("{:,}".format(round(ttBkhac),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 12, str("{:,}".format(round(ttBcong),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 13, str("{:,}".format(round(ttBthue_tnct_phai_nop),0)), style_total_red)
        ws_PIT.write(last_B_row+1, 14, str(ttBghichu), style_total_red)
        last_B_total_row = last_B_row + 2
        
        # C
        ws_PIT.write(last_B_total_row, 0, 'C', style_head_11pt_bold)
        ws_PIT.write(last_B_total_row, 2, 'Cá Nhân Không Cư Trú', style_head_11pt_bold)
        for col_row in range(3,15):
            ws_PIT.write(last_B_total_row, col_row, '', style_head_11pt_bold)
        # PIT B data
        # Khai báo total
        ttCthu_nhap_chiu_thue = 0
        ttCtong_tnct_khau_tru_thue = 0
        ttCbao_hiem_bat_buoc = 0
        ttCkhau_tru = 0
        ttCthu_nhap_tinh_thue = 0
        ttCthuong = 0
        ttCkhac = 0
        ttCcong = 0
        ttCthue_tnct_phai_nop = 0
        ttCghichu = 0
        if report_pit_payroll_canhankhongcutru.exists():
            for index, pit_data in enumerate(report_pit_payroll_canhankhongcutru):
                # Set row height
                ws_PIT.row(last_B_total_row+1+index).height_mismatch = True
                ws_PIT.row(last_B_total_row+1+index).height = 400
                # Write data
                ws_PIT.write(last_B_total_row+1+index, 0, str(index+1),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 1, str(pit_data.employee.employee_code),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 2, str(pit_data.employee.full_name),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 3, str(pit_data.employee.id_card_no),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 4, str(pit_data.employee.personal_income_tax),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 5, str("{:,}".format(round(pit_data.thu_nhap_chiu_thue),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 6, str("{:,}".format(round(pit_data.tong_tnct_khau_tru_thue),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 7, str("{:,}".format(round(pit_data.bao_hiem_bat_buoc),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 8, str("{:,}".format(round(pit_data.khau_tru),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 9, str("{:,}".format(round(pit_data.thu_nhap_tinh_thue),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 10, str("{:,}".format(round(pit_data.thuong),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 11, str("{:,}".format(round(pit_data.khac),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 12, str("{:,}".format(round(pit_data.cong),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 13, str("{:,}".format(round(pit_data.thue_tnct_phai_nop),0)),style_normal)
                ws_PIT.write(last_B_total_row+1+index, 14, str(pit_data.ghi_chu),style_normal)
                # Total
                ttCthu_nhap_chiu_thue += round(pit_data.thu_nhap_chiu_thue,0)
                ttCtong_tnct_khau_tru_thue += round(pit_data.tong_tnct_khau_tru_thue,0)
                ttCbao_hiem_bat_buoc += round(pit_data.bao_hiem_bat_buoc,0) 
                ttCkhau_tru += round(pit_data.khau_tru,0)
                ttCthu_nhap_tinh_thue += round(pit_data.thu_nhap_tinh_thue,0)
                ttCthuong += round(pit_data.thuong,0)
                ttCkhac += round(pit_data.khac,0)
                ttCcong += round(pit_data.cong,0)
                ttCthue_tnct_phai_nop += round(pit_data.thue_tnct_phai_nop,0)
                if pit_data.thue_tnct_phai_nop > 0:
                    ttCghichu += 1
                last_C_row = last_B_total_row+1+index+1
        else:
            last_C_row = last_B_total_row + 1
        # Total
        # Set row height
        ws_PIT.row(last_C_row).height_mismatch = True
        ws_PIT.row(last_C_row).height = 400
        # data
        ws_PIT.write(last_C_row, 0, str(index+1), style_total_red)
        ws_PIT.write_merge(last_C_row, last_C_row, 1, 4, 'Tổng Cộng C', style_total_red_onlyvertcen)
        ws_PIT.write(last_C_row, 5, str("{:,}".format(round(ttCthu_nhap_chiu_thue),0)), style_total_red)
        ws_PIT.write(last_C_row, 6, str("{:,}".format(round(ttCtong_tnct_khau_tru_thue),0)), style_total_red)
        ws_PIT.write(last_C_row, 7, str("{:,}".format(round(ttCbao_hiem_bat_buoc),0)), style_total_red)
        ws_PIT.write(last_C_row, 8, str("{:,}".format(round(ttCkhau_tru),0)), style_total_red)
        ws_PIT.write(last_C_row, 9, str("{:,}".format(round(ttCthu_nhap_tinh_thue),0)), style_total_red)
        ws_PIT.write(last_C_row, 10, str("{:,}".format(round(ttCthuong),0)), style_total_red)
        ws_PIT.write(last_C_row, 11, str("{:,}".format(round(ttCkhac),0)), style_total_red)
        ws_PIT.write(last_C_row, 12, str("{:,}".format(round(ttCcong),0)), style_total_red)
        ws_PIT.write(last_C_row, 13, str("{:,}".format(round(ttCthue_tnct_phai_nop),0)), style_total_red)
        ws_PIT.write(last_C_row, 14, str(ttCghichu), style_total_red)
        last_C_total_row = last_C_row + 1
        
        # TOTAL A+B+C
        # Set row height
        ws_PIT.row(last_C_total_row).height_mismatch = True
        ws_PIT.row(last_C_total_row).height = 400
        # data
        ws_PIT.write(last_C_total_row, 0, str(report_pit_payroll.count() + report_pit_payroll_canhancutru.count() + report_pit_payroll_canhankhongcutru.count()), style_total_red)
        ws_PIT.write_merge(last_C_total_row, last_C_total_row, 1, 4, 'Tổng Cộng A + B + C', style_total_red_onlyvertcen)
        ws_PIT.write(last_C_total_row, 5, str("{:,}".format(round(ttAthu_nhap_chiu_thue + ttBthu_nhap_chiu_thue + ttCthu_nhap_chiu_thue),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 6, str("{:,}".format(round(ttAtong_tnct_khau_tru_thue + ttBtong_tnct_khau_tru_thue + ttCtong_tnct_khau_tru_thue),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 7, str("{:,}".format(round(ttAbao_hiem_bat_buoc + ttBbao_hiem_bat_buoc + ttCbao_hiem_bat_buoc),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 8, str("{:,}".format(round(ttAkhau_tru + ttBkhau_tru + ttCkhau_tru),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 9, str("{:,}".format(round(ttAthu_nhap_tinh_thue + ttBthu_nhap_tinh_thue + ttCthu_nhap_tinh_thue),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 10, str("{:,}".format(round(ttAthuong + ttBthuong + ttCthuong),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 11, str("{:,}".format(round(ttAkhac + ttBkhac + ttCkhac),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 12, str("{:,}".format(round(ttAcong + ttBcong + ttCcong),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 13, str("{:,}".format(round(ttAthue_tnct_phai_nop + ttBthue_tnct_phai_nop + ttCthue_tnct_phai_nop),0)), style_total_red)
        ws_PIT.write(last_C_total_row, 14, str(ttAghichu + ttBghichu + ttCghichu), style_total_red)

        
        '''Sheet Transfer Staff HCM'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_12pt_bold_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: vert center' % 'white')
        style_head_24pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 480, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert center' % 'white')
        
        # Create sheet
        ws_TransferStaff = wb.add_sheet('Transfer Staff')
        # Set col width
        ws_TransferStaff.col(0).width = 2000
        ws_TransferStaff.col(1).width = 3500
        for col in range(2,7):
            if col == 4:
                ws_TransferStaff.col(col).width = 9000
            else:
                ws_TransferStaff.col(col).width = 5000
        
        # Set row height
        ws_TransferStaff.row(0).height_mismatch = True
        ws_TransferStaff.row(0).height = 700
        ws_TransferStaff.row(1).height_mismatch = True
        ws_TransferStaff.row(1).height = 670
        ws_TransferStaff.row(2).height_mismatch = True
        ws_TransferStaff.row(2).height = 800
        ws_TransferStaff.row(3).height_mismatch = True
        ws_TransferStaff.row(3).height = 400
        ws_TransferStaff.row(4).height_mismatch = True
        ws_TransferStaff.row(4).height = 700
        # Head
        ws_TransferStaff.write(0, 3, ' TEDIS - VIET HA PHARMA JOINT STOCK COMPANY', style_head_12pt_bold_vertbot)
        ws_TransferStaff.write(1, 3, 'Lot F.2B Street No.2, Long Hau IZ, Long Hau Ward, Can Giuoc District, Long An Province', style_head_12pt_vertcen)
        ws_TransferStaff.write_merge(2, 2, 0, 6, 'SALARY TRANSFER LIST', style_head_24pt_bold)
        ws_TransferStaff.write(3, 5, 'Date:', style_11pt_horizright)
        ws_TransferStaff.write(3, 6, datetime.now().strftime('%d/%m/%Y'), style_11pt_horizleft)
        
        # Table
        # Table-head
        ws_TransferStaff.write(4, 0, 'No', style_tablehead_grey25)
        ws_TransferStaff.write(4, 1, 'Employee Code', style_tablehead_grey25)
        ws_TransferStaff.write(4, 2, 'Full Name', style_tablehead_grey25)
        ws_TransferStaff.write(4, 3, 'Bank Account No.', style_tablehead_grey25)
        ws_TransferStaff.write(4, 4, 'With Bank', style_tablehead_grey25)
        ws_TransferStaff.write(4, 5, "Bank's Address", style_tablehead_grey25)
        ws_TransferStaff.write(4, 6, 'Amount', style_tablehead_grey25)
        # Table-Body
        total_amount = 0
        for index, transfer_data in enumerate(report_transferStaff_payroll):
            # Set row height
            ws_TransferStaff.row(5+index).height_mismatch = True
            ws_TransferStaff.row(5+index).height = 650
            # Write data
            ws_TransferStaff.write(5+index, 0, str(index+1),style_tablebody)
            ws_TransferStaff.write(5+index, 1, str(transfer_data.employee.employee_code),style_tablebody_onlyvertcenter)
            ws_TransferStaff.write(5+index, 2, str(transfer_data.employee.full_name),style_tablebody_onlyvertcenter)
            ws_TransferStaff.write(5+index, 3, str(transfer_data.employee.account_no),style_tablebody_onlyvertcenter)
            ws_TransferStaff.write(5+index, 4, str(transfer_data.employee.bank) + ' - ' + str(transfer_data.employee.branch),style_tablebody_onlyvertcenter)
            ws_TransferStaff.write(5+index, 5, str(transfer_data.employee.bank_address),style_tablebody_onlyvertcenter)
            ws_TransferStaff.write(5+index, 6, str("{:,}".format(round(transfer_data.amount),0)),style_normal)
            total_amount += round(transfer_data.amount, 0)
            last_row = 5 + index + 1
        # Table-footer
        ws_TransferStaff.row(last_row).height_mismatch = True
        ws_TransferStaff.row(last_row).height = 700
        ws_TransferStaff.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_tablehead_grey25)
        ws_TransferStaff.write(last_row, 6, str("{:,}".format(round(total_amount),0)), style_tablehead_grey25) 
        # Footer
        # Set row height
        for i in range(last_row+1, last_row+6):
            if i == last_row+3:
                ws_TransferStaff.row(i).height_mismatch = True
                ws_TransferStaff.row(i).height = 2000
            else: 
                ws_TransferStaff.row(i).height_mismatch = True
                ws_TransferStaff.row(i).height = 650
        ws_TransferStaff.write(last_row+2, 5, 'Approved by', style_footer)
        ws_TransferStaff.write_merge(last_row+4, last_row+4, 4, 6, 'TÔ NGỌC CHI LAN                                                       VÕ THỊ KIM NHUNG', style_footer)
        
        
        '''Sheet Transfer COLL HCM'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_12pt_bold_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: vert center' % 'white')
        style_head_24pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 480, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert center' % 'white')
        
        # Create sheet
        ws_TransferColl = wb.add_sheet('Transfer Coll')
        # Set col width
        ws_TransferColl.col(0).width = 2000
        ws_TransferColl.col(1).width = 3500
        for col in range(2,7):
            if col == 4:
                ws_TransferColl.col(col).width = 9000
            else:
                ws_TransferColl.col(col).width = 5000
        
        # Set row height
        ws_TransferColl.row(0).height_mismatch = True
        ws_TransferColl.row(0).height = 700
        ws_TransferColl.row(1).height_mismatch = True
        ws_TransferColl.row(1).height = 670
        ws_TransferColl.row(2).height_mismatch = True
        ws_TransferColl.row(2).height = 800
        ws_TransferColl.row(3).height_mismatch = True
        ws_TransferColl.row(3).height = 400
        ws_TransferColl.row(4).height_mismatch = True
        ws_TransferColl.row(4).height = 700
        # Head
        ws_TransferColl.write(0, 3, ' TEDIS - VIET HA PHARMA JOINT STOCK COMPANY', style_head_12pt_bold_vertbot)
        ws_TransferColl.write(1, 3, 'Lot F.2B Street No.2, Long Hau IZ, Long Hau Ward, Can Giuoc District, Long An Province', style_head_12pt_vertcen)
        ws_TransferColl.write_merge(2, 2, 0, 6, 'TRANSFER LIST', style_head_24pt_bold)
        ws_TransferColl.write(3, 5, 'Date:', style_11pt_horizright)
        ws_TransferColl.write(3, 6, datetime.now().strftime('%d/%m/%Y'), style_11pt_horizleft)
        
        # Table
        # Table-head
        ws_TransferColl.write(4, 0, 'No', style_tablehead_grey25)
        ws_TransferColl.write(4, 1, 'Employee Code', style_tablehead_grey25)
        ws_TransferColl.write(4, 2, 'Full Name', style_tablehead_grey25)
        ws_TransferColl.write(4, 3, 'Bank Account No.', style_tablehead_grey25)
        ws_TransferColl.write(4, 4, 'With Bank', style_tablehead_grey25)
        ws_TransferColl.write(4, 5, "Bank's Address", style_tablehead_grey25)
        ws_TransferColl.write(4, 6, 'Amount', style_tablehead_grey25)
        # Table-Body
        total_amount = 0
        for index, transfer_data in enumerate(report_transferColl_payroll):
            # Set row height
            ws_TransferColl.row(5+index).height_mismatch = True
            ws_TransferColl.row(5+index).height = 650
            # Write data
            ws_TransferColl.write(5+index, 0, str(index+1),style_tablebody)
            ws_TransferColl.write(5+index, 1, str(transfer_data.employee.employee_code),style_tablebody_onlyvertcenter)
            ws_TransferColl.write(5+index, 2, str(transfer_data.employee.full_name),style_tablebody_onlyvertcenter)
            ws_TransferColl.write(5+index, 3, str(transfer_data.employee.account_no),style_tablebody_onlyvertcenter)
            ws_TransferColl.write(5+index, 4, str(transfer_data.employee.bank) + ' - ' + str(transfer_data.employee.branch),style_tablebody_onlyvertcenter)
            ws_TransferColl.write(5+index, 5, str(transfer_data.employee.bank_address),style_tablebody_onlyvertcenter)
            ws_TransferColl.write(5+index, 6, str("{:,}".format(round(transfer_data.amount),0)),style_normal)
            total_amount += round(transfer_data.amount, 0)
            last_row = 5 + index + 1
        # Table-footer
        ws_TransferColl.row(last_row).height_mismatch = True
        ws_TransferColl.row(last_row).height = 700
        ws_TransferColl.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_tablehead_grey25)
        ws_TransferColl.write(last_row, 6, str("{:,}".format(round(total_amount),0)), style_tablehead_grey25) 
        # Footer
        # Set row height
        for i in range(last_row+1, last_row+6):
            if i == last_row+3:
                ws_TransferColl.row(i).height_mismatch = True
                ws_TransferColl.row(i).height = 2000
            else: 
                ws_TransferColl.row(i).height_mismatch = True
                ws_TransferColl.row(i).height = 650
        ws_TransferColl.write(last_row+2, 5, 'Approved by', style_footer)
        ws_TransferColl.write_merge(last_row+4, last_row+4, 4, 6, 'TÔ NGỌC CHI LAN                                                       VÕ THỊ KIM NHUNG', style_footer)
        
        
        '''Sheet Payroll Staff'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_12pt_bold_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertbot_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: horiz right,vert bottom' % 'white')
        style_head_12pt_vertbot_horizright.alignment.wrap = 1
        style_head_26pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 520, name Arial, colour black; align: vert bottom' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer_10pt_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_vertcen_horizleft.alignment.wrap = 1
        style_footer_10pt_bold_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_bold_vertcen_horizleft.alignment.wrap = 1
        
        # Create sheet
        ws_PayrollStaff = wb.add_sheet('Payroll Staff')


        # Set col width
        for col in range(0,42):
            if col == 0:
                ws_PayrollStaff.col(col).width = 1500
            elif col == 1:
                ws_PayrollStaff.col(col).width = 3000
            elif col == 2:
                ws_PayrollStaff.col(col).width = 7000
            elif col == 7:
                ws_PayrollStaff.col(col).width = 3000
            elif col == 8:
                ws_PayrollStaff.col(col).width = 3000
            else:
                ws_PayrollStaff.col(col).width = 5000
        
        # Set row height
        ws_PayrollStaff.row(0).height_mismatch = True
        ws_PayrollStaff.row(0).height = 1300
        ws_PayrollStaff.row(1).height_mismatch = True
        ws_PayrollStaff.row(1).height = 500
        ws_PayrollStaff.row(2).height_mismatch = True
        ws_PayrollStaff.row(2).height = 500
        ws_PayrollStaff.row(3).height_mismatch = True
        ws_PayrollStaff.row(3).height = 600
        ws_PayrollStaff.row(4).height_mismatch = True
        ws_PayrollStaff.row(4).height = 1500
        # Head
        ws_PayrollStaff.write(0, 5, 'PAYROLL IN ' + str(period_month.month_name), style_head_26pt_bold)
        ws_PayrollStaff.write_merge(1, 1, 5, 7, 'Working days of BO: ' + str(working_day_bo), style_head_12pt_vertbot_horizright)
        ws_PayrollStaff.write_merge(2, 2, 5, 7, 'Working days of WH: ' + str(working_day_wh), style_head_12pt_vertbot_horizright)
        
        # Table
        # Table-head
        ws_PayrollStaff.write(4, 0, 'No.', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 1, 'Employee code', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 2, 'Full name', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 3, 'Joining Date', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 4, 'Department', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 5, 'Title', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 6, 'Salary ' + str(period_month.period.period_year) + ' (VND)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 7, 'Working days', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 8, '% Adjust', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 9, 'Gross Income', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 10, 'Transportation', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 11, 'Phone', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 12, 'Lunch', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 13, 'Travel', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 14, 'Responsibility', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 15, 'Seniority Bonus', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 16, 'Others', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 17, 'Outstanding annual leave', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 18, 'OTC Incentive', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 19, 'KPI Achievement', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 20, '13th salary (pro-rata)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 21, 'Incentive last month', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 22, 'Incentive last quarter', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 23, 'Taxable Overtime', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 24, 'Non Taxable Overtime', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 25, 'SHUI(10.5%)(Employee pay)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 26, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 27, 'SHUI(21.5%)(Company pay)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 28, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 29, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 30, 'Trade Union fee (Company pay)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 31, 'Trade Union fee (Employee pay)', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 32, 'Family deduction', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 33, 'Taxable Income', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 34, 'Taxed Income', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 35, 'PIT 13th salary', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 36, 'PIT', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 37, 'PIT balance', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 38, '1st payment', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 39, 'Net Income', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 40, 'Transfer Bank', style_tablehead_grey25)
        ws_PayrollStaff.write(4, 41, 'Total Cost', style_tablehead_grey25)
        # Table-Body
        # Create total var
        ttnewest_salary = 0
        ttgross_income = 0
        tttransportation = 0
        ttphone = 0
        ttlunch = 0
        tttravel = 0
        ttresponsibility = 0
        ttseniority_bonus = 0
        ttother = 0
        ttoutstanding_annual_leave = 0
        ttOTC_incentive = 0
        ttKPI_achievement = 0
        ttmonth_13_salary_Pro_ata = 0
        ttincentive_last_month = 0
        ttincentive_last_quy_last_year = 0
        tttaxable_overtime = 0
        ttnontaxable_overtime = 0
        ttSHUI_10point5percent_employee_pay = 0
        ttrecuperation_of_SHU_Ins_10point5percent_staff_pay = 0
        ttSHUI_21point5percent_company_pay = 0
        ttrecuperation_of_SHU_Ins_21point5percent_company_pay = 0
        ttoccupational_accident_and_disease = 0
        tttrade_union_fee_company_pay = 0
        tttrade_union_fee_employee_pay = 0
        ttfamily_deduction = 0
        tttaxable_income = 0
        tttaxed_income = 0
        ttPIT_13th_salary = 0
        ttPIT = 0
        ttPIT_balance = 0
        ttfirst_payment = 0
        ttnet_income = 0
        tttransfer_bank = 0
        tttotal_cost = 0
        for index, data in enumerate(list_payroll_staff_info):
            # Set row height
            ws_PayrollStaff.row(5+index).height_mismatch = True
            ws_PayrollStaff.row(5+index).height = 500
            # Write data
            ws_PayrollStaff.write(5+index, 0, str(index+1),style_normal)
            ws_PayrollStaff.write(5+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws_PayrollStaff.write(5+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws_PayrollStaff.write(5+index, 3, str(data['payroll_info'].employee.joining_date.strftime('%d/%m/%Y')),style_normal)
            ws_PayrollStaff.write(5+index, 4, str(data['payroll_info'].employee.department_e),style_normal)
            ws_PayrollStaff.write(5+index, 5, str(data['payroll_info'].employee.position_e),style_normal)
            ws_PayrollStaff.write(5+index, 6, str("{:,}".format(round(data['payroll_info'].newest_salary))),style_normal)
            ws_PayrollStaff.write(5+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws_PayrollStaff.write(5+index, 8, str(round(data['payroll_info'].adjust_percent)) + '%',style_normal)
            ws_PayrollStaff.write(5+index, 9, str("{:,}".format(round(data['payroll_info'].gross_income))),style_normal)
            ws_PayrollStaff.write(5+index, 10, str("{:,}".format(round(data['payroll_info'].transportation))),style_normal)
            ws_PayrollStaff.write(5+index, 11, str("{:,}".format(round(data['payroll_info'].phone))),style_normal)
            ws_PayrollStaff.write(5+index, 12, str("{:,}".format(round(data['payroll_info'].lunch))),style_normal)
            ws_PayrollStaff.write(5+index, 13, str("{:,}".format(round(data['payroll_info'].travel))),style_normal)
            ws_PayrollStaff.write(5+index, 14, str("{:,}".format(round(data['payroll_info'].responsibility))),style_normal)
            ws_PayrollStaff.write(5+index, 15, str("{:,}".format(round(data['payroll_info'].seniority_bonus))),style_normal)
            ws_PayrollStaff.write(5+index, 16, str("{:,}".format(round(data['payroll_info'].other))),style_normal)
            ws_PayrollStaff.write(5+index, 17, str("{:,}".format(round(data['payroll_info'].outstanding_annual_leave))),style_normal)
            ws_PayrollStaff.write(5+index, 18, str("{:,}".format(round(data['payroll_info'].OTC_incentive))),style_normal)
            ws_PayrollStaff.write(5+index, 19, str("{:,}".format(round(data['payroll_info'].KPI_achievement))),style_normal)
            ws_PayrollStaff.write(5+index, 20, str("{:,}".format(round(data['payroll_info'].month_13_salary_Pro_ata))),style_normal)
            ws_PayrollStaff.write(5+index, 21, str("{:,}".format(round(data['payroll_info'].incentive_last_month))),style_normal)
            ws_PayrollStaff.write(5+index, 22, str("{:,}".format(round(data['payroll_info'].incentive_last_quy_last_year))),style_normal)
            ws_PayrollStaff.write(5+index, 23, str("{:,}".format(round(data['payroll_info'].taxable_overtime))),style_normal)
            ws_PayrollStaff.write(5+index, 24, str("{:,}".format(round(data['payroll_info'].nontaxable_overtime))),style_normal)
            ws_PayrollStaff.write(5+index, 25, str("{:,}".format(round(data['payroll_info'].SHUI_10point5percent_employee_pay))),style_normal)
            ws_PayrollStaff.write(5+index, 26, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay))),style_normal)
            ws_PayrollStaff.write(5+index, 27, str("{:,}".format(round(data['payroll_info'].SHUI_21point5percent_company_pay))),style_normal)
            ws_PayrollStaff.write(5+index, 28, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay))),style_normal)
            ws_PayrollStaff.write(5+index, 29, str("{:,}".format(round(data['payroll_info'].occupational_accident_and_disease))),style_normal)
            ws_PayrollStaff.write(5+index, 30, str("{:,}".format(round(data['payroll_info'].trade_union_fee_company_pay))),style_normal)
            ws_PayrollStaff.write(5+index, 31, str("{:,}".format(round(data['payroll_info'].trade_union_fee_employee_pay))),style_normal)
            ws_PayrollStaff.write(5+index, 32, str("{:,}".format(round(data['payroll_info'].family_deduction))),style_normal)
            ws_PayrollStaff.write(5+index, 33, str("{:,}".format(round(data['payroll_info'].taxable_income))),style_normal)
            ws_PayrollStaff.write(5+index, 34, str("{:,}".format(round(data['payroll_info'].taxed_income))),style_normal)
            ws_PayrollStaff.write(5+index, 35, str("{:,}".format(round(data['payroll_info'].PIT_13th_salary))),style_normal)
            ws_PayrollStaff.write(5+index, 36, str("{:,}".format(round(data['payroll_info'].PIT))),style_normal)
            ws_PayrollStaff.write(5+index, 37, str("{:,}".format(round(data['payroll_info'].PIT_balance))),style_normal)
            ws_PayrollStaff.write(5+index, 38, str("{:,}".format(round(data['payroll_info'].first_payment))),style_normal)
            ws_PayrollStaff.write(5+index, 39, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws_PayrollStaff.write(5+index, 40, str("{:,}".format(round(data['payroll_info'].transfer_bank))),style_normal)
            ws_PayrollStaff.write(5+index, 41, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 5 + index + 1
            ttnewest_salary += data['payroll_info'].newest_salary
            ttgross_income += data['payroll_info'].gross_income
            tttransportation += data['payroll_info'].transportation
            ttphone += data['payroll_info'].phone
            ttlunch += data['payroll_info'].lunch
            tttravel += data['payroll_info'].travel
            ttresponsibility += data['payroll_info'].responsibility
            ttseniority_bonus += data['payroll_info'].seniority_bonus
            ttother += data['payroll_info'].other
            ttoutstanding_annual_leave += data['payroll_info'].outstanding_annual_leave
            ttOTC_incentive += data['payroll_info'].OTC_incentive
            ttKPI_achievement += data['payroll_info'].KPI_achievement
            ttmonth_13_salary_Pro_ata += data['payroll_info'].month_13_salary_Pro_ata
            ttincentive_last_month += data['payroll_info'].incentive_last_month
            ttincentive_last_quy_last_year += data['payroll_info'].incentive_last_quy_last_year
            tttaxable_overtime += data['payroll_info'].taxable_overtime
            ttnontaxable_overtime += data['payroll_info'].nontaxable_overtime
            ttSHUI_10point5percent_employee_pay += data['payroll_info'].SHUI_10point5percent_employee_pay
            ttrecuperation_of_SHU_Ins_10point5percent_staff_pay += data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay
            ttSHUI_21point5percent_company_pay += data['payroll_info'].SHUI_21point5percent_company_pay
            ttrecuperation_of_SHU_Ins_21point5percent_company_pay += data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay
            ttoccupational_accident_and_disease += data['payroll_info'].occupational_accident_and_disease
            tttrade_union_fee_company_pay += data['payroll_info'].trade_union_fee_company_pay
            tttrade_union_fee_employee_pay += data['payroll_info'].trade_union_fee_employee_pay
            ttfamily_deduction += data['payroll_info'].family_deduction
            tttaxable_income += data['payroll_info'].taxable_income
            tttaxed_income += data['payroll_info'].taxed_income
            ttPIT_13th_salary += data['payroll_info'].PIT_13th_salary
            ttPIT += data['payroll_info'].PIT
            ttPIT_balance += data['payroll_info'].PIT_balance
            ttfirst_payment += data['payroll_info'].first_payment
            ttnet_income += data['payroll_info'].net_income
            tttransfer_bank += data['payroll_info'].transfer_bank
            tttotal_cost += data['payroll_info'].total_cost
        # Table-footer
        # Set row height
        ws_PayrollStaff.row(last_row).height_mismatch = True
        ws_PayrollStaff.row(last_row).height = 1000
        # Total line in bottom of table 
        ws_PayrollStaff.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 6, str("{:,}".format(round(ttnewest_salary))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 7, '-',style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 8, '-',style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 9, str("{:,}".format(round(ttgross_income))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 10, str("{:,}".format(round(tttransportation))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 11, str("{:,}".format(round(ttphone))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 12, str("{:,}".format(round(ttlunch))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 13, str("{:,}".format(round(tttravel))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 14, str("{:,}".format(round(ttresponsibility))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 15, str("{:,}".format(round(ttseniority_bonus))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 16, str("{:,}".format(round(ttother))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 17, str("{:,}".format(round(ttoutstanding_annual_leave))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 18, str("{:,}".format(round(ttOTC_incentive))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 19, str("{:,}".format(round(ttKPI_achievement))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 20, str("{:,}".format(round(ttmonth_13_salary_Pro_ata))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 21, str("{:,}".format(round(ttincentive_last_month))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 22, str("{:,}".format(round(ttincentive_last_quy_last_year))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 23, str("{:,}".format(round(tttaxable_overtime))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 24, str("{:,}".format(round(ttnontaxable_overtime))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 25, str("{:,}".format(round(ttSHUI_10point5percent_employee_pay))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 26, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 27, str("{:,}".format(round(ttSHUI_21point5percent_company_pay))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 28, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_21point5percent_company_pay))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 29, str("{:,}".format(round(ttoccupational_accident_and_disease))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 30, str("{:,}".format(round(tttrade_union_fee_company_pay))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 31, str("{:,}".format(round(tttrade_union_fee_employee_pay))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 32, str("{:,}".format(round(ttfamily_deduction))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 33, str("{:,}".format(round(tttaxable_income))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 34, str("{:,}".format(round(tttaxed_income))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 35, str("{:,}".format(round(ttPIT_13th_salary))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 36, str("{:,}".format(round(ttPIT))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 37, str("{:,}".format(round(ttPIT_balance))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 38, str("{:,}".format(round(ttfirst_payment))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 39, str("{:,}".format(round(ttnet_income))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 40, str("{:,}".format(round(tttransfer_bank))),style_tablehead_grey25)
        ws_PayrollStaff.write(last_row, 41, str("{:,}".format(round(tttotal_cost))),style_tablehead_grey25)
        # Footer
        # Set row height
        for i in range(last_row+6, last_row+10):
            if i == last_row+7:
                ws_PayrollStaff.row(i).height_mismatch = True
                ws_PayrollStaff.row(i).height = 2000
            else: 
                ws_PayrollStaff.row(i).height_mismatch = True
                ws_PayrollStaff.row(i).height = 500
        ws_PayrollStaff.write_merge(last_row+6, last_row+6, 5, 8, 'Prepared by', style_footer_10pt_vertcen_horizleft)
        ws_PayrollStaff.write_merge(last_row+8, last_row+8, 5, 8, 'Le Thi Thanh Tuyen', style_footer_10pt_bold_vertcen_horizleft)
        ws_PayrollStaff.write_merge(last_row+9, last_row+9, 5, 8, datetime.now().strftime('%d/%m/%Y'), style_footer_10pt_vertcen_horizleft)
        
        
        '''Sheet Payroll Coll'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_12pt_bold_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertbot_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: horiz right,vert bottom' % 'white')
        style_head_12pt_vertbot_horizright.alignment.wrap = 1
        style_head_26pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 520, name Arial, colour black; align: vert bottom' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer_10pt_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_vertcen_horizleft.alignment.wrap = 1
        style_footer_10pt_bold_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_bold_vertcen_horizleft.alignment.wrap = 1
        
        # Create sheet
        ws_PayrollColl = wb.add_sheet('Payroll Coll')
        # Set col width
        for col in range(0,42):
            if col == 0:
                ws_PayrollColl.col(col).width = 1500
            elif col == 1:
                ws_PayrollColl.col(col).width = 3000
            elif col == 2:
                ws_PayrollColl.col(col).width = 7000
            elif col == 7:
                ws_PayrollColl.col(col).width = 3000
            elif col == 8:
                ws_PayrollColl.col(col).width = 3000
            else:
                ws_PayrollColl.col(col).width = 5000
        
        # Set row height
        ws_PayrollColl.row(0).height_mismatch = True
        ws_PayrollColl.row(0).height = 1300
        ws_PayrollColl.row(1).height_mismatch = True
        ws_PayrollColl.row(1).height = 500
        ws_PayrollColl.row(2).height_mismatch = True
        ws_PayrollColl.row(2).height = 500
        ws_PayrollColl.row(3).height_mismatch = True
        ws_PayrollColl.row(3).height = 600
        ws_PayrollColl.row(4).height_mismatch = True
        ws_PayrollColl.row(4).height = 1500
        # Head
        ws_PayrollColl.write(0, 5, 'PAYROLL IN ' + str(period_month.month_name), style_head_26pt_bold)
        ws_PayrollColl.write_merge(1, 1, 5, 7, 'Working days of BO: ' + str(working_day_bo), style_head_12pt_vertbot_horizright)
        ws_PayrollColl.write_merge(2, 2, 5, 7, 'Working days of WH: ' + str(working_day_wh), style_head_12pt_vertbot_horizright)
        
        # Table
        # Table-head
        ws_PayrollColl.write(4, 0, 'No.', style_tablehead_grey25)
        ws_PayrollColl.write(4, 1, 'Employee code', style_tablehead_grey25)
        ws_PayrollColl.write(4, 2, 'Full name', style_tablehead_grey25)
        ws_PayrollColl.write(4, 3, 'Joining Date', style_tablehead_grey25)
        ws_PayrollColl.write(4, 4, 'Department', style_tablehead_grey25)
        ws_PayrollColl.write(4, 5, 'Title', style_tablehead_grey25)
        ws_PayrollColl.write(4, 6, 'Salary ' + str(period_month.period.period_year) + ' (VND)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 7, 'Working days', style_tablehead_grey25)
        ws_PayrollColl.write(4, 8, '% Adjust', style_tablehead_grey25)
        ws_PayrollColl.write(4, 9, 'Gross Income', style_tablehead_grey25)
        ws_PayrollColl.write(4, 10, 'Transportation', style_tablehead_grey25)
        ws_PayrollColl.write(4, 11, 'Phone', style_tablehead_grey25)
        ws_PayrollColl.write(4, 12, 'Lunch', style_tablehead_grey25)
        ws_PayrollColl.write(4, 13, 'Travel', style_tablehead_grey25)
        ws_PayrollColl.write(4, 14, 'Responsibility', style_tablehead_grey25)
        ws_PayrollColl.write(4, 15, 'Seniority Bonus', style_tablehead_grey25)
        ws_PayrollColl.write(4, 16, 'Others', style_tablehead_grey25)
        ws_PayrollColl.write(4, 17, 'Outstanding annual leave', style_tablehead_grey25)
        ws_PayrollColl.write(4, 18, 'OTC Incentive', style_tablehead_grey25)
        ws_PayrollColl.write(4, 19, 'KPI Achievement', style_tablehead_grey25)
        ws_PayrollColl.write(4, 20, '13th salary (pro-rata)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 21, 'Incentive last month', style_tablehead_grey25)
        ws_PayrollColl.write(4, 22, 'Incentive last quarter', style_tablehead_grey25)
        ws_PayrollColl.write(4, 23, 'Taxable Overtime', style_tablehead_grey25)
        ws_PayrollColl.write(4, 24, 'Non Taxable Overtime', style_tablehead_grey25)
        ws_PayrollColl.write(4, 25, 'SHUI(10.5%)(Employee pay)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 26, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 27, 'SHUI(21.5%)(Company pay)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 28, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 29, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 30, 'Trade Union fee (Company pay)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 31, 'Trade Union fee (Employee pay)', style_tablehead_grey25)
        ws_PayrollColl.write(4, 32, 'Family deduction', style_tablehead_grey25)
        ws_PayrollColl.write(4, 33, 'Taxable Income', style_tablehead_grey25)
        ws_PayrollColl.write(4, 34, 'Taxed Income', style_tablehead_grey25)
        ws_PayrollColl.write(4, 35, 'PIT 13th salary', style_tablehead_grey25)
        ws_PayrollColl.write(4, 36, 'PIT', style_tablehead_grey25)
        ws_PayrollColl.write(4, 37, 'PIT balance', style_tablehead_grey25)
        ws_PayrollColl.write(4, 38, '1st payment', style_tablehead_grey25)
        ws_PayrollColl.write(4, 39, 'Net Income', style_tablehead_grey25)
        ws_PayrollColl.write(4, 40, 'Transfer Bank', style_tablehead_grey25)
        ws_PayrollColl.write(4, 41, 'Total Cost', style_tablehead_grey25)
        # Table-Body
        # Create total var
        ttnewest_salary = 0
        ttgross_income = 0
        tttransportation = 0
        ttphone = 0
        ttlunch = 0
        tttravel = 0
        ttresponsibility = 0
        ttseniority_bonus = 0
        ttother = 0
        ttoutstanding_annual_leave = 0
        ttOTC_incentive = 0
        ttKPI_achievement = 0
        ttmonth_13_salary_Pro_ata = 0
        ttincentive_last_month = 0
        ttincentive_last_quy_last_year = 0
        tttaxable_overtime = 0
        ttnontaxable_overtime = 0
        ttSHUI_10point5percent_employee_pay = 0
        ttrecuperation_of_SHU_Ins_10point5percent_staff_pay = 0
        ttSHUI_21point5percent_company_pay = 0
        ttrecuperation_of_SHU_Ins_21point5percent_company_pay = 0
        ttoccupational_accident_and_disease = 0
        tttrade_union_fee_company_pay = 0
        tttrade_union_fee_employee_pay = 0
        ttfamily_deduction = 0
        tttaxable_income = 0
        tttaxed_income = 0
        ttPIT_13th_salary = 0
        ttPIT = 0
        ttPIT_balance = 0
        ttfirst_payment = 0
        ttnet_income = 0
        tttransfer_bank = 0
        tttotal_cost = 0
        for index, data in enumerate(list_payroll_coll_info):
            # Set row height
            ws_PayrollColl.row(5+index).height_mismatch = True
            ws_PayrollColl.row(5+index).height = 500
            # Write data
            ws_PayrollColl.write(5+index, 0, str(index+1),style_normal)
            ws_PayrollColl.write(5+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws_PayrollColl.write(5+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws_PayrollColl.write(5+index, 3, str(data['payroll_info'].employee.joining_date.strftime('%d/%m/%Y')),style_normal)
            ws_PayrollColl.write(5+index, 4, str(data['payroll_info'].employee.department_e),style_normal)
            ws_PayrollColl.write(5+index, 5, str(data['payroll_info'].employee.position_e),style_normal)
            ws_PayrollColl.write(5+index, 6, str("{:,}".format(round(data['payroll_info'].newest_salary))),style_normal)
            ws_PayrollColl.write(5+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws_PayrollColl.write(5+index, 8, str(round(data['payroll_info'].adjust_percent)) + '%',style_normal)
            ws_PayrollColl.write(5+index, 9, str("{:,}".format(round(data['payroll_info'].gross_income))),style_normal)
            ws_PayrollColl.write(5+index, 10, str("{:,}".format(round(data['payroll_info'].transportation))),style_normal)
            ws_PayrollColl.write(5+index, 11, str("{:,}".format(round(data['payroll_info'].phone))),style_normal)
            ws_PayrollColl.write(5+index, 12, str("{:,}".format(round(data['payroll_info'].lunch))),style_normal)
            ws_PayrollColl.write(5+index, 13, str("{:,}".format(round(data['payroll_info'].travel))),style_normal)
            ws_PayrollColl.write(5+index, 14, str("{:,}".format(round(data['payroll_info'].responsibility))),style_normal)
            ws_PayrollColl.write(5+index, 15, str("{:,}".format(round(data['payroll_info'].seniority_bonus))),style_normal)
            ws_PayrollColl.write(5+index, 16, str("{:,}".format(round(data['payroll_info'].other))),style_normal)
            ws_PayrollColl.write(5+index, 17, str("{:,}".format(round(data['payroll_info'].outstanding_annual_leave))),style_normal)
            ws_PayrollColl.write(5+index, 18, str("{:,}".format(round(data['payroll_info'].OTC_incentive))),style_normal)
            ws_PayrollColl.write(5+index, 19, str("{:,}".format(round(data['payroll_info'].KPI_achievement))),style_normal)
            ws_PayrollColl.write(5+index, 20, str("{:,}".format(round(data['payroll_info'].month_13_salary_Pro_ata))),style_normal)
            ws_PayrollColl.write(5+index, 21, str("{:,}".format(round(data['payroll_info'].incentive_last_month))),style_normal)
            ws_PayrollColl.write(5+index, 22, str("{:,}".format(round(data['payroll_info'].incentive_last_quy_last_year))),style_normal)
            ws_PayrollColl.write(5+index, 23, str("{:,}".format(round(data['payroll_info'].taxable_overtime))),style_normal)
            ws_PayrollColl.write(5+index, 24, str("{:,}".format(round(data['payroll_info'].nontaxable_overtime))),style_normal)
            ws_PayrollColl.write(5+index, 25, str("{:,}".format(round(data['payroll_info'].SHUI_10point5percent_employee_pay))),style_normal)
            ws_PayrollColl.write(5+index, 26, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay))),style_normal)
            ws_PayrollColl.write(5+index, 27, str("{:,}".format(round(data['payroll_info'].SHUI_21point5percent_company_pay))),style_normal)
            ws_PayrollColl.write(5+index, 28, str("{:,}".format(round(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay))),style_normal)
            ws_PayrollColl.write(5+index, 29, str("{:,}".format(round(data['payroll_info'].occupational_accident_and_disease))),style_normal)
            ws_PayrollColl.write(5+index, 30, str("{:,}".format(round(data['payroll_info'].trade_union_fee_company_pay))),style_normal)
            ws_PayrollColl.write(5+index, 31, str("{:,}".format(round(data['payroll_info'].trade_union_fee_employee_pay))),style_normal)
            ws_PayrollColl.write(5+index, 32, str("{:,}".format(round(data['payroll_info'].family_deduction))),style_normal)
            ws_PayrollColl.write(5+index, 33, str("{:,}".format(round(data['payroll_info'].taxable_income))),style_normal)
            ws_PayrollColl.write(5+index, 34, str("{:,}".format(round(data['payroll_info'].taxed_income))),style_normal)
            ws_PayrollColl.write(5+index, 35, str("{:,}".format(round(data['payroll_info'].PIT_13th_salary))),style_normal)
            ws_PayrollColl.write(5+index, 36, str("{:,}".format(round(data['payroll_info'].PIT))),style_normal)
            ws_PayrollColl.write(5+index, 37, str("{:,}".format(round(data['payroll_info'].PIT_balance))),style_normal)
            ws_PayrollColl.write(5+index, 38, str("{:,}".format(round(data['payroll_info'].first_payment))),style_normal)
            ws_PayrollColl.write(5+index, 39, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws_PayrollColl.write(5+index, 40, str("{:,}".format(round(data['payroll_info'].transfer_bank))),style_normal)
            ws_PayrollColl.write(5+index, 41, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 5 + index + 1
            ttnewest_salary += data['payroll_info'].newest_salary
            ttgross_income += data['payroll_info'].gross_income
            tttransportation += data['payroll_info'].transportation
            ttphone += data['payroll_info'].phone
            ttlunch += data['payroll_info'].lunch
            tttravel += data['payroll_info'].travel
            ttresponsibility += data['payroll_info'].responsibility
            ttseniority_bonus += data['payroll_info'].seniority_bonus
            ttother += data['payroll_info'].other
            ttoutstanding_annual_leave += data['payroll_info'].outstanding_annual_leave
            ttOTC_incentive += data['payroll_info'].OTC_incentive
            ttKPI_achievement += data['payroll_info'].KPI_achievement
            ttmonth_13_salary_Pro_ata += data['payroll_info'].month_13_salary_Pro_ata
            ttincentive_last_month += data['payroll_info'].incentive_last_month
            ttincentive_last_quy_last_year += data['payroll_info'].incentive_last_quy_last_year
            tttaxable_overtime += data['payroll_info'].taxable_overtime
            ttnontaxable_overtime += data['payroll_info'].nontaxable_overtime
            ttSHUI_10point5percent_employee_pay += data['payroll_info'].SHUI_10point5percent_employee_pay
            ttrecuperation_of_SHU_Ins_10point5percent_staff_pay += data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay
            ttSHUI_21point5percent_company_pay += data['payroll_info'].SHUI_21point5percent_company_pay
            ttrecuperation_of_SHU_Ins_21point5percent_company_pay += data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay
            ttoccupational_accident_and_disease += data['payroll_info'].occupational_accident_and_disease
            tttrade_union_fee_company_pay += data['payroll_info'].trade_union_fee_company_pay
            tttrade_union_fee_employee_pay += data['payroll_info'].trade_union_fee_employee_pay
            ttfamily_deduction += data['payroll_info'].family_deduction
            tttaxable_income += data['payroll_info'].taxable_income
            tttaxed_income += data['payroll_info'].taxed_income
            ttPIT_13th_salary += data['payroll_info'].PIT_13th_salary
            ttPIT += data['payroll_info'].PIT
            ttPIT_balance += data['payroll_info'].PIT_balance
            ttfirst_payment += data['payroll_info'].first_payment
            ttnet_income += data['payroll_info'].net_income
            tttransfer_bank += data['payroll_info'].transfer_bank
            tttotal_cost += data['payroll_info'].total_cost
        # Table-footer
        # Set row height
        ws_PayrollColl.row(last_row).height_mismatch = True
        ws_PayrollColl.row(last_row).height = 1000
        # Total line in bottom of table 
        ws_PayrollColl.write_merge(last_row, last_row, 0, 5, 'TOTAL', style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 6, str("{:,}".format(round(ttnewest_salary))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 7, '-',style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 8, '-',style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 9, str("{:,}".format(round(ttgross_income))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 10, str("{:,}".format(round(tttransportation))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 11, str("{:,}".format(round(ttphone))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 12, str("{:,}".format(round(ttlunch))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 13, str("{:,}".format(round(tttravel))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 14, str("{:,}".format(round(ttresponsibility))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 15, str("{:,}".format(round(ttseniority_bonus))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 16, str("{:,}".format(round(ttother))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 17, str("{:,}".format(round(ttoutstanding_annual_leave))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 18, str("{:,}".format(round(ttOTC_incentive))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 19, str("{:,}".format(round(ttKPI_achievement))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 20, str("{:,}".format(round(ttmonth_13_salary_Pro_ata))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 21, str("{:,}".format(round(ttincentive_last_month))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 22, str("{:,}".format(round(ttincentive_last_quy_last_year))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 23, str("{:,}".format(round(tttaxable_overtime))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 24, str("{:,}".format(round(ttnontaxable_overtime))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 25, str("{:,}".format(round(ttSHUI_10point5percent_employee_pay))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 26, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 27, str("{:,}".format(round(ttSHUI_21point5percent_company_pay))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 28, str("{:,}".format(round(ttrecuperation_of_SHU_Ins_21point5percent_company_pay))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 29, str("{:,}".format(round(ttoccupational_accident_and_disease))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 30, str("{:,}".format(round(tttrade_union_fee_company_pay))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 31, str("{:,}".format(round(tttrade_union_fee_employee_pay))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 32, str("{:,}".format(round(ttfamily_deduction))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 33, str("{:,}".format(round(tttaxable_income))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 34, str("{:,}".format(round(tttaxed_income))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 35, str("{:,}".format(round(ttPIT_13th_salary))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 36, str("{:,}".format(round(ttPIT))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 37, str("{:,}".format(round(ttPIT_balance))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 38, str("{:,}".format(round(ttfirst_payment))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 39, str("{:,}".format(round(ttnet_income))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 40, str("{:,}".format(round(tttransfer_bank))),style_tablehead_grey25)
        ws_PayrollColl.write(last_row, 41, str("{:,}".format(round(tttotal_cost))),style_tablehead_grey25)
        # Footer
        # Set row height
        for i in range(last_row+6, last_row+10):
            if i == last_row+7:
                ws_PayrollColl.row(i).height_mismatch = True
                ws_PayrollColl.row(i).height = 2000
            else: 
                ws_PayrollColl.row(i).height_mismatch = True
                ws_PayrollColl.row(i).height = 500
        ws_PayrollColl.write_merge(last_row+6, last_row+6, 5, 8, 'Prepared by', style_footer_10pt_vertcen_horizleft)
        ws_PayrollColl.write_merge(last_row+8, last_row+8, 5, 8, 'Le Thi Thanh Tuyen', style_footer_10pt_bold_vertcen_horizleft)
        ws_PayrollColl.write_merge(last_row+9, last_row+9, 5, 8, datetime.now().strftime('%d/%m/%Y'), style_footer_10pt_vertcen_horizleft)
        ws_PayrollColl.write(last_row+6, 23, 'Approved by',style_footer_10pt_vertcen_horizleft)
        ws_PayrollColl.write(last_row+8, 23, 'Nguyen Minh Son',style_footer_10pt_bold_vertcen_horizleft)
        
        
        '''Sheet Payroll Coll (print)'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head_11pt_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertbot_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: horiz right,vert bottom' % 'white')
        style_head_12pt_vertbot_horizright.alignment.wrap = 1
        style_head_16pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 320, name Arial, colour black; align: horiz left, vert bottom' % 'white')
        style_head_20pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 400, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer_bold_10pt_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_bold_10pt_vertcen_horizleft.alignment.wrap = 1
        style_footer_10pt_bold_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_bold_vertcen_horizleft.alignment.wrap = 1
        
        # Create sheet
        ws_PayrollColl_print = wb.add_sheet('Payroll Coll (print)')
        # Set col width
        for col in range(0,7):
            if col == 0:
                ws_PayrollColl_print.col(col).width = 3000
            elif col == 1:
                ws_PayrollColl_print.col(col).width = 5000
            elif col == 2:
                ws_PayrollColl_print.col(col).width = 7000
            else:
                ws_PayrollColl_print.col(col).width = 5000
        
        # Set row height
        ws_PayrollColl_print.row(0).height_mismatch = True
        ws_PayrollColl_print.row(0).height = 1100
        ws_PayrollColl_print.row(1).height_mismatch = True
        ws_PayrollColl_print.row(1).height = 650
        ws_PayrollColl_print.row(2).height_mismatch = True
        ws_PayrollColl_print.row(2).height = 650
        ws_PayrollColl_print.row(3).height_mismatch = True
        ws_PayrollColl_print.row(3).height = 1000
        ws_PayrollColl_print.row(4).height_mismatch = True
        ws_PayrollColl_print.row(4).height = 650
        ws_PayrollColl_print.row(5).height_mismatch = True
        ws_PayrollColl_print.row(5).height = 1300
        # Head
        ws_PayrollColl_print.write_merge(0, 0, 2, 6, 'TEDIS - VIET HA PHARMA JOINT STOCK COMPANY', style_head_16pt_bold)
        ws_PayrollColl_print.write_merge(1, 1, 2, 6, ' Lot F.2B, Street No.2, Long Hau IZ, Long Hau Ward, Can Giuoc District, Long An Province', style_head_11pt_vertbot)
        ws_PayrollColl_print.write_merge(3, 3, 0, 6, 'COLLABORATION PAYMENT - ' + str(period_month.month_name), style_head_20pt_bold)
        
        # Table
        # Table-head
        ws_PayrollColl_print.write(5, 0, 'No.', style_tablehead_grey25)
        ws_PayrollColl_print.write(5, 1, 'Employee code', style_tablehead_grey25)
        ws_PayrollColl_print.write(5, 2, 'Full name', style_tablehead_grey25)
        ws_PayrollColl_print.write(5, 3, 'Title', style_tablehead_grey25)
        ws_PayrollColl_print.write(5, 4, 'Collaboration Fee', style_tablehead_grey25)
        ws_PayrollColl_print.write(5, 5, 'PIT', style_tablehead_grey25)
        ws_PayrollColl_print.write(5, 6, 'Total Payment', style_tablehead_grey25)
        # Table-Body
        # Create total var
        ttcollaboration_fee = 0
        ttPIT = 0
        tttotal_payment = 0
        for index, data in enumerate(list_payroll_coll_info):
            # Set row height
            ws_PayrollColl_print.row(6+index).height_mismatch = True
            ws_PayrollColl_print.row(6+index).height = 500
            # Write data
            ws_PayrollColl_print.write(6+index, 0, str(index+1),style_normal)
            ws_PayrollColl_print.write(6+index, 1, str(data['payroll_info'].employee.employee_code),style_normal)
            ws_PayrollColl_print.write(6+index, 2, str(data['payroll_info'].employee.full_name),style_normal)
            ws_PayrollColl_print.write(6+index, 3, 'Collaborator',style_normal)
            ws_PayrollColl_print.write(6+index, 4, str("{:,}".format(round(data['payroll_info'].net_income))),style_normal)
            ws_PayrollColl_print.write(6+index, 5, str("{:,}".format(round(data['payroll_info'].PIT))),style_normal)
            ws_PayrollColl_print.write(6+index, 6, str("{:,}".format(round(data['payroll_info'].total_cost))),style_normal)
            # Get total line data
            last_row = 6 + index + 1
            ttcollaboration_fee += data['payroll_info'].net_income
            ttPIT += data['payroll_info'].PIT
            tttotal_payment += data['payroll_info'].total_cost
        # Table-footer
        # Set row height
        ws_PayrollColl_print.row(last_row).height_mismatch = True
        ws_PayrollColl_print.row(last_row).height = 800
        # Total line in bottom of table 
        ws_PayrollColl_print.write_merge(last_row, last_row, 0, 3, 'TOTAL', style_tablehead_grey25)
        ws_PayrollColl_print.write(last_row, 4, str("{:,}".format(ttcollaboration_fee)),style_tablehead_grey25)
        ws_PayrollColl_print.write(last_row, 5, str("{:,}".format(ttPIT)),style_tablehead_grey25)
        ws_PayrollColl_print.write(last_row, 6, str("{:,}".format(tttotal_payment)),style_tablehead_grey25)
        # Footer
        ws_PayrollColl_print.write(last_row+3, 1, 'Prepared by', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollColl_print.write(last_row+3, 5, 'Approved by', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollColl_print.write(last_row+9, 1, 'Le Thi Thanh Tuyen', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollColl_print.write(last_row+9, 5, 'Nguyen Minh Son', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollColl_print.write(last_row+10, 1, datetime.now().strftime('%d/%m/%Y'), style_footer_10pt_vertcen_horizleft)
        ws_PayrollColl_print.write(last_row+10, 5, datetime.now().strftime('%d/%m/%Y'), style_footer_10pt_vertcen_horizleft)
        
        
        '''Sheet Payroll Ser'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head_11pt_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert bottom' % 'white')
        style_head_12pt_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_head_16pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 320, name Arial, colour black; align: horiz left, vert bottom' % 'white')
        style_head_22pt_bold_vertbot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 440, name Arial, colour black; align: vert bottom' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_tablefooterdata_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz right, vert center' % '67')
        style_tablefooterdata_grey25.alignment.wrap = 1
        style_tablebody = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_tablebody.alignment.wrap = 1
        style_tablebody_onlyvertcenter = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                     'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: vert center' % 'white')
        style_tablebody_onlyvertcenter.alignment.wrap = 1
        style_footer_bold_10pt_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_bold_vertcen_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_footer_10pt_bold_vertcen_horizleft.alignment.wrap = 1
        style_footer_date = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 200, name Arial, colour black; align: horiz left,vert center' % 'white')
        
        # Create sheet
        ws_PayrollSer = wb.add_sheet(str(period_month.month_name)+ ' Ser')
        # Set col width
        ws_PayrollSer.col(0).width = 1652
        ws_PayrollSer.col(1).width = 2535
        ws_PayrollSer.col(2).width = 5423
        ws_PayrollSer.col(3).width = 2973
        ws_PayrollSer.col(4).width = 4840
        ws_PayrollSer.col(5).width = 4363
        for i in range(6,44):
            if i == 8:
                ws_PayrollSer.col(i).width = 2170
            else:
                ws_PayrollSer.col(i).width = 3263
        
        # Set row height
        ws_PayrollSer.row(0).height_mismatch = True
        ws_PayrollSer.row(0).height = 1100
        ws_PayrollSer.row(1).height_mismatch = True
        ws_PayrollSer.row(1).height = 650
        ws_PayrollSer.row(2).height_mismatch = True
        ws_PayrollSer.row(2).height = 650
        ws_PayrollSer.row(3).height_mismatch = True
        ws_PayrollSer.row(3).height = 1000
        ws_PayrollSer.row(4).height_mismatch = True
        ws_PayrollSer.row(4).height = 650
        ws_PayrollSer.row(5).height_mismatch = True
        ws_PayrollSer.row(5).height = 650
        ws_PayrollSer.row(6).height_mismatch = True
        ws_PayrollSer.row(6).height = 650
        ws_PayrollSer.row(7).height_mismatch = True
        ws_PayrollSer.row(7).height = 2080
        ws_PayrollSer.row(8).height_mismatch = True
        ws_PayrollSer.row(8).height = 930
        ws_PayrollSer.row(9).height_mismatch = True
        ws_PayrollSer.row(9).height = 900
        ws_PayrollSer.row(10).height_mismatch = True
        ws_PayrollSer.row(10).height = 660
        ws_PayrollSer.row(11).height_mismatch = True
        ws_PayrollSer.row(11).height = 660
        ws_PayrollSer.row(13).height_mismatch = True
        ws_PayrollSer.row(13).height = 2220
        
        # Head
        ws_PayrollSer.write(0, 3, 'TEDIS - VIET HA PHARMA JOINT STOCK COMPANY', style_head_16pt_bold)
        ws_PayrollSer.write(1, 3, ' Lot F.2B, Street No.2, Long Hau IZ, Long Hau Ward, Can Giuoc District, Long An Province', style_head_11pt_vertbot)
        ws_PayrollSer.write(3, 3, 'PAYROLL IN  ' + str(period_month.month_name), style_head_22pt_bold_vertbot)
        
        ws_PayrollSer.write(4, 0, 'Working days:', style_head_12pt_vertcen_horizleft)
        ws_PayrollSer.write(4, 3, str(payroll_ser.working_days), style_head_12pt_vertcen_horizleft)
        ws_PayrollSer.write(5, 0, 'Exchange rate (USD)', style_head_12pt_vertcen_horizleft)
        ws_PayrollSer.write(5, 3, str(payroll_ser.exchange_rate_usd), style_head_12pt_vertcen_horizleft)
        ws_PayrollSer.write(6, 0, 'Exchange rate (EURO)', style_head_12pt_vertcen_horizleft)
        ws_PayrollSer.write(6, 3, str(payroll_ser.exchange_rate_euro), style_head_12pt_vertcen_horizleft)
        
        
        # Table
        # Table-head
        ws_PayrollSer.write(7, 0, 'No', style_tablehead_grey25)
        ws_PayrollSer.write(7, 1, 'Employee code', style_tablehead_grey25)
        ws_PayrollSer.write(7, 2, 'Full name', style_tablehead_grey25)
        ws_PayrollSer.write(7, 3, 'Joining Date', style_tablehead_grey25)
        ws_PayrollSer.write(7, 4, 'Department/Area', style_tablehead_grey25)
        ws_PayrollSer.write(7, 5, 'Title', style_tablehead_grey25)
        ws_PayrollSer.write(7, 6, 'Salary (USD)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 7, 'Salary (VND)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 8, 'Working days', style_tablehead_grey25)
        ws_PayrollSer.write(7, 9, 'Gross Income', style_tablehead_grey25)
        ws_PayrollSer.write(7, 10, 'Salary recuperation', style_tablehead_grey25)
        ws_PayrollSer.write(7, 11, 'Housing (EURO)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 12, 'Housing (VND)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 13, 'Phone', style_tablehead_grey25)
        ws_PayrollSer.write(7, 14, 'Lunch', style_tablehead_grey25)
        ws_PayrollSer.write(7, 15, 'Training fee', style_tablehead_grey25)
        ws_PayrollSer.write(7, 16, 'Toxic Allowance', style_tablehead_grey25)
        ws_PayrollSer.write(7, 17, 'Travel', style_tablehead_grey25)
        ws_PayrollSer.write(7, 18, 'Responsibility', style_tablehead_grey25)
        ws_PayrollSer.write(7, 19, 'Seniority Bonus', style_tablehead_grey25)
        ws_PayrollSer.write(7, 20, 'Others', style_tablehead_grey25)
        ws_PayrollSer.write(7, 21, 'Total allowance recuperation', style_tablehead_grey25)
        ws_PayrollSer.write(7, 22, 'Benefits', style_tablehead_grey25)
        ws_PayrollSer.write(7, 23, 'Severance Allowance', style_tablehead_grey25)
        ws_PayrollSer.write(7, 24, 'Outstanding annual leave', style_tablehead_grey25)
        ws_PayrollSer.write(7, 25, '13th salary(Pro-ata)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 26, 'SHUI(9.5%)(Employee pay)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 27, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 28, 'SHUI(20.5%)(Employer pay)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 29, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 30, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 31, 'Trade Union fee (Company pay 2%)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 32, 'Trade Union fee (Member)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 33, 'Family deduction', style_tablehead_grey25)
        ws_PayrollSer.write(7, 34, 'Taxable Income', style_tablehead_grey25)
        ws_PayrollSer.write(7, 35, 'Taxed Income', style_tablehead_grey25)
        ws_PayrollSer.write(7, 36, 'PIT', style_tablehead_grey25)
        ws_PayrollSer.write(7, 37, '1st Payment Cash advance (EURO)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 38, '2nd Payment Net Income (VND)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 39, '2nd Payment Net Income (EURO)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 40, 'Net Income', style_tablehead_grey25)
        ws_PayrollSer.write(7, 41, 'Total Cost (VND)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 42, 'Total Cost (USD)', style_tablehead_grey25)
        ws_PayrollSer.write(7, 43, 'Note', style_tablehead_grey25)
        # Table-Body
        ws_PayrollSer.write(8, 0, '1',style_normal)
        ws_PayrollSer.write(8, 1, str(payroll_ser.employee.employee_code),style_normal)
        ws_PayrollSer.write(8, 2, str(payroll_ser.employee.full_name),style_normal)
        ws_PayrollSer.write(8, 3, str(payroll_ser.employee.joining_date.strftime('%d/%m/%Y')),style_normal)
        ws_PayrollSer.write(8, 4, str(payroll_ser.employee.department_e),style_normal)
        ws_PayrollSer.write(8, 5, str(payroll_ser.employee.position_e),style_normal)
        ws_PayrollSer.write(8, 6, str("{:,.0f}".format(payroll_ser.salary_usd)),style_normal)
        ws_PayrollSer.write(8, 7, str("{:,.0f}".format(payroll_ser.salary_vnd)),style_normal)
        ws_PayrollSer.write(8, 8, str(payroll_ser.working_days),style_normal)
        ws_PayrollSer.write(8, 9, str("{:,.0f}".format(payroll_ser.gross_income)),style_normal)
        ws_PayrollSer.write(8, 10, str("{:,.0f}".format(payroll_ser.salary_recuperation)),style_normal)
        ws_PayrollSer.write(8, 11, str("{:,}".format(payroll_ser.housing_euro)),style_normal)
        ws_PayrollSer.write(8, 12, str("{:,.0f}".format(payroll_ser.housing_vnd)),style_normal)
        ws_PayrollSer.write(8, 13, str("{:,.0f}".format(payroll_ser.phone)),style_normal)
        ws_PayrollSer.write(8, 14, str("{:,.0f}".format(payroll_ser.lunch)),style_normal)
        ws_PayrollSer.write(8, 15, str("{:,.0f}".format(payroll_ser.training_fee)),style_normal)
        ws_PayrollSer.write(8, 16, str("{:,.0f}".format(payroll_ser.toxic_allowance)),style_normal)
        ws_PayrollSer.write(8, 17, str("{:,.0f}".format(payroll_ser.travel)),style_normal)
        ws_PayrollSer.write(8, 18, str("{:,.0f}".format(payroll_ser.responsibility)),style_normal)
        ws_PayrollSer.write(8, 19, str("{:,.0f}".format(payroll_ser.seniority_bonus)),style_normal)
        ws_PayrollSer.write(8, 20, str("{:,.0f}".format(payroll_ser.other)),style_normal)
        ws_PayrollSer.write(8, 21, str("{:,.0f}".format(payroll_ser.total_allowance_recuperation)),style_normal)
        ws_PayrollSer.write(8, 22, str("{:,.0f}".format(payroll_ser.benefits)),style_normal)
        ws_PayrollSer.write(8, 23, str("{:,.0f}".format(payroll_ser.severance_allowance)),style_normal)
        ws_PayrollSer.write(8, 24, str("{:,.0f}".format(payroll_ser.outstanding_annual_leave)),style_normal)
        ws_PayrollSer.write(8, 25, str("{:,.0f}".format(payroll_ser.month_13_salary_Pro_ata)),style_normal)
        ws_PayrollSer.write(8, 26, str("{:,.0f}".format(payroll_ser.SHUI_9point5percent_employee_pay)),style_normal)
        ws_PayrollSer.write(8, 27, str("{:,.0f}".format(payroll_ser.recuperation_of_SHU_Ins_10point5percent_staff_pay)),style_normal)
        ws_PayrollSer.write(8, 28, str("{:,.0f}".format(payroll_ser.SHUI_20point5percent_employer_pay)),style_normal)
        ws_PayrollSer.write(8, 29, str("{:,.0f}".format(payroll_ser.recuperation_of_SHU_Ins_21point5percent_company_pay)),style_normal)
        ws_PayrollSer.write(8, 30, str("{:,.0f}".format(payroll_ser.occupational_accident_and_disease)),style_normal)
        ws_PayrollSer.write(8, 31, str("{:,.0f}".format(payroll_ser.trade_union_fee_company_pay)),style_normal)
        ws_PayrollSer.write(8, 32, str("{:,.0f}".format(payroll_ser.trade_union_fee_member)),style_normal)
        ws_PayrollSer.write(8, 33, str("{:,.0f}".format(payroll_ser.family_deduction)),style_normal)
        ws_PayrollSer.write(8, 34, str("{:,.0f}".format(payroll_ser.taxable_income)),style_normal)
        ws_PayrollSer.write(8, 35, str("{:,.0f}".format(payroll_ser.taxed_income)),style_normal)
        ws_PayrollSer.write(8, 36, str("{:,.0f}".format(payroll_ser.PIT)),style_normal)
        ws_PayrollSer.write(8, 37, str("{:,.0f}".format(payroll_ser.first_payment_cash_advance_euro)),style_normal)
        ws_PayrollSer.write(8, 38, str("{:,.0f}".format(payroll_ser.second_payment_net_income_vnd)),style_normal)
        ws_PayrollSer.write(8, 39, str("{:,.0f}".format(payroll_ser.second_payment_net_income_euro)),style_normal)
        ws_PayrollSer.write(8, 40, str("{:,.0f}".format(payroll_ser.net_income)),style_normal)
        ws_PayrollSer.write(8, 41, str("{:,.0f}".format(payroll_ser.total_cost_vnd)),style_normal)
        ws_PayrollSer.write(8, 42, str("{:,.0f}".format(payroll_ser.total_cost_usd)),style_normal)
        ws_PayrollSer.write(8, 43, str(payroll_ser.note),style_normal)    
        # Table-footer
        ws_PayrollSer.write_merge(9, 9, 0, 5, 'TOTAL', style_tablehead_grey25)
        ws_PayrollSer.write(9, 6, str("{:,.0f}".format(payroll_ser.salary_usd)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 7, str("{:,.0f}".format(payroll_ser.salary_vnd)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 8, str(payroll_ser.working_days),style_tablehead_grey25)
        ws_PayrollSer.write(9, 9, str("{:,.0f}".format(payroll_ser.gross_income)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 10, str("{:,.0f}".format(payroll_ser.salary_recuperation)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 11, str("{:,}".format(payroll_ser.housing_euro)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 12, str("{:,.0f}".format(payroll_ser.housing_vnd)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 13, str("{:,.0f}".format(payroll_ser.phone)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 14, str("{:,.0f}".format(payroll_ser.lunch)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 15, str("{:,.0f}".format(payroll_ser.training_fee)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 16, str("{:,.0f}".format(payroll_ser.toxic_allowance)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 17, str("{:,.0f}".format(payroll_ser.travel)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 18, str("{:,.0f}".format(payroll_ser.responsibility)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 19, str("{:,.0f}".format(payroll_ser.seniority_bonus)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 20, str("{:,.0f}".format(payroll_ser.other)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 21, str("{:,.0f}".format(payroll_ser.total_allowance_recuperation)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 22, str("{:,.0f}".format(payroll_ser.benefits)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 23, str("{:,.0f}".format(payroll_ser.severance_allowance)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 24, str("{:,.0f}".format(payroll_ser.outstanding_annual_leave)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 25, str("{:,.0f}".format(payroll_ser.month_13_salary_Pro_ata)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 26, str("{:,.0f}".format(payroll_ser.SHUI_9point5percent_employee_pay)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 27, str("{:,.0f}".format(payroll_ser.recuperation_of_SHU_Ins_10point5percent_staff_pay)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 28, str("{:,.0f}".format(payroll_ser.SHUI_20point5percent_employer_pay)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 29, str("{:,.0f}".format(payroll_ser.recuperation_of_SHU_Ins_21point5percent_company_pay)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 30, str("{:,.0f}".format(payroll_ser.occupational_accident_and_disease)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 31, str("{:,.0f}".format(payroll_ser.trade_union_fee_company_pay)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 32, str("{:,.0f}".format(payroll_ser.trade_union_fee_member)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 33, str("{:,.0f}".format(payroll_ser.family_deduction)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 34, str("{:,.0f}".format(payroll_ser.taxable_income)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 35, str("{:,.0f}".format(payroll_ser.taxed_income)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 36, str("{:,.0f}".format(payroll_ser.PIT)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 37, str("{:,.0f}".format(payroll_ser.first_payment_cash_advance_euro)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 38, str("{:,.0f}".format(payroll_ser.second_payment_net_income_vnd)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 39, str("{:,.0f}".format(payroll_ser.second_payment_net_income_euro)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 40, str("{:,.0f}".format(payroll_ser.net_income)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 41, str("{:,.0f}".format(payroll_ser.total_cost_vnd)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 42, str("{:,.0f}".format(payroll_ser.total_cost_usd)),style_tablehead_grey25)
        ws_PayrollSer.write(9, 43, str(payroll_ser.note),style_tablehead_grey25)    
        # Footer
        ws_PayrollSer.write(12, 2, 'Reviewed by', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollSer.write(12, 39, 'Approved by', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollSer.write(14, 2, 'Le Thi Thanh Tuyen', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollSer.write(14, 39, 'To Ngoc Chi Lan', style_footer_bold_10pt_vertcen_horizleft)
        ws_PayrollSer.write(15, 2, datetime.now().strftime('%d/%m/%Y'), style_footer_date)
        ws_PayrollSer.write(15, 39, datetime.now().strftime('%d/%m/%Y'), style_footer_date)
        
        
        '''Sheet Payment'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold off,height 200, name Times New Roman, colour black;' % 'white')
        style_head_red = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color gray25, top thin;'
                                    'font: bold off,height 200, name Arial, colour red;' % 'white')
        style_head_16pt_bold_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 320, name Arial, colour black; align: vert center' % 'white')
        style_head_12pt_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: vert center' % 'white')
        style_head_20pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 400, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_grey25 = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz center, vert center' % '67')
        style_tablehead_grey25.alignment.wrap = 1
        style_no = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_no.alignment.wrap = 1
        style_item = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_item.alignment.wrap = 1
        style_description = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_description.alignment.wrap = 1
        style_tablebody_vertcen_horizleft_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablebody_vertcen_horizleft_bold.alignment.wrap = 1
        style_amount = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_amount.alignment.wrap = 1
        style_paidby_paidto_accno = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_paidby_paidto_accno.alignment.wrap = 1
        style_prepared_by = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert bottom' % 'white')
        style_footer_name = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_date = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')

        # Create sheet
        ws_Payment = wb.add_sheet('Payment')
        # Set col width
        ws_Payment.col(0).width = 2000
        for col in range(1,8):
            if col == 5:
                ws_Payment.col(col).width = 4000
            elif col == 6:
                ws_Payment.col(col).width = 4000 
            elif col == 7:
                ws_Payment.col(col).width = 30000 
            else:
                ws_Payment.col(col).width = 6000

        # Set row height
        ws_Payment.row(0).height_mismatch = True
        ws_Payment.row(0).height = 800
        ws_Payment.row(1).height_mismatch = True
        ws_Payment.row(1).height = 300
        ws_Payment.row(2).height_mismatch = True
        ws_Payment.row(2).height = 300
        ws_Payment.row(3).height_mismatch = True
        ws_Payment.row(3).height = 600
        ws_Payment.row(4).height_mismatch = True
        ws_Payment.row(4).height = 300
        ws_Payment.row(5).height_mismatch = True
        ws_Payment.row(5).height = 800
        # Head
        ws_Payment.write(0, 2, 'TEDIS - VIET HA PHARMA JOINT STOCK COMPANY', style_head_16pt_bold_vertcen)
        ws_Payment.write(1, 2, 'Lot F.2B Street No.2, Long Hau IZ, Long Hau Ward, Can Giuoc District, Long An Province', style_head_12pt_vertcen)
        ws_Payment.write_merge(3, 3, 0, 7, 'PAYMENT REPORT IN ' + str(period_month.month_name).upper(), style_head_20pt_bold)

        # Table
        # Table-head
        ws_Payment.write(5, 0, 'No.', style_tablehead_grey25)
        ws_Payment.write(5, 1, 'ITEM', style_tablehead_grey25)
        ws_Payment.write(5, 2, 'DESCRIPTION', style_tablehead_grey25)
        ws_Payment.write(5, 3, 'AMOUNT\nEURO', style_tablehead_grey25)
        ws_Payment.write(5, 4, 'AMOUNT\nVND', style_tablehead_grey25)
        ws_Payment.write(5, 5, 'PAID BY', style_tablehead_grey25)
        ws_Payment.write(5, 6, 'PAID TO', style_tablehead_grey25)
        ws_Payment.write(5, 7, 'ACCOUNT NO.', style_tablehead_grey25)
        # Table-Body
        '''SALARY'''
        report_payment_payroll_SALARY = Report_Payment_Payroll_Tedis_VietHa.objects.filter(month=period_month, item='SALARY').order_by('description')
        # Write NO. and ITEM column
        no_salary = report_payment_payroll_SALARY.count()
        ws_Payment.write_merge(6, 5+no_salary , 0, 0, '1', style_no)
        ws_Payment.write_merge(6, 5+no_salary , 1, 1, 'SALARY', style_item)
        # Make subtotal var
        subtotal_salary_euro = 0
        subtotal_salary_vnd = 0
        for index, payment_data in enumerate(report_payment_payroll_SALARY):    
            # Set row height
            ws_Payment.row(6+index).height_mismatch = True
            ws_Payment.row(6+index).height = 1400
            # Write data
            ws_Payment.write(6+index, 2, str(payment_data.description),style_description)
            ws_Payment.write(6+index, 3, str("{:,}".format(round(payment_data.amount_euro),0)),style_amount)
            ws_Payment.write(6+index, 4, str("{:,}".format(round(payment_data.amount_vnd),0)),style_amount)
            subtotal_salary_euro += payment_data.amount_euro
            subtotal_salary_vnd += payment_data.amount_vnd
            ws_Payment.write(6+index, 5, str(payment_data.paidby),style_paidby_paidto_accno)
            ws_Payment.write(6+index, 6, str(payment_data.paidto),style_paidby_paidto_accno)
            ws_Payment.write(6+index, 7, str(payment_data.account_no),style_paidby_paidto_accno)
        last_row_salary = 6 + no_salary
        '''SALARY + ALLOWANCE'''
        report_payment_payroll_SALARY_ALLOWANCE = Report_Payment_Payroll_Tedis_VietHa.objects.filter(month=period_month, item='SALARY + ALLOWANCE').order_by('description')
        # Write NO. and ITEM column
        no_salary_allowance = report_payment_payroll_SALARY_ALLOWANCE.count()
        ws_Payment.write_merge(last_row_salary, last_row_salary+no_salary_allowance-1 , 0, 0, '2', style_no)
        ws_Payment.write_merge(last_row_salary, last_row_salary+no_salary_allowance-1 , 1, 1, 'SALARY + ALLOWANCE', style_item)
        # Make subtotal var
        subtotal_salary_allowance_euro = 0
        subtotal_salary_allowance_vnd = 0
        for index, payment_data in enumerate(report_payment_payroll_SALARY_ALLOWANCE):    
            # Set row height
            ws_Payment.row(last_row_salary+index).height_mismatch = True
            ws_Payment.row(last_row_salary+index).height = 1400
            # Write data
            ws_Payment.write(last_row_salary+index, 2, str(payment_data.description),style_description)
            ws_Payment.write(last_row_salary+index, 3, str("{:,}".format(round(payment_data.amount_euro),0)),style_amount)
            ws_Payment.write(last_row_salary+index, 4, str("{:,}".format(round(payment_data.amount_vnd),0)),style_amount)
            subtotal_salary_allowance_euro += payment_data.amount_euro
            subtotal_salary_allowance_vnd += payment_data.amount_vnd
            ws_Payment.write(last_row_salary+index, 5, str(payment_data.paidby),style_paidby_paidto_accno)
            ws_Payment.write(last_row_salary+index, 6, str(payment_data.paidto),style_paidby_paidto_accno)
            ws_Payment.write(last_row_salary+index, 7, str(payment_data.account_no),style_paidby_paidto_accno)
        last_row_salary_allowance = last_row_salary + no_salary_allowance
        '''SHUI'''
        report_payment_payroll_SHUI = Report_Payment_Payroll_Tedis_VietHa.objects.filter(month=period_month, item='SHUI').order_by('-description')
        # Write NO. and ITEM column
        no_shui = report_payment_payroll_SHUI.count()
        ws_Payment.write_merge(last_row_salary_allowance, last_row_salary_allowance+no_shui-1 , 0, 0, '3', style_no)
        ws_Payment.write_merge(last_row_salary_allowance, last_row_salary_allowance+no_shui-1 , 1, 1, 'SHUI', style_item)
        # Make subtotal var
        subtotal_shui_euro = 0
        subtotal_shui_vnd = 0
        for index, payment_data in enumerate(report_payment_payroll_SHUI):    
            # Set row height
            ws_Payment.row(last_row_salary_allowance+index).height_mismatch = True
            ws_Payment.row(last_row_salary_allowance+index).height = 1400
            # Write data
            ws_Payment.write(last_row_salary_allowance+index, 2, str(payment_data.description),style_description)
            ws_Payment.write(last_row_salary_allowance+index, 3, str("{:,}".format(round(payment_data.amount_euro),0)),style_amount)
            ws_Payment.write(last_row_salary_allowance+index, 4, str("{:,}".format(round(payment_data.amount_vnd),0)),style_amount)
            subtotal_shui_euro += payment_data.amount_euro
            subtotal_shui_vnd += payment_data.amount_vnd
            ws_Payment.write(last_row_salary_allowance+index, 5, str(payment_data.paidby),style_paidby_paidto_accno)
            ws_Payment.write(last_row_salary_allowance+index, 6, str(payment_data.paidto),style_paidby_paidto_accno)
            ws_Payment.write(last_row_salary_allowance+index, 7, str(payment_data.account_no),style_paidby_paidto_accno)
        last_row_SHUI = last_row_salary_allowance + no_shui
        '''PIT'''
        report_payment_payroll_PIT = Report_Payment_Payroll_Tedis_VietHa.objects.filter(month=period_month, item='PIT').order_by('-description')
        # Write NO. and ITEM column
        no_pit = report_payment_payroll_PIT.count()
        ws_Payment.write_merge(last_row_SHUI, last_row_SHUI+no_pit-1 , 0, 0, '4', style_no)
        ws_Payment.write_merge(last_row_SHUI, last_row_SHUI+no_pit-1 , 1, 1, 'PIT', style_item)
        # Make subtotal var
        subtotal_pit_euro = 0
        subtotal_pit_vnd = 0
        for index, payment_data in enumerate(report_payment_payroll_PIT):    
            # Set row height
            ws_Payment.row(last_row_SHUI+index).height_mismatch = True
            ws_Payment.row(last_row_SHUI+index).height = 1400
            # Write data
            ws_Payment.write(last_row_SHUI+index, 2, str(payment_data.description),style_description)
            ws_Payment.write(last_row_SHUI+index, 3, str("{:,}".format(round(payment_data.amount_euro),0)),style_amount)
            ws_Payment.write(last_row_SHUI+index, 4, str("{:,}".format(round(payment_data.amount_vnd),0)),style_amount)
            subtotal_pit_euro += payment_data.amount_euro
            subtotal_pit_vnd += payment_data.amount_vnd
            ws_Payment.write(last_row_SHUI+index, 5, str(payment_data.paidby),style_paidby_paidto_accno)
            ws_Payment.write(last_row_SHUI+index, 6, str(payment_data.paidto),style_paidby_paidto_accno)
            ws_Payment.write(last_row_SHUI+index, 7, str(payment_data.account_no),style_paidby_paidto_accno)
        last_row_pit = last_row_SHUI + no_pit
        '''Trade union'''
        report_payment_payroll_TRADE_UNION = Report_Payment_Payroll_Tedis_VietHa.objects.filter(month=period_month, item='TRADE UNION').order_by('-description')
        # Write NO. and ITEM column
        no_trade_union = report_payment_payroll_TRADE_UNION.count()
        ws_Payment.write_merge(last_row_pit, last_row_pit+no_trade_union-1 , 0, 0, '5', style_no)
        ws_Payment.write_merge(last_row_pit, last_row_pit+no_trade_union-1 , 1, 1, 'TRADE UNION', style_item)
        # Make subtotal var
        subtotal_trade_union_euro = 0
        subtotal_trade_union_vnd = 0
        for index, payment_data in enumerate(report_payment_payroll_TRADE_UNION):    
            # Set row height
            ws_Payment.row(last_row_pit+index).height_mismatch = True
            ws_Payment.row(last_row_pit+index).height = 1400
            # Write data
            ws_Payment.write(last_row_pit+index, 2, str(payment_data.description),style_description)
            ws_Payment.write(last_row_pit+index, 3, str("{:,}".format(round(payment_data.amount_euro),0)),style_amount)
            ws_Payment.write(last_row_pit+index, 4, str("{:,}".format(round(payment_data.amount_vnd),0)),style_amount)
            subtotal_trade_union_euro += payment_data.amount_euro
            subtotal_trade_union_vnd += payment_data.amount_vnd
            ws_Payment.write(last_row_pit+index, 5, str(payment_data.paidby),style_paidby_paidto_accno)
            ws_Payment.write(last_row_pit+index, 6, str(payment_data.paidto),style_paidby_paidto_accno)
            ws_Payment.write(last_row_pit+index, 7, str(payment_data.account_no),style_paidby_paidto_accno)
        last_row_trade_union = last_row_pit + no_trade_union
        '''TOTAL COST'''
        # Make total var
        total_cost_euro = subtotal_salary_euro + subtotal_salary_allowance_euro + subtotal_shui_euro + subtotal_pit_euro + subtotal_trade_union_euro
        total_cost_vnd = subtotal_salary_vnd + subtotal_salary_allowance_vnd + subtotal_shui_vnd + subtotal_pit_vnd + subtotal_trade_union_vnd
        # Set row height
        ws_Payment.row(last_row_trade_union).height_mismatch = True
        ws_Payment.row(last_row_trade_union).height = 750
        # Write data
        ws_Payment.write_merge(last_row_trade_union, last_row_trade_union , 0, 2, 'TOTAL', style_item) 
        ws_Payment.write(last_row_trade_union, 3, str("{:,}".format(round(total_cost_euro),0)),style_amount) 
        ws_Payment.write(last_row_trade_union, 4, str("{:,}".format(round(total_cost_vnd),0)),style_amount)
        ws_Payment.write_merge(last_row_trade_union, last_row_trade_union , 5, 7, '', style_amount)
        '''TOTAL'''
        # Make total var
        total = total_cost_euro + total_cost_vnd
        # Set row height
        ws_Payment.row(last_row_trade_union + 1).height_mismatch = True
        ws_Payment.row(last_row_trade_union + 1).height = 750
        # Write data
        ws_Payment.write_merge(last_row_trade_union + 1, last_row_trade_union + 1 , 0, 2, '', style_amount) 
        ws_Payment.write_merge(last_row_trade_union + 1, last_row_trade_union + 1 , 3, 4, str("{:,}".format(round(total),0)), style_amount) 
        ws_Payment.write_merge(last_row_trade_union + 1, last_row_trade_union + 1 , 5, 7, '', style_amount)               
        
        # Footer
        # Set row height
        ws_Payment.row(last_row_trade_union + 2).height_mismatch = True
        ws_Payment.row(last_row_trade_union + 2).height = 820
        ws_Payment.row(last_row_trade_union + 3).height_mismatch = True
        ws_Payment.row(last_row_trade_union + 3).height = 1410
        ws_Payment.row(last_row_trade_union + 4).height_mismatch = True
        ws_Payment.row(last_row_trade_union + 4).height = 465
        ws_Payment.row(last_row_trade_union + 5).height_mismatch = True
        ws_Payment.row(last_row_trade_union + 5).height = 465
        # Write data
        ws_Payment.write(last_row_trade_union + 2, 1, 'Prepared by', style_prepared_by)  
        ws_Payment.write(last_row_trade_union + 2, 7, 'Approved by', style_prepared_by)
        ws_Payment.write(last_row_trade_union + 4, 1, 'Le Thi Thanh Tuyen', style_footer_name)
        ws_Payment.write(last_row_trade_union + 4, 7, 'Vu Chau Kim Anh', style_footer_name)
        ws_Payment.write(last_row_trade_union + 5, 1, datetime.now().strftime('%d/%m/%Y'), style_date)  
        ws_Payment.write(last_row_trade_union + 5, 7, datetime.now().strftime('%d/%m/%Y'), style_date)  
        
        
        '''Sheet Infor.Payroll'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head_12pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 240, name Arial, colour black; align: horiz left,vert bottom' % 'white')
        style_head_12pt_vertcen = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 240, name Arial, colour black; align: vert center' % 'white')
        style_head_20pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 400, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_title = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, top thin, bottom double;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz left,vert bottom' % '44')
        style_tablehead = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz center,vert center' % '44')
        style_tablehead.alignment.wrap = 1
        style_no = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_no.alignment.wrap = 1
        style_item = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_item.alignment.wrap = 1
        style_body = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 200, name Arial, colour 56; align: horiz center, vert center' % 'white')
        style_body.alignment.wrap = 1
        style_tablebody_vertcen_horizleft_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablebody_vertcen_horizleft_bold.alignment.wrap = 1
        style_amount = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_amount.alignment.wrap = 1
        style_paidby_paidto_accno = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_paidby_paidto_accno.alignment.wrap = 1
        style_prepared_by = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert bottom' % 'white')
        style_footer_name = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_date = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')

        # Create sheet
        ws_InforPayroll = wb.add_sheet('Infor.Payroll')
        # Set col width
        for col in range(0,14):
            if col == 0:
                ws_InforPayroll.col(col).width = 2293
            elif col == 1:
                ws_InforPayroll.col(col).width = 2293 
            elif col == 2:
                ws_InforPayroll.col(col).width = 9578
            elif col == 3:
                ws_InforPayroll.col(col).width = 6182
            elif col == 4:
                ws_InforPayroll.col(col).width = 3692
            elif col == 5:
                ws_InforPayroll.col(col).width = 4414
            elif col == 6:
                ws_InforPayroll.col(col).width = 4696
            elif col == 7:
                ws_InforPayroll.col(col).width = 5140
            elif col == 8:
                ws_InforPayroll.col(col).width = 3372
            elif col == 9:
                ws_InforPayroll.col(col).width = 3372
            elif col == 10:
                ws_InforPayroll.col(col).width = 3372
            elif col == 11:
                ws_InforPayroll.col(col).width = 3372
            elif col == 12:
                ws_InforPayroll.col(col).width = 3372
            elif col == 13:
                ws_InforPayroll.col(col).width = 6623  
        

        # Set row height
        ws_InforPayroll.row(0).height_mismatch = True
        ws_InforPayroll.row(0).height = 300
        ws_InforPayroll.row(1).height_mismatch = True
        ws_InforPayroll.row(1).height = 300
        ws_InforPayroll.row(2).height_mismatch = True
        ws_InforPayroll.row(2).height = 300
        ws_InforPayroll.row(3).height_mismatch = True
        ws_InforPayroll.row(3).height = 300
        ws_InforPayroll.row(4).height_mismatch = True
        ws_InforPayroll.row(4).height = 300
        ws_InforPayroll.row(5).height_mismatch = True
        ws_InforPayroll.row(5).height = 525
        # Head
        ws_InforPayroll.write(2, 0, 'UPDATED INFORMATION FOR PAYROLL ' + str(period_month.month_name).upper(), style_head_12pt_bold)

        # Table
        
        '''NEW STAFF'''
        # Table-head
        ws_InforPayroll.write(4, 0, 'NEW STAFF', style_tablehead_title)
        ws_InforPayroll.write(4, 1, '', style_tablehead_title)
        ws_InforPayroll.write(4, 2, '', style_tablehead_title)
        ws_InforPayroll.write(4, 3, '', style_tablehead_title)
        ws_InforPayroll.write(4, 4, '', style_tablehead_title)
        ws_InforPayroll.write(4, 5, '', style_tablehead_title)
        ws_InforPayroll.write(4, 6, '', style_tablehead_title)
        ws_InforPayroll.write(4, 7, '', style_tablehead_title)
        ws_InforPayroll.write(4, 8, '', style_tablehead_title)
        ws_InforPayroll.write(4, 9, '', style_tablehead_title)
        ws_InforPayroll.write(4, 10, '', style_tablehead_title)
        ws_InforPayroll.write(4, 11, '', style_tablehead_title)
        ws_InforPayroll.write(4, 12, '', style_tablehead_title)
        ws_InforPayroll.write(4, 13, '', style_tablehead_title)
        
        ws_InforPayroll.write(5, 0, 'No.', style_tablehead)
        ws_InforPayroll.write(5, 1, '', style_tablehead)
        ws_InforPayroll.write(5, 2, 'Name', style_tablehead)
        ws_InforPayroll.write(5, 3, 'Dept', style_tablehead)
        ws_InforPayroll.write(5, 4, 'Joining date', style_tablehead)
        ws_InforPayroll.write(5, 5, 'Gross Salary', style_tablehead)
        ws_InforPayroll.write(5, 6, 'Allowance', style_tablehead)
        ws_InforPayroll.write(5, 7, 'Remark', style_tablehead)
        ws_InforPayroll.write(5, 8, 'Dependant deduction', style_tablehead)
        ws_InforPayroll.write(5, 9, 'Hospital for HI', style_tablehead)
        ws_InforPayroll.write(5, 10, 'A/c no.', style_tablehead)
        ws_InforPayroll.write(5, 11, 'Bank name', style_tablehead)
        ws_InforPayroll.write(5, 12, 'PIT code', style_tablehead)
        ws_InforPayroll.write(5, 13, '', style_tablehead)
        # Table-Body
        new_staff_reports = Report_new_staff_Tedis_VietHa.objects.filter(month=period_month)
        # Make subtotal var
        for index, report in enumerate(new_staff_reports):    
            # Set row height
            ws_InforPayroll.row(6+index).height_mismatch = True
            ws_InforPayroll.row(6+index).height = 525
            # Write data
            ws_InforPayroll.write(6+index, 0, str(index + 1),style_body)
            ws_InforPayroll.write(6+index, 1, str(report.employee.employee_code),style_body)
            ws_InforPayroll.write(6+index, 2, str(report.employee.full_name),style_body)
            ws_InforPayroll.write(6+index, 3, str(report.department),style_body)
            ws_InforPayroll.write(6+index, 4, report.joining_date.strftime('%#d-%b-%Y'),style_body)
            ws_InforPayroll.write(6+index, 5, str("{:,}".format(round(report.gross_salary),0)),style_body)
            ws_InforPayroll.write(6+index, 6, str("{:,}".format(round(report.allowance),0)),style_body)
            ws_InforPayroll.write(6+index, 7, str(report.remark),style_body)
            ws_InforPayroll.write(6+index, 8, str("{:,}".format(round(report.dependant_deduction),0)),style_body)
            ws_InforPayroll.write(6+index, 9, str(report.hospital_for_HI),style_body)
            ws_InforPayroll.write(6+index, 10, str(report.account_no),style_body)
            ws_InforPayroll.write(6+index, 11, str(report.bank_name),style_body)
            ws_InforPayroll.write(6+index, 12, str(report.PIT_code),style_body)
        last_row_new_staff = 6 + new_staff_reports.count()
        ws_InforPayroll.row(last_row_new_staff).height_mismatch = True
        ws_InforPayroll.row(last_row_new_staff).height = 525
        
        '''Resigned staff'''
        # Set row height
        ws_InforPayroll.row(last_row_new_staff + 1).height_mismatch = True
        ws_InforPayroll.row(last_row_new_staff + 1).height = 300
        ws_InforPayroll.row(last_row_new_staff + 2).height_mismatch = True
        ws_InforPayroll.row(last_row_new_staff + 2).height = 525
        # Table-head
        ws_InforPayroll.write(last_row_new_staff + 1, 0, 'CONFIRMED AFTER PROBATION', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 1, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 2, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 3, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 4, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 5, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 6, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 7, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 8, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 9, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 10, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 11, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 12, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_new_staff + 1, 13, '', style_tablehead_title)
        
        ws_InforPayroll.write(last_row_new_staff + 2, 0, 'No.', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 1, '', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 2, 'Name', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 3, 'Dept', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 4, 'Joining date', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 5, 'Sign LC date', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 6, 'Allowance', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 7, 'Sal. After probation', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 8, 'SI Book no.', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 9, 'Hospital for HI', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 10, '', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 11, '', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 12, '', style_tablehead)
        ws_InforPayroll.write(last_row_new_staff + 2, 13, '', style_tablehead)
        # Table-Body
        confirmed_after_probation_reports = Report_confirmed_after_probation_Tedis_VietHa.objects.filter(month=period_month)
        # Make subtotal var
        for index, report in enumerate(confirmed_after_probation_reports):    
            # Set row height
            ws_InforPayroll.row(last_row_new_staff+3+index).height_mismatch = True
            ws_InforPayroll.row(last_row_new_staff+3+index).height = 525
            # Write data
            ws_InforPayroll.write(last_row_new_staff+3+index, 0, str(index + 1),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 1, str(report.employee.employee_code),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 2, str(report.employee.full_name),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 3, str(report.department),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 4, report.joining_date.strftime('%#d-%b-%Y'),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 5, report.sign_LC_date.strftime('%#d-%b-%Y'),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 6, str("{:,}".format(round(report.allowance),0)),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 7, str("{:,}".format(round(report.salary_after_probation),0)),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 8, str(report.SI_book_no),style_body)
            ws_InforPayroll.write(last_row_new_staff+3+index, 9, str(report.hospital_for_HI),style_body)
        last_row_confirmed_after_probation = last_row_new_staff+3 + confirmed_after_probation_reports.count()
        ws_InforPayroll.row(last_row_confirmed_after_probation).height_mismatch = True
        ws_InforPayroll.row(last_row_confirmed_after_probation).height = 525
        
        '''Resigned staff'''
        # Set row height
        ws_InforPayroll.row(last_row_confirmed_after_probation + 1).height_mismatch = True
        ws_InforPayroll.row(last_row_confirmed_after_probation + 1).height = 300
        ws_InforPayroll.row(last_row_confirmed_after_probation + 2).height_mismatch = True
        ws_InforPayroll.row(last_row_confirmed_after_probation + 2).height = 525
        # Table-head
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 0, 'RESIGNED STAFF', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 1, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 2, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 3, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 4, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 5, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 6, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 7, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 8, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 9, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 10, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 11, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 12, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 1, 13, '', style_tablehead_title)
        
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 0, 'No.', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 1, '', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 2, 'Name', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 3, 'Dept', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 4, 'Joining date', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 5, 'Leaving date', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 6, 'Allowance', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 7, 'Unused AL', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 8, '13th month salary', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 9, 'Severance Allowance', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 10, 'Other allowance', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 11, 'Incentive', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 12, 'Remark', style_tablehead)
        ws_InforPayroll.write(last_row_confirmed_after_probation + 2, 13, '', style_tablehead)
        # Table-Body
        resigned_staff_reports = Report_resigned_staff_Tedis_VietHa.objects.filter(month=period_month)
        # Make subtotal var
        for index, report in enumerate(resigned_staff_reports):    
            # Set row height
            ws_InforPayroll.row(last_row_confirmed_after_probation+3+index).height_mismatch = True
            ws_InforPayroll.row(last_row_confirmed_after_probation+3+index).height = 525
            # Write data
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 0, str(index + 1),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 1, str(report.employee.employee_code),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 2, str(report.employee.full_name),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 3, str(report.department),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 4, report.joining_date.strftime('%#d-%b-%Y'),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 5, report.leaving_date.strftime('%#d-%b-%Y'),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 6, str("{:,}".format(round(report.allowance),0)),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 7, str("{:,}".format(round(report.unused_AL),0)),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 8, str("{:,}".format(round(report.month_13_salary),0)),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 9, str("{:,}".format(round(report.severance_allowance),0)),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 10, str("{:,}".format(round(report.other_allowance),0)),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 11, str("{:,}".format(round(report.incentive),0)),style_body)
            ws_InforPayroll.write(last_row_confirmed_after_probation+3+index, 12, str(report.remark),style_body)
        last_row_resigned_staff = last_row_confirmed_after_probation+3 + resigned_staff_reports.count()
        ws_InforPayroll.row(last_row_resigned_staff).height_mismatch = True
        ws_InforPayroll.row(last_row_resigned_staff).height = 525
        
        
        '''Other changes'''
        # Set row height
        ws_InforPayroll.row(last_row_resigned_staff + 1).height_mismatch = True
        ws_InforPayroll.row(last_row_resigned_staff + 1).height = 300
        ws_InforPayroll.row(last_row_resigned_staff + 2).height_mismatch = True
        ws_InforPayroll.row(last_row_resigned_staff + 2).height = 525
        # Table-head
        ws_InforPayroll.write(last_row_resigned_staff + 1, 0, 'OTHER CHANGES', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 1, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 2, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 3, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 4, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 5, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 6, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 7, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 8, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 9, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 10, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 11, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 12, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_resigned_staff + 1, 13, '', style_tablehead_title)
        
        ws_InforPayroll.write(last_row_resigned_staff + 2, 0, 'No.', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 1, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 2, 'Name', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 3, 'New Salary', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 4, 'Allowance', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 5, 'Effective date', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 6, 'Remark', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 7, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 8, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 9, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 10, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 11, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 12, '', style_tablehead)
        ws_InforPayroll.write(last_row_resigned_staff + 2, 13, '', style_tablehead)
        # Table-Body
        other_changes_reports = Report_other_changes_Tedis_VietHa.objects.filter(month=period_month)
        # Make subtotal var
        for index, report in enumerate(other_changes_reports):    
            # Set row height
            ws_InforPayroll.row(last_row_resigned_staff+3+index).height_mismatch = True
            ws_InforPayroll.row(last_row_resigned_staff+3+index).height = 525
            # Write data
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 0, str(index + 1),style_body)
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 1, str(report.employee.employee_code),style_body)
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 2, str(report.employee.full_name),style_body)
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 3, str("{:,}".format(round(report.new_salary),0)),style_body)
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 4, str("{:,}".format(round(report.allowance),0)),style_body)
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 5, report.effective_date.strftime('%#d-%b-%Y'),style_body)
            ws_InforPayroll.write(last_row_resigned_staff+3+index, 6, str(report.remark),style_body)
        last_row_other_changes = last_row_resigned_staff+3 + resigned_staff_reports.count()
        ws_InforPayroll.row(last_row_other_changes).height_mismatch = True
        ws_InforPayroll.row(last_row_other_changes).height = 525
        
        '''Maternity leave'''
        # Set row height
        ws_InforPayroll.row(last_row_other_changes + 1).height_mismatch = True
        ws_InforPayroll.row(last_row_other_changes + 1).height = 300
        ws_InforPayroll.row(last_row_other_changes + 2).height_mismatch = True
        ws_InforPayroll.row(last_row_other_changes + 2).height = 525
        # Table-head
        ws_InforPayroll.write(last_row_other_changes + 1, 0, 'MATERNITY LEAVE', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 1, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 2, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 3, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 4, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 5, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 6, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 7, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 8, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 9, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 10, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 11, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 12, '', style_tablehead_title)
        ws_InforPayroll.write(last_row_other_changes + 1, 13, '', style_tablehead_title)
        
        ws_InforPayroll.write(last_row_other_changes + 2, 0, 'No.', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 1, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 2, 'Name', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 3, 'Dept', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 4, 'From', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 5, 'To', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 6, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 7, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 8, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 9, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 10, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 11, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 12, '', style_tablehead)
        ws_InforPayroll.write(last_row_other_changes + 2, 13, '', style_tablehead)
        # Table-Body
        maternity_leave_reports = Report_maternity_leave_Tedis_VietHa.objects.filter(month=period_month)
        # Make subtotal var
        for index, report in enumerate(maternity_leave_reports):    
            # Set row height
            ws_InforPayroll.row(last_row_other_changes+3+index).height_mismatch = True
            ws_InforPayroll.row(last_row_other_changes+3+index).height = 525
            # Write data
            ws_InforPayroll.write(last_row_other_changes+3+index, 0, str(index + 1),style_body)
            ws_InforPayroll.write(last_row_other_changes+3+index, 1, str(report.employee.employee_code),style_body)
            ws_InforPayroll.write(last_row_other_changes+3+index, 2, str(report.employee.full_name),style_body)
            ws_InforPayroll.write(last_row_other_changes+3+index, 3, str(report.department),style_body)
            ws_InforPayroll.write(last_row_other_changes+3+index, 4, report.from_date.strftime('%d/%m/%Y'),style_body)
            ws_InforPayroll.write(last_row_other_changes+3+index, 5, report.to_date.strftime('%d/%m/%Y'),style_body)
        last_row_maternity_leave = last_row_other_changes+3 + resigned_staff_reports.count()
        ws_InforPayroll.row(last_row_maternity_leave).height_mismatch = True
        ws_InforPayroll.row(last_row_maternity_leave).height = 525
        
        
        '''Sheet reconcile'''
        # Style
        # xlwt color url: https://docs.google.com/spreadsheets/d/1ihNaZcUh7961yU7db1-Db0lbws4NT24B7koY8v8GHNQ/pubhtml?gid=1072579560&single=true
        style_head_24pt_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 480, name Arial, colour black; align: horiz left,vert center' % 'white')
        style_no = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom DASHED;'
                                'font: bold 1,height 200, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_10pt_bold_horizleft_vertcenter_allthin_but_botdot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom DASHED;'
                                'font: bold 1,height 200, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_7pt_bold_horizcenter_vertcenter_allthin_but_topdot_colorlightblue = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom thin;'
                                'font: bold 1,height 200, name Arial, colour black; align: horiz left, vert center' % '44')
        style_10pt_bold_horizleft_vertcenter_alldot_but_rightthin = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left DASHED, right thin, top DASHED, bottom DASHED;'
                                'font: bold 1,height 200, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_10pt_bold_horizleft_vertcenter_allthin_but_topdot = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom thin;'
                                'font: bold 1,height 200, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_10pt_bold_horizleft_vertcenter_allthin = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                'font: bold 1,height 200, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_headcount_staff = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom DASHED;'
                                'font: bold 1,height 140, name Arial, colour black; align: horiz center, vert center' % '44')
        style_body_staff = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom DASHED;'
                                'font: bold 0,height 160, name Arial, colour black; align: horiz center, vert center' % '44')
        style_headcount_coll = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom DASHED;'
                                'font: bold 1,height 140, name Arial, colour black; align: horiz center, vert center' % '44')
        style_body_coll = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom DASHED;'
                                'font: bold 0,height 160, name Arial, colour black; align: horiz center, vert center' % '44')
        style_headcount_ser = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom thin;'
                                'font: bold 1,height 140, name Arial, colour black; align: horiz center, vert center' % '44')
        style_body_ser = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom thin;'
                                'font: bold 0,height 160, name Arial, colour black; align: horiz center, vert center' % '44')
        style_headcount_diff = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                'font: bold 1,height 160, name Arial, colour black; align: horiz center, vert center' % '44')
        style_body_diff = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                               'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                'font: bold 1,height 160, name Arial, colour black; align: horiz center, vert center' % '44')
        style_explain_remark_employeename = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom DASHED;'
                                                        'font: bold 0,height 180, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_explain_remark_employeename.alignment.wrap = 1
        style_explain_data = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top DASHED, bottom DASHED;'
                                        'font: bold 1,height 160, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_explain_data.alignment.wrap = 1
        style_11pt_horizright = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_11pt_horizleft = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablehead_title = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom DASHED;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz center, vert center' % '44')
        style_tablehead_title.alignment.wrap = 1
        style_tablehead = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 200, name Arial, colour black; align: horiz center,vert center' % '44')
        style_tablehead.alignment.wrap = 1
        style_item = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz center, vert center' % 'white')
        style_item.alignment.wrap = 1
        style_body = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 200, name Arial, colour 56; align: horiz center, vert center' % 'white')
        style_body.alignment.wrap = 1
        style_tablebody_vertcen_horizleft_bold = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 260, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_tablebody_vertcen_horizleft_bold.alignment.wrap = 1
        style_amount = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz right, vert center' % 'white')
        style_amount.alignment.wrap = 1
        style_paidby_paidto_accno = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                        'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_paidby_paidto_accno.alignment.wrap = 1
        style_prepared_by = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert bottom' % 'white')
        style_footer_name = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 1,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')
        style_date = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                                    'font: bold 0,height 220, name Arial, colour black; align: horiz left, vert center' % 'white')

        # Create sheet
        ws_reconcile = wb.add_sheet('reconcile')
        # Set col width
        for col in range(0,30):
            if col == 0:
                ws_reconcile.col(col).width = 11446
            elif col == 1:
                ws_reconcile.col(col).width = 6400 
            elif col == 2:
                ws_reconcile.col(col).width = 4096
            elif col == 3:
                ws_reconcile.col(col).width = 4096
            elif col == 4:
                ws_reconcile.col(col).width = 4096
            elif col == 5:
                ws_reconcile.col(col).width = 4096
            elif col == 6:
                ws_reconcile.col(col).width = 4096
            elif col == 7:
                ws_reconcile.col(col).width = 4096
            elif col == 8:
                ws_reconcile.col(col).width = 4096
            elif col == 9:
                ws_reconcile.col(col).width = 4096
            elif col == 10:
                ws_reconcile.col(col).width = 4096
            elif col == 11:
                ws_reconcile.col(col).width = 4096
            elif col == 12:
                ws_reconcile.col(col).width = 4096
            elif col == 13:
                ws_reconcile.col(col).width = 4096
            elif col == 14:
                ws_reconcile.col(col).width = 4096
            elif col == 15:
                ws_reconcile.col(col).width = 4096
            elif col == 16:
                ws_reconcile.col(col).width = 4096
            elif col == 17:
                ws_reconcile.col(col).width = 4096
            elif col == 18:
                ws_reconcile.col(col).width = 4096
            elif col == 19:
                ws_reconcile.col(col).width = 4096
            elif col == 20:
                ws_reconcile.col(col).width = 4096
            elif col == 21:
                ws_reconcile.col(col).width = 4096
            elif col == 22:
                ws_reconcile.col(col).width = 4096
            elif col == 23:
                ws_reconcile.col(col).width = 4096
            elif col == 24:
                ws_reconcile.col(col).width = 4096
            elif col == 25:
                ws_reconcile.col(col).width = 4096
            elif col == 26:
                ws_reconcile.col(col).width = 4096
            elif col == 27:
                ws_reconcile.col(col).width = 4096
            elif col == 28:
                ws_reconcile.col(col).width = 4096
            elif col == 29:
                ws_reconcile.col(col).width = 4096
              
        

        # Set row height
        ws_reconcile.row(0).height_mismatch = True
        ws_reconcile.row(0).height = 800
        ws_reconcile.row(1).height_mismatch = True
        ws_reconcile.row(1).height = 1583
        ws_reconcile.row(2).height_mismatch = True
        ws_reconcile.row(2).height = 540
        ws_reconcile.row(3).height_mismatch = True
        ws_reconcile.row(3).height = 380
        ws_reconcile.row(4).height_mismatch = True
        ws_reconcile.row(4).height = 380
        ws_reconcile.row(5).height_mismatch = True
        ws_reconcile.row(5).height = 380
        ws_reconcile.row(6).height_mismatch = True
        ws_reconcile.row(6).height = 380
        ws_reconcile.row(7).height_mismatch = True
        ws_reconcile.row(7).height = 380
        ws_reconcile.row(8).height_mismatch = True
        ws_reconcile.row(8).height = 380
        ws_reconcile.row(9).height_mismatch = True
        ws_reconcile.row(9).height = 465
        ws_reconcile.row(10).height_mismatch = True
        ws_reconcile.row(10).height = 465
        
        # Head
        ws_reconcile.write(0, 0, 'PAYROLL ' + str(period_month.month_name).upper(), style_head_24pt_bold)
        
        # Table
        # Table-head
        ws_reconcile.write(1, 0, 'No', style_no)
        ws_reconcile.write(1, 1, 'Name', style_tablehead_title)
        ws_reconcile.write(1, 2, 'Headcount', style_tablehead_title)
        ws_reconcile.write(1, 3, 'Gross Income', style_tablehead_title)
        ws_reconcile.write(1, 4, 'Transportation', style_tablehead_title)
        ws_reconcile.write(1, 5, 'Phone', style_tablehead_title)
        ws_reconcile.write(1, 6, 'Lunch', style_tablehead_title)
        ws_reconcile.write(1, 7, 'Outstanding annual leave', style_tablehead_title)
        ws_reconcile.write(1, 8, 'Responsibility', style_tablehead_title)
        ws_reconcile.write(1, 9, 'Travel', style_tablehead_title)
        ws_reconcile.write(1, 10, 'Seniority Bonus', style_tablehead_title)
        ws_reconcile.write(1, 11, 'Others', style_tablehead_title)
        ws_reconcile.write(1, 12, 'OTC Incentive', style_tablehead_title)
        ws_reconcile.write(1, 13, 'KPI Achievement', style_tablehead_title)
        ws_reconcile.write(1, 14, 'Incentive last month', style_tablehead_title)
        ws_reconcile.write(1, 15, '13th salary (pro-rata)', style_tablehead_title)
        ws_reconcile.write(1, 16, 'Incentive last quarter', style_tablehead_title)
        ws_reconcile.write(1, 17, 'Taxable Overtime', style_tablehead_title)
        ws_reconcile.write(1, 18, 'Non Taxable Overtime', style_tablehead_title)
        ws_reconcile.write(1, 19, 'SHUI(10.5%)(Employee pay)', style_tablehead_title)
        ws_reconcile.write(1, 20, 'SHUI(21.5%)(Company pay)', style_tablehead_title)
        ws_reconcile.write(1, 21, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_tablehead_title)
        ws_reconcile.write(1, 22, 'Trade Union fee (Company pay)', style_tablehead_title)
        ws_reconcile.write(1, 23, 'Trade Union fee (Employee pay)', style_tablehead_title)
        ws_reconcile.write(1, 24, 'Family deduction', style_tablehead_title)
        ws_reconcile.write(1, 25, 'Taxable Income ', style_tablehead_title)
        ws_reconcile.write(1, 26, 'Taxed Income', style_tablehead_title)
        ws_reconcile.write(1, 27, 'PIT', style_tablehead_title)
        ws_reconcile.write(1, 28, 'Net Income', style_tablehead_title)
        ws_reconcile.write(1, 29, 'Total Cost', style_tablehead_title)
        
        # Blank line
        for blank_col in range(1,30): 
            ws_reconcile.write(2, blank_col, '', style_7pt_bold_horizcenter_vertcenter_allthin_but_topdot_colorlightblue)
        
        # Last month staff
        ws_reconcile.write(3, 0, str(last_period_month.month_name) + ' - staff', style_10pt_bold_horizleft_vertcenter_allthin_but_botdot)
        ws_reconcile.write(3, 1, '', style_headcount_staff)
        ws_reconcile.write(3, 2, str(payroll_staff_last_month['head_count']), style_headcount_staff)
        ws_reconcile.write(3, 3, str("{:,}".format(round(payroll_staff_last_month['gross_income']),0)), style_body_staff)
        ws_reconcile.write(3, 4, str("{:,}".format(round(payroll_staff_last_month['transportation']),0)), style_body_staff)
        ws_reconcile.write(3, 5, str("{:,}".format(round(payroll_staff_last_month['phone']),0)), style_body_staff)
        ws_reconcile.write(3, 6, str("{:,}".format(round(payroll_staff_last_month['lunch']),0)), style_body_staff)
        ws_reconcile.write(3, 7, str("{:,}".format(round(payroll_staff_last_month['outstanding_annual_leave']),0)), style_body_staff)
        ws_reconcile.write(3, 8, str("{:,}".format(round(payroll_staff_last_month['responsibility']),0)), style_body_staff)
        ws_reconcile.write(3, 9, str("{:,}".format(round(payroll_staff_last_month['travel']),0)), style_body_staff)
        ws_reconcile.write(3, 10, str("{:,}".format(round(payroll_staff_last_month['seniority_bonus']),0)), style_body_staff)
        ws_reconcile.write(3, 11, str("{:,}".format(round(payroll_staff_last_month['other']),0)), style_body_staff)
        ws_reconcile.write(3, 12, str("{:,}".format(round(payroll_staff_last_month['OTC_incentive']),0)), style_body_staff)
        ws_reconcile.write(3, 13, str("{:,}".format(round(payroll_staff_last_month['KPI_achievement']),0)), style_body_staff)
        ws_reconcile.write(3, 14, str("{:,}".format(round(payroll_staff_last_month['incentive_last_month']),0)), style_body_staff)
        ws_reconcile.write(3, 15, str("{:,}".format(round(payroll_staff_last_month['month_13_salary_Pro_ata']),0)), style_body_staff)
        ws_reconcile.write(3, 16, str("{:,}".format(round(payroll_staff_last_month['incentive_last_quy_last_year']),0)), style_body_staff)
        ws_reconcile.write(3, 17, str("{:,}".format(round(payroll_staff_last_month['taxable_overtime']),0)), style_body_staff)
        ws_reconcile.write(3, 18, str("{:,}".format(round(payroll_staff_last_month['nontaxable_overtime']),0)), style_body_staff)
        ws_reconcile.write(3, 19, str("{:,}".format(round(payroll_staff_last_month['SHUI_10point5percent_employee_pay']),0)), style_body_staff)
        ws_reconcile.write(3, 20, str("{:,}".format(round(payroll_staff_last_month['SHUI_21point5percent_company_pay']),0)), style_body_staff)
        ws_reconcile.write(3, 21, str("{:,}".format(round(payroll_staff_last_month['occupational_accident_and_disease']),0)), style_body_staff)
        ws_reconcile.write(3, 22, str("{:,}".format(round(payroll_staff_last_month['trade_union_fee_company_pay']),0)), style_body_staff)
        ws_reconcile.write(3, 23, str("{:,}".format(round(payroll_staff_last_month['trade_union_fee_employee_pay']),0)), style_body_staff)
        ws_reconcile.write(3, 24, str("{:,}".format(round(payroll_staff_last_month['family_deduction']),0)), style_body_staff)
        ws_reconcile.write(3, 25, str("{:,}".format(round(payroll_staff_last_month['taxable_income']),0)), style_body_staff)
        ws_reconcile.write(3, 26, str("{:,}".format(round(payroll_staff_last_month['taxed_income']),0)), style_body_staff)
        ws_reconcile.write(3, 27, str("{:,}".format(round(payroll_staff_last_month['PIT']),0)), style_body_staff)
        ws_reconcile.write(3, 28, str("{:,}".format(round(payroll_staff_last_month['net_income']),0)), style_body_staff)
        ws_reconcile.write(3, 29, str("{:,}".format(round(payroll_staff_last_month['total_cost']),0)), style_body_staff)
        
        # Last month coll
        ws_reconcile.write(4, 0, str(last_period_month.month_name) + ' - Coll', style_10pt_bold_horizleft_vertcenter_alldot_but_rightthin)
        ws_reconcile.write(4, 1, '', style_headcount_coll)
        ws_reconcile.write(4, 2, str(payroll_coll_last_month['head_count']), style_headcount_coll)
        ws_reconcile.write(4, 3, str("{:,}".format(round(payroll_coll_last_month['gross_income']),0)), style_body_coll)
        ws_reconcile.write(4, 4, str("{:,}".format(round(payroll_coll_last_month['transportation']),0)), style_body_coll)
        ws_reconcile.write(4, 5, str("{:,}".format(round(payroll_coll_last_month['phone']),0)), style_body_coll)
        ws_reconcile.write(4, 6, str("{:,}".format(round(payroll_coll_last_month['lunch']),0)), style_body_coll)
        ws_reconcile.write(4, 7, str("{:,}".format(round(payroll_coll_last_month['outstanding_annual_leave']),0)), style_body_coll)
        ws_reconcile.write(4, 8, str("{:,}".format(round(payroll_coll_last_month['responsibility']),0)), style_body_coll)
        ws_reconcile.write(4, 9, str("{:,}".format(round(payroll_coll_last_month['travel']),0)), style_body_coll)
        ws_reconcile.write(4, 10, str("{:,}".format(round(payroll_coll_last_month['seniority_bonus']),0)), style_body_coll)
        ws_reconcile.write(4, 11, str("{:,}".format(round(payroll_coll_last_month['other']),0)), style_body_coll)
        ws_reconcile.write(4, 12, str("{:,}".format(round(payroll_coll_last_month['OTC_incentive']),0)), style_body_coll)
        ws_reconcile.write(4, 13, str("{:,}".format(round(payroll_coll_last_month['KPI_achievement']),0)), style_body_coll)
        ws_reconcile.write(4, 14, str("{:,}".format(round(payroll_coll_last_month['incentive_last_month']),0)), style_body_coll)
        ws_reconcile.write(4, 15, str("{:,}".format(round(payroll_coll_last_month['month_13_salary_Pro_ata']),0)), style_body_coll)
        ws_reconcile.write(4, 16, str("{:,}".format(round(payroll_coll_last_month['incentive_last_quy_last_year']),0)), style_body_coll)
        ws_reconcile.write(4, 17, str("{:,}".format(round(payroll_coll_last_month['taxable_overtime']),0)), style_body_coll)
        ws_reconcile.write(4, 18, str("{:,}".format(round(payroll_coll_last_month['nontaxable_overtime']),0)), style_body_coll)
        ws_reconcile.write(4, 19, str("{:,}".format(round(payroll_coll_last_month['SHUI_10point5percent_employee_pay']),0)), style_body_coll)
        ws_reconcile.write(4, 20, str("{:,}".format(round(payroll_coll_last_month['SHUI_21point5percent_company_pay']),0)), style_body_coll)
        ws_reconcile.write(4, 21, str("{:,}".format(round(payroll_coll_last_month['occupational_accident_and_disease']),0)), style_body_coll)
        ws_reconcile.write(4, 22, str("{:,}".format(round(payroll_coll_last_month['trade_union_fee_company_pay']),0)), style_body_coll)
        ws_reconcile.write(4, 23, str("{:,}".format(round(payroll_coll_last_month['trade_union_fee_employee_pay']),0)), style_body_coll)
        ws_reconcile.write(4, 24, str("{:,}".format(round(payroll_coll_last_month['family_deduction']),0)), style_body_coll)
        ws_reconcile.write(4, 25, str("{:,}".format(round(payroll_coll_last_month['taxable_income']),0)), style_body_coll)
        ws_reconcile.write(4, 26, str("{:,}".format(round(payroll_coll_last_month['taxed_income']),0)), style_body_coll)
        ws_reconcile.write(4, 27, str("{:,}".format(round(payroll_coll_last_month['PIT']),0)), style_body_coll)
        ws_reconcile.write(4, 28, str("{:,}".format(round(payroll_coll_last_month['net_income']),0)), style_body_coll)
        ws_reconcile.write(4, 29, str("{:,}".format(round(payroll_coll_last_month['total_cost']),0)), style_body_coll)
        
        # Last month Ser
        ws_reconcile.write(5, 0, str(last_period_month.month_name) + ' - Séverine Edgard - Rosa', style_10pt_bold_horizleft_vertcenter_allthin_but_topdot)
        ws_reconcile.write(5, 1, '', style_headcount_ser)
        ws_reconcile.write(5, 2, str(payroll_ser_last_month['head_count']), style_headcount_ser)
        ws_reconcile.write(5, 3, str("{:,}".format(round(payroll_ser_last_month['gross_income']),0)), style_body_ser)
        ws_reconcile.write(5, 4, '', style_body_ser)
        ws_reconcile.write(5, 5, '', style_body_ser)
        ws_reconcile.write(5, 6, '', style_body_ser)
        ws_reconcile.write(5, 7, '', style_body_ser)
        ws_reconcile.write(5, 8, '', style_body_ser)
        ws_reconcile.write(5, 9, '', style_body_ser)
        ws_reconcile.write(5, 10, '', style_body_ser)
        ws_reconcile.write(5, 11, '', style_body_ser)
        ws_reconcile.write(5, 12, '', style_body_ser)
        ws_reconcile.write(5, 13, '', style_body_ser)
        ws_reconcile.write(5, 14, '', style_body_ser)
        ws_reconcile.write(5, 15, '', style_body_ser)
        ws_reconcile.write(5, 16, '', style_body_ser)
        ws_reconcile.write(5, 17, '', style_body_ser)
        ws_reconcile.write(5, 18, '', style_body_ser)
        ws_reconcile.write(5, 19, '', style_body_ser)
        ws_reconcile.write(5, 20, str("{:,}".format(round(payroll_ser_last_month['SHUI_21point5percent_company_pay']),0)), style_body_ser)
        ws_reconcile.write(5, 21, '', style_body_ser)
        ws_reconcile.write(5, 22, str("{:,}".format(round(payroll_ser_last_month['trade_union_fee_company_pay']),0)), style_body_ser)
        ws_reconcile.write(5, 23, '', style_body_ser)
        ws_reconcile.write(5, 24, '', style_body_ser)
        ws_reconcile.write(5, 25, '', style_body_ser)
        ws_reconcile.write(5, 26, '', style_body_ser)
        ws_reconcile.write(5, 27, str("{:,}".format(round(payroll_ser_last_month['PIT']),0)), style_body_ser)
        ws_reconcile.write(5, 28, str("{:,}".format(round(payroll_ser_last_month['net_income']),0)), style_body_ser)
        ws_reconcile.write(5, 29, str("{:,}".format(round(payroll_ser_last_month['total_cost']),0)), style_body_ser)
        
        
        # This month staff
        ws_reconcile.write(6, 0, str(period_month.month_name) + ' - staff', style_10pt_bold_horizleft_vertcenter_allthin_but_botdot)
        ws_reconcile.write(6, 1, '', style_headcount_staff)
        ws_reconcile.write(6, 2, str(payroll_staff_this_month['head_count']), style_headcount_staff)
        ws_reconcile.write(6, 3, str("{:,}".format(round(payroll_staff_this_month['gross_income']),0)), style_body_staff)
        ws_reconcile.write(6, 4, str("{:,}".format(round(payroll_staff_this_month['transportation']),0)), style_body_staff)
        ws_reconcile.write(6, 5, str("{:,}".format(round(payroll_staff_this_month['phone']),0)), style_body_staff)
        ws_reconcile.write(6, 6, str("{:,}".format(round(payroll_staff_this_month['lunch']),0)), style_body_staff)
        ws_reconcile.write(6, 7, str("{:,}".format(round(payroll_staff_this_month['outstanding_annual_leave']),0)), style_body_staff)
        ws_reconcile.write(6, 8, str("{:,}".format(round(payroll_staff_this_month['responsibility']),0)), style_body_staff)
        ws_reconcile.write(6, 9, str("{:,}".format(round(payroll_staff_this_month['travel']),0)), style_body_staff)
        ws_reconcile.write(6, 10, str("{:,}".format(round(payroll_staff_this_month['seniority_bonus']),0)), style_body_staff)
        ws_reconcile.write(6, 11, str("{:,}".format(round(payroll_staff_this_month['other']),0)), style_body_staff)
        ws_reconcile.write(6, 12, str("{:,}".format(round(payroll_staff_this_month['OTC_incentive']),0)), style_body_staff)
        ws_reconcile.write(6, 13, str("{:,}".format(round(payroll_staff_this_month['KPI_achievement']),0)), style_body_staff)
        ws_reconcile.write(6, 14, str("{:,}".format(round(payroll_staff_this_month['incentive_last_month']),0)), style_body_staff)
        ws_reconcile.write(6, 15, str("{:,}".format(round(payroll_staff_this_month['month_13_salary_Pro_ata']),0)), style_body_staff)
        ws_reconcile.write(6, 16, str("{:,}".format(round(payroll_staff_this_month['incentive_last_quy_last_year']),0)), style_body_staff)
        ws_reconcile.write(6, 17, str("{:,}".format(round(payroll_staff_this_month['taxable_overtime']),0)), style_body_staff)
        ws_reconcile.write(6, 18, str("{:,}".format(round(payroll_staff_this_month['nontaxable_overtime']),0)), style_body_staff)
        ws_reconcile.write(6, 19, str("{:,}".format(round(payroll_staff_this_month['SHUI_10point5percent_employee_pay']),0)), style_body_staff)
        ws_reconcile.write(6, 20, str("{:,}".format(round(payroll_staff_this_month['SHUI_21point5percent_company_pay']),0)), style_body_staff)
        ws_reconcile.write(6, 21, str("{:,}".format(round(payroll_staff_this_month['occupational_accident_and_disease']),0)), style_body_staff)
        ws_reconcile.write(6, 22, str("{:,}".format(round(payroll_staff_this_month['trade_union_fee_company_pay']),0)), style_body_staff)
        ws_reconcile.write(6, 23, str("{:,}".format(round(payroll_staff_this_month['trade_union_fee_employee_pay']),0)), style_body_staff)
        ws_reconcile.write(6, 24, str("{:,}".format(round(payroll_staff_this_month['family_deduction']),0)), style_body_staff)
        ws_reconcile.write(6, 25, str("{:,}".format(round(payroll_staff_this_month['taxable_income']),0)), style_body_staff)
        ws_reconcile.write(6, 26, str("{:,}".format(round(payroll_staff_this_month['taxed_income']),0)), style_body_staff)
        ws_reconcile.write(6, 27, str("{:,}".format(round(payroll_staff_this_month['PIT']),0)), style_body_staff)
        ws_reconcile.write(6, 28, str("{:,}".format(round(payroll_staff_this_month['net_income']),0)), style_body_staff)
        ws_reconcile.write(6, 29, str("{:,}".format(round(payroll_staff_this_month['total_cost']),0)), style_body_staff)
        
        # This month coll
        ws_reconcile.write(7, 0, str(period_month.month_name) + ' - Coll', style_10pt_bold_horizleft_vertcenter_alldot_but_rightthin)
        ws_reconcile.write(7, 1, '', style_headcount_coll)
        ws_reconcile.write(7, 2, str(payroll_coll_this_month['head_count']), style_headcount_coll)
        ws_reconcile.write(7, 3, str("{:,}".format(round(payroll_coll_this_month['gross_income']),0)), style_body_coll)
        ws_reconcile.write(7, 4, str("{:,}".format(round(payroll_coll_this_month['transportation']),0)), style_body_coll)
        ws_reconcile.write(7, 5, str("{:,}".format(round(payroll_coll_this_month['phone']),0)), style_body_coll)
        ws_reconcile.write(7, 6, str("{:,}".format(round(payroll_coll_this_month['lunch']),0)), style_body_coll)
        ws_reconcile.write(7, 7, str("{:,}".format(round(payroll_coll_this_month['outstanding_annual_leave']),0)), style_body_coll)
        ws_reconcile.write(7, 8, str("{:,}".format(round(payroll_coll_this_month['responsibility']),0)), style_body_coll)
        ws_reconcile.write(7, 9, str("{:,}".format(round(payroll_coll_this_month['travel']),0)), style_body_coll)
        ws_reconcile.write(7, 10, str("{:,}".format(round(payroll_coll_this_month['seniority_bonus']),0)), style_body_coll)
        ws_reconcile.write(7, 11, str("{:,}".format(round(payroll_coll_this_month['other']),0)), style_body_coll)
        ws_reconcile.write(7, 12, str("{:,}".format(round(payroll_coll_this_month['OTC_incentive']),0)), style_body_coll)
        ws_reconcile.write(7, 13, str("{:,}".format(round(payroll_coll_this_month['KPI_achievement']),0)), style_body_coll)
        ws_reconcile.write(7, 14, str("{:,}".format(round(payroll_coll_this_month['incentive_last_month']),0)), style_body_coll)
        ws_reconcile.write(7, 15, str("{:,}".format(round(payroll_coll_this_month['month_13_salary_Pro_ata']),0)), style_body_coll)
        ws_reconcile.write(7, 16, str("{:,}".format(round(payroll_coll_this_month['incentive_last_quy_last_year']),0)), style_body_coll)
        ws_reconcile.write(7, 17, str("{:,}".format(round(payroll_coll_this_month['taxable_overtime']),0)), style_body_coll)
        ws_reconcile.write(7, 18, str("{:,}".format(round(payroll_coll_this_month['nontaxable_overtime']),0)), style_body_coll)
        ws_reconcile.write(7, 19, str("{:,}".format(round(payroll_coll_this_month['SHUI_10point5percent_employee_pay']),0)), style_body_coll)
        ws_reconcile.write(7, 20, str("{:,}".format(round(payroll_coll_this_month['SHUI_21point5percent_company_pay']),0)), style_body_coll)
        ws_reconcile.write(7, 21, str("{:,}".format(round(payroll_coll_this_month['occupational_accident_and_disease']),0)), style_body_coll)
        ws_reconcile.write(7, 22, str("{:,}".format(round(payroll_coll_this_month['trade_union_fee_company_pay']),0)), style_body_coll)
        ws_reconcile.write(7, 23, str("{:,}".format(round(payroll_coll_this_month['trade_union_fee_employee_pay']),0)), style_body_coll)
        ws_reconcile.write(7, 24, str("{:,}".format(round(payroll_coll_this_month['family_deduction']),0)), style_body_coll)
        ws_reconcile.write(7, 25, str("{:,}".format(round(payroll_coll_this_month['taxable_income']),0)), style_body_coll)
        ws_reconcile.write(7, 26, str("{:,}".format(round(payroll_coll_this_month['taxed_income']),0)), style_body_coll)
        ws_reconcile.write(7, 27, str("{:,}".format(round(payroll_coll_this_month['PIT']),0)), style_body_coll)
        ws_reconcile.write(7, 28, str("{:,}".format(round(payroll_coll_this_month['net_income']),0)), style_body_coll)
        ws_reconcile.write(7, 29, str("{:,}".format(round(payroll_coll_this_month['total_cost']),0)), style_body_coll)
        
        # This month Ser
        ws_reconcile.write(8, 0, str(period_month.month_name) + ' - Séverine Edgard - Rosa', style_10pt_bold_horizleft_vertcenter_allthin_but_topdot)
        ws_reconcile.write(8, 1, '', style_headcount_ser)
        ws_reconcile.write(8, 2, str(payroll_ser_this_month['head_count']), style_headcount_ser)
        ws_reconcile.write(8, 3, str("{:,}".format(round(payroll_ser_this_month['gross_income']),0)), style_body_ser)
        ws_reconcile.write(8, 4, '', style_body_ser)
        ws_reconcile.write(8, 5, '', style_body_ser)
        ws_reconcile.write(8, 6, '', style_body_ser)
        ws_reconcile.write(8, 7, '', style_body_ser)
        ws_reconcile.write(8, 8, '', style_body_ser)
        ws_reconcile.write(8, 9, '', style_body_ser)
        ws_reconcile.write(8, 10, '', style_body_ser)
        ws_reconcile.write(8, 11, '', style_body_ser)
        ws_reconcile.write(8, 12, '', style_body_ser)
        ws_reconcile.write(8, 13, '', style_body_ser)
        ws_reconcile.write(8, 14, '', style_body_ser)
        ws_reconcile.write(8, 15, '', style_body_ser)
        ws_reconcile.write(8, 16, '', style_body_ser)
        ws_reconcile.write(8, 17, '', style_body_ser)
        ws_reconcile.write(8, 18, '', style_body_ser)
        ws_reconcile.write(8, 19, '', style_body_ser)
        ws_reconcile.write(8, 20, str("{:,}".format(round(payroll_ser_this_month['SHUI_21point5percent_company_pay']),0)), style_body_ser)
        ws_reconcile.write(8, 21, '', style_body_ser)
        ws_reconcile.write(8, 22, str("{:,}".format(round(payroll_ser_this_month['trade_union_fee_company_pay']),0)), style_body_ser)
        ws_reconcile.write(8, 23, '', style_body_ser)
        ws_reconcile.write(8, 24, '', style_body_ser)
        ws_reconcile.write(8, 25, '', style_body_ser)
        ws_reconcile.write(8, 26, '', style_body_ser)
        ws_reconcile.write(8, 27, str("{:,}".format(round(payroll_ser_this_month['PIT']),0)), style_body_ser)
        ws_reconcile.write(8, 28, str("{:,}".format(round(payroll_ser_this_month['net_income']),0)), style_body_ser)
        ws_reconcile.write(8, 29, str("{:,}".format(round(payroll_ser_this_month['total_cost']),0)), style_body_ser)
        
        
        # Difference btw last and this
        ws_reconcile.write(9, 0, 'Difference btw ' +  str(last_period_month.month_name) + ' & ' +  str(period_month.month_name), style_10pt_bold_horizleft_vertcenter_allthin)
        ws_reconcile.write(9, 1, '', style_headcount_diff)
        ws_reconcile.write(9, 2, str(difference_last_this['head_count']), style_headcount_diff)
        ws_reconcile.write(9, 3, str("{:,}".format(round(difference_last_this['gross_income']),0)), style_body_diff)
        ws_reconcile.write(9, 4, str("{:,}".format(round(difference_last_this['transportation']),0)), style_body_diff)
        ws_reconcile.write(9, 5, str("{:,}".format(round(difference_last_this['phone']),0)), style_body_diff)
        ws_reconcile.write(9, 6, str("{:,}".format(round(difference_last_this['lunch']),0)), style_body_diff)
        ws_reconcile.write(9, 7, str("{:,}".format(round(difference_last_this['outstanding_annual_leave']),0)), style_body_diff)
        ws_reconcile.write(9, 8, str("{:,}".format(round(difference_last_this['responsibility']),0)), style_body_diff)
        ws_reconcile.write(9, 9, str("{:,}".format(round(difference_last_this['travel']),0)), style_body_diff)
        ws_reconcile.write(9, 10, str("{:,}".format(round(difference_last_this['seniority_bonus']),0)), style_body_diff)
        ws_reconcile.write(9, 11, str("{:,}".format(round(difference_last_this['other']),0)), style_body_diff)
        ws_reconcile.write(9, 12, str("{:,}".format(round(difference_last_this['OTC_incentive']),0)), style_body_diff)
        ws_reconcile.write(9, 13, str("{:,}".format(round(difference_last_this['KPI_achievement']),0)), style_body_diff)
        ws_reconcile.write(9, 14, str("{:,}".format(round(difference_last_this['incentive_last_month']),0)), style_body_diff)
        ws_reconcile.write(9, 15, str("{:,}".format(round(difference_last_this['month_13_salary_Pro_ata']),0)), style_body_diff)
        ws_reconcile.write(9, 16, str("{:,}".format(round(difference_last_this['incentive_last_quy_last_year']),0)), style_body_diff)
        ws_reconcile.write(9, 17, str("{:,}".format(round(difference_last_this['taxable_overtime']),0)), style_body_diff)
        ws_reconcile.write(9, 18, str("{:,}".format(round(difference_last_this['nontaxable_overtime']),0)), style_body_diff)
        ws_reconcile.write(9, 19, str("{:,}".format(round(difference_last_this['SHUI_10point5percent_employee_pay']),0)), style_body_diff)
        ws_reconcile.write(9, 20, str("{:,}".format(round(difference_last_this['SHUI_21point5percent_company_pay']),0)), style_body_diff)
        ws_reconcile.write(9, 21, str("{:,}".format(round(difference_last_this['occupational_accident_and_disease']),0)), style_body_diff)
        ws_reconcile.write(9, 22, str("{:,}".format(round(difference_last_this['trade_union_fee_company_pay']),0)), style_body_diff)
        ws_reconcile.write(9, 23, str("{:,}".format(round(difference_last_this['trade_union_fee_employee_pay']),0)), style_body_diff)
        ws_reconcile.write(9, 24, str("{:,}".format(round(difference_last_this['family_deduction']),0)), style_body_diff)
        ws_reconcile.write(9, 25, str("{:,}".format(round(difference_last_this['taxable_income']),0)), style_body_diff)
        ws_reconcile.write(9, 26, str("{:,}".format(round(difference_last_this['taxed_income']),0)), style_body_diff)
        ws_reconcile.write(9, 27, str("{:,}".format(round(difference_last_this['PIT']),0)), style_body_diff)
        ws_reconcile.write(9, 28, str("{:,}".format(round(difference_last_this['net_income']),0)), style_body_diff)
        ws_reconcile.write(9, 29, str("{:,}".format(round(difference_last_this['total_cost']),0)), style_body_diff)
        
        
        # Explain
        ws_reconcile.write(10, 0, 'Explain', style_10pt_bold_horizleft_vertcenter_allthin)
        ws_reconcile.write(10, 1, '', style_headcount_diff)
        ws_reconcile.write(10, 2, '', style_headcount_diff)
        ws_reconcile.write(10, 3, '', style_body_diff)
        ws_reconcile.write(10, 4, '', style_body_diff)
        ws_reconcile.write(10, 5, '', style_body_diff)
        ws_reconcile.write(10, 6, '', style_body_diff)
        ws_reconcile.write(10, 7, '', style_headcount_diff)
        ws_reconcile.write(10, 8, '', style_headcount_diff)
        ws_reconcile.write(10, 9, '', style_body_diff)
        ws_reconcile.write(10, 10, '', style_body_diff)
        ws_reconcile.write(10, 11, '', style_body_diff)
        ws_reconcile.write(10, 12, '', style_body_diff)
        ws_reconcile.write(10, 13, '', style_headcount_diff)
        ws_reconcile.write(10, 14, '', style_headcount_diff)
        ws_reconcile.write(10, 15, '', style_body_diff)
        ws_reconcile.write(10, 16, '', style_body_diff)
        ws_reconcile.write(10, 17, '', style_body_diff)
        ws_reconcile.write(10, 18, '', style_body_diff)
        ws_reconcile.write(10, 19, '', style_headcount_diff)
        ws_reconcile.write(10, 20, '', style_headcount_diff)
        ws_reconcile.write(10, 21, '', style_body_diff)
        ws_reconcile.write(10, 22, '', style_body_diff)
        ws_reconcile.write(10, 23, '', style_body_diff)
        ws_reconcile.write(10, 24, '', style_body_diff)
        ws_reconcile.write(10, 25, '', style_headcount_diff)
        ws_reconcile.write(10, 26, '', style_body_diff)
        ws_reconcile.write(10, 27, '', style_body_diff)
        ws_reconcile.write(10, 28, '', style_body_diff)
        ws_reconcile.write(10, 29, '', style_body_diff)

        for index, data in enumerate(list_data):    
            # Set row height
            ws_reconcile.row(11+index).height_mismatch = True
            ws_reconcile.row(11+index).height = 600
            # Write data
            ws_reconcile.write(11+index, 0, str(data['remark']),style_explain_remark_employeename)
            ws_reconcile.write(11+index, 1, str(data['employee'].full_name),style_explain_remark_employeename)
            ws_reconcile.write(11+index, 2, str(data['head_count']),style_explain_data)
         
        # last_row_new_staff = 6 + new_staff_reports.count()
        # ws_reconcile.row(last_row_new_staff).height_mismatch = True
        # ws_reconcile.row(last_row_new_staff).height = 525
        
        # '''Resigned staff'''
        # # Set row height
        # ws_reconcile.row(last_row_new_staff + 1).height_mismatch = True
        # ws_reconcile.row(last_row_new_staff + 1).height = 300
        # ws_reconcile.row(last_row_new_staff + 2).height_mismatch = True
        # ws_reconcile.row(last_row_new_staff + 2).height = 525
        # # Table-head
        # ws_reconcile.write(last_row_new_staff + 1, 0, 'CONFIRMED AFTER PROBATION', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 1, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 2, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 3, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 4, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 5, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 6, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 7, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 8, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 9, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 10, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 11, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 12, '', style_tablehead_title)
        # ws_reconcile.write(last_row_new_staff + 1, 13, '', style_tablehead_title)
        
        # ws_reconcile.write(last_row_new_staff + 2, 0, 'No.', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 1, '', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 2, 'Name', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 3, 'Dept', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 4, 'Joining date', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 5, 'Sign LC date', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 6, 'Allowance', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 7, 'Sal. After probation', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 8, 'SI Book no.', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 9, 'Hospital for HI', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 10, '', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 11, '', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 12, '', style_tablehead)
        # ws_reconcile.write(last_row_new_staff + 2, 13, '', style_tablehead)
        # # Table-Body
        # confirmed_after_probation_reports = Report_confirmed_after_probation_Tedis_VietHa.objects.filter(month=period_month)
        # # Make subtotal var
        # for index, report in enumerate(confirmed_after_probation_reports):    
        #     # Set row height
        #     ws_reconcile.row(last_row_new_staff+3+index).height_mismatch = True
        #     ws_reconcile.row(last_row_new_staff+3+index).height = 525
        #     # Write data
        #     ws_reconcile.write(last_row_new_staff+3+index, 0, str(index + 1),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 1, str(report.employee.employee_code),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 2, str(report.employee.full_name),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 3, str(report.department),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 4, report.joining_date.strftime('%#d-%b-%Y'),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 5, report.sign_LC_date.strftime('%#d-%b-%Y'),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 6, str("{:,}".format(round(report.allowance),0)),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 7, str("{:,}".format(round(report.salary_after_probation),0)),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 8, str(report.SI_book_no),style_body)
        #     ws_reconcile.write(last_row_new_staff+3+index, 9, str(report.hospital_for_HI),style_body)
        # last_row_confirmed_after_probation = last_row_new_staff+3 + confirmed_after_probation_reports.count()
        # ws_reconcile.row(last_row_confirmed_after_probation).height_mismatch = True
        # ws_reconcile.row(last_row_confirmed_after_probation).height = 525
        
        # '''Resigned staff'''
        # # Set row height
        # ws_reconcile.row(last_row_confirmed_after_probation + 1).height_mismatch = True
        # ws_reconcile.row(last_row_confirmed_after_probation + 1).height = 300
        # ws_reconcile.row(last_row_confirmed_after_probation + 2).height_mismatch = True
        # ws_reconcile.row(last_row_confirmed_after_probation + 2).height = 525
        # # Table-head
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 0, 'RESIGNED STAFF', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 1, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 2, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 3, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 4, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 5, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 6, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 7, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 8, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 9, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 10, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 11, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 12, '', style_tablehead_title)
        # ws_reconcile.write(last_row_confirmed_after_probation + 1, 13, '', style_tablehead_title)
        
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 0, 'No.', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 1, '', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 2, 'Name', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 3, 'Dept', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 4, 'Joining date', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 5, 'Leaving date', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 6, 'Allowance', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 7, 'Unused AL', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 8, '13th month salary', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 9, 'Severance Allowance', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 10, 'Other allowance', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 11, 'Incentive', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 12, 'Remark', style_tablehead)
        # ws_reconcile.write(last_row_confirmed_after_probation + 2, 13, '', style_tablehead)
        # # Table-Body
        # resigned_staff_reports = Report_resigned_staff_Tedis_VietHa.objects.filter(month=period_month)
        # # Make subtotal var
        # for index, report in enumerate(resigned_staff_reports):    
        #     # Set row height
        #     ws_reconcile.row(last_row_confirmed_after_probation+3+index).height_mismatch = True
        #     ws_reconcile.row(last_row_confirmed_after_probation+3+index).height = 525
        #     # Write data
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 0, str(index + 1),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 1, str(report.employee.employee_code),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 2, str(report.employee.full_name),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 3, str(report.department),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 4, report.joining_date.strftime('%#d-%b-%Y'),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 5, report.leaving_date.strftime('%#d-%b-%Y'),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 6, str("{:,}".format(round(report.allowance),0)),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 7, str("{:,}".format(round(report.unused_AL),0)),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 8, str("{:,}".format(round(report.month_13_salary),0)),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 9, str("{:,}".format(round(report.severance_allowance),0)),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 10, str("{:,}".format(round(report.other_allowance),0)),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 11, str("{:,}".format(round(report.incentive),0)),style_body)
        #     ws_reconcile.write(last_row_confirmed_after_probation+3+index, 12, str(report.remark),style_body)
        # last_row_resigned_staff = last_row_confirmed_after_probation+3 + resigned_staff_reports.count()
        # ws_reconcile.row(last_row_resigned_staff).height_mismatch = True
        # ws_reconcile.row(last_row_resigned_staff).height = 525
        
        
        # '''Other changes'''
        # # Set row height
        # ws_reconcile.row(last_row_resigned_staff + 1).height_mismatch = True
        # ws_reconcile.row(last_row_resigned_staff + 1).height = 300
        # ws_reconcile.row(last_row_resigned_staff + 2).height_mismatch = True
        # ws_reconcile.row(last_row_resigned_staff + 2).height = 525
        # # Table-head
        # ws_reconcile.write(last_row_resigned_staff + 1, 0, 'OTHER CHANGES', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 1, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 2, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 3, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 4, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 5, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 6, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 7, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 8, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 9, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 10, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 11, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 12, '', style_tablehead_title)
        # ws_reconcile.write(last_row_resigned_staff + 1, 13, '', style_tablehead_title)
        
        # ws_reconcile.write(last_row_resigned_staff + 2, 0, 'No.', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 1, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 2, 'Name', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 3, 'New Salary', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 4, 'Allowance', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 5, 'Effective date', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 6, 'Remark', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 7, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 8, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 9, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 10, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 11, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 12, '', style_tablehead)
        # ws_reconcile.write(last_row_resigned_staff + 2, 13, '', style_tablehead)
        # # Table-Body
        # other_changes_reports = Report_other_changes_Tedis_VietHa.objects.filter(month=period_month)
        # # Make subtotal var
        # for index, report in enumerate(other_changes_reports):    
        #     # Set row height
        #     ws_reconcile.row(last_row_resigned_staff+3+index).height_mismatch = True
        #     ws_reconcile.row(last_row_resigned_staff+3+index).height = 525
        #     # Write data
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 0, str(index + 1),style_body)
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 1, str(report.employee.employee_code),style_body)
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 2, str(report.employee.full_name),style_body)
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 3, str("{:,}".format(round(report.new_salary),0)),style_body)
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 4, str("{:,}".format(round(report.allowance),0)),style_body)
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 5, report.effective_date.strftime('%#d-%b-%Y'),style_body)
        #     ws_reconcile.write(last_row_resigned_staff+3+index, 6, str(report.remark),style_body)
        # last_row_other_changes = last_row_resigned_staff+3 + resigned_staff_reports.count()
        # ws_reconcile.row(last_row_other_changes).height_mismatch = True
        # ws_reconcile.row(last_row_other_changes).height = 525
        
        # '''Maternity leave'''
        # # Set row height
        # ws_reconcile.row(last_row_other_changes + 1).height_mismatch = True
        # ws_reconcile.row(last_row_other_changes + 1).height = 300
        # ws_reconcile.row(last_row_other_changes + 2).height_mismatch = True
        # ws_reconcile.row(last_row_other_changes + 2).height = 525
        # # Table-head
        # ws_reconcile.write(last_row_other_changes + 1, 0, 'MATERNITY LEAVE', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 1, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 2, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 3, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 4, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 5, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 6, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 7, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 8, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 9, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 10, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 11, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 12, '', style_tablehead_title)
        # ws_reconcile.write(last_row_other_changes + 1, 13, '', style_tablehead_title)
        
        # ws_reconcile.write(last_row_other_changes + 2, 0, 'No.', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 1, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 2, 'Name', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 3, 'Dept', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 4, 'From', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 5, 'To', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 6, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 7, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 8, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 9, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 10, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 11, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 12, '', style_tablehead)
        # ws_reconcile.write(last_row_other_changes + 2, 13, '', style_tablehead)
        # # Table-Body
        # maternity_leave_reports = Report_maternity_leave_Tedis_VietHa.objects.filter(month=period_month)
        # # Make subtotal var
        # for index, report in enumerate(maternity_leave_reports):    
        #     # Set row height
        #     ws_reconcile.row(last_row_other_changes+3+index).height_mismatch = True
        #     ws_reconcile.row(last_row_other_changes+3+index).height = 525
        #     # Write data
        #     ws_reconcile.write(last_row_other_changes+3+index, 0, str(index + 1),style_body)
        #     ws_reconcile.write(last_row_other_changes+3+index, 1, str(report.employee.employee_code),style_body)
        #     ws_reconcile.write(last_row_other_changes+3+index, 2, str(report.employee.full_name),style_body)
        #     ws_reconcile.write(last_row_other_changes+3+index, 3, str(report.department),style_body)
        #     ws_reconcile.write(last_row_other_changes+3+index, 4, report.from_date.strftime('%d/%m/%Y'),style_body)
        #     ws_reconcile.write(last_row_other_changes+3+index, 5, report.to_date.strftime('%d/%m/%Y'),style_body)
        # last_row_maternity_leave = last_row_other_changes+3 + resigned_staff_reports.count()
        # ws_reconcile.row(last_row_maternity_leave).height_mismatch = True
        # ws_reconcile.row(last_row_maternity_leave).height = 525
            
    
        wb.save(response)
        return response
        
        
        
    
    return render(request, 'employee/view_report_payroll_tedis_vietha.html', {
        'period_month' : period_month,
        'list_employee_tedis_vietha' : list_employee_tedis_vietha,
        'list_individual_types' : list_individual_types,
        'report_payrollExist' : report_payrollExist,
        'report_pit_payroll' : report_pit_payroll,
        'report_pit_payroll_canhancutru' : report_pit_payroll_canhancutru,
        'report_pit_payroll_canhankhongcutru' : report_pit_payroll_canhankhongcutru,
        'report_transferStaff_payroll' : report_transferStaff_payroll,
        'report_transferColl_payroll' : report_transferColl_payroll,
        'list_payroll_staff_info' : list_payroll_staff_info,
        'list_payroll_coll_info' : list_payroll_coll_info,
        'payroll_ser' : payroll_ser,
        'report_payment_payroll' : report_payment_payroll,
        # Sheet Infor.Payroll
        'new_staff_reports' : new_staff_reports,
        'confirmed_after_probation_reports' : confirmed_after_probation_reports,
        'resigned_staff_reports' : resigned_staff_reports,
        'other_changes_reports' : other_changes_reports,
        'maternity_leave_reports' : maternity_leave_reports,
        # Reconcile
        'last_period_month' : last_period_month,
        'payroll_staff_last_month' : payroll_staff_last_month,
        'payroll_coll_last_month' : payroll_coll_last_month,
        'payroll_ser_last_month' : payroll_ser_last_month,
        'payroll_staff_this_month' : payroll_staff_this_month,
        'payroll_coll_this_month' : payroll_coll_this_month,
        'payroll_ser_this_month' : payroll_ser_this_month,
        'difference_last_this' : difference_last_this,
        'list_data' : list_data,
        'total_data' : total_data,
        
    })
    

def PIT_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    pit_info = Report_PIT_Payroll_Tedis_VietHa.objects.get(pk=pk)
    
    # Create lists
    list_individual_types = ['','Cá Nhân Cư Trú','Cá Nhân Không Cư Trú']
    
    
    # Update payroll info
    if request.POST.get('btnupdatepit'):
        thuong = request.POST.get('thuong')
        khac = request.POST.get('khac')
        cong = request.POST.get('cong')
        ghi_chu = request.POST.get('ghi_chu')
        individual_type = request.POST.get('individual_type')
        # Get unchange data
        month = pit_info.month
        payroll = pit_info.payroll
        employee = pit_info.employee
        
        thu_nhap_chiu_thue = pit_info.thu_nhap_chiu_thue
        tong_tnct_khau_tru_thue = pit_info.tong_tnct_khau_tru_thue
        bao_hiem_bat_buoc = pit_info.bao_hiem_bat_buoc
        khau_tru = pit_info.khau_tru
        
        thu_nhap_tinh_thue = pit_info.thu_nhap_tinh_thue
        
        thue_tnct_phai_nop = pit_info.thue_tnct_phai_nop
        
        
        # Update and save
        pit_update_info = Report_PIT_Payroll_Tedis_VietHa(id=pit_info.id,thuong=thuong,khac=khac,cong=cong,ghi_chu=ghi_chu,individual_type=individual_type,
                                                   month=month,payroll=payroll,employee=employee,
                                                   thu_nhap_chiu_thue=thu_nhap_chiu_thue,tong_tnct_khau_tru_thue=tong_tnct_khau_tru_thue,bao_hiem_bat_buoc=bao_hiem_bat_buoc,khau_tru=khau_tru,
                                                   thu_nhap_tinh_thue=thu_nhap_tinh_thue,
                                                   thue_tnct_phai_nop=thue_tnct_phai_nop)
        pit_update_info.save()
        messages.success(request, 'SUCCESS: PIT updated')
        return redirect('employee:PIT_report_payroll_tedis_vietha_edit',pk=pit_info.id)
        
        
        
    
    return render(request, 'employee/edit_PIT_report_payroll_tedis_vietha.html', {
        'pit_info' : pit_info,
        'list_individual_types' : list_individual_types,
        
    })
    

def payroll_ser_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    payroll_info = Payroll_Ser.objects.get(pk=pk)

    # Update payroll info
    if request.POST.get('btnupdatePayrollSer'):
        # Get unchange data
        month = payroll_info.month
        employee = payroll_info.employee
        # Get update data
        exchange_rate_usd = request.POST.get('exchange_rate_usd')
        exchange_rate_euro = request.POST.get('exchange_rate_euro')
        salary_usd = request.POST.get('salary_usd')
        salary_vnd = request.POST.get('salary_vnd')
        working_days = request.POST.get('working_days')
        gross_income = request.POST.get('gross_income')
        salary_recuperation = request.POST.get('salary_recuperation')
        housing_euro = request.POST.get('housing_euro')
        housing_vnd = request.POST.get('housing_vnd')
        phone = request.POST.get('phone')
        lunch = request.POST.get('lunch')
        training_fee = request.POST.get('training_fee')
        toxic_allowance = request.POST.get('toxic_allowance')
        travel = request.POST.get('travel')
        responsibility = request.POST.get('responsibility')
        seniority_bonus = request.POST.get('seniority_bonus')
        other = request.POST.get('other')
        total_allowance_recuperation = request.POST.get('total_allowance_recuperation')
        benefits = request.POST.get('benefits')
        severance_allowance = request.POST.get('severance_allowance')
        outstanding_annual_leave = request.POST.get('outstanding_annual_leave')
        month_13_salary_Pro_ata = request.POST.get('month_13_salary_Pro_ata')
        SHUI_9point5percent_employee_pay = request.POST.get('SHUI_9point5percent_employee_pay')
        recuperation_of_SHU_Ins_10point5percent_staff_pay = request.POST.get('recuperation_of_SHU_Ins_10point5percent_staff_pay')
        SHUI_20point5percent_employer_pay = request.POST.get('SHUI_20point5percent_employer_pay')
        recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
        occupational_accident_and_disease = request.POST.get('occupational_accident_and_disease')
        trade_union_fee_company_pay = request.POST.get('trade_union_fee_company_pay')
        trade_union_fee_member = request.POST.get('trade_union_fee_member')
        family_deduction = request.POST.get('family_deduction')
        taxable_income = request.POST.get('taxable_income')
        taxed_income = request.POST.get('taxed_income')
        PIT = request.POST.get('PIT')
        first_payment_cash_advance_euro = request.POST.get('first_payment_cash_advance_euro')
        second_payment_net_income_vnd = request.POST.get('second_payment_net_income_vnd')
        second_payment_net_income_euro = request.POST.get('second_payment_net_income_euro')
        net_income = request.POST.get('net_income')
        total_cost_vnd = request.POST.get('total_cost_vnd')
        total_cost_usd = request.POST.get('total_cost_usd')
        note = request.POST.get('note')
        
        # Update and save
        payroll_update_info = Payroll_Ser(id=payroll_info.id,month=month,employee=employee,
                                       exchange_rate_usd=exchange_rate_usd,exchange_rate_euro=exchange_rate_euro,
                                       salary_usd=salary_usd,salary_vnd=salary_vnd,
                                       working_days=working_days,
                                       gross_income=gross_income,salary_recuperation=salary_recuperation,
                                       housing_euro=housing_euro,housing_vnd=housing_vnd,
                                       phone=phone,lunch=lunch,training_fee=training_fee,toxic_allowance=toxic_allowance,travel=travel,
                                       responsibility=responsibility,seniority_bonus=seniority_bonus,other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,
                                       severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata,SHUI_9point5percent_employee_pay=SHUI_9point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,
                                       SHUI_20point5percent_employer_pay=SHUI_20point5percent_employer_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease=occupational_accident_and_disease,trade_union_fee_company_pay=trade_union_fee_company_pay,trade_union_fee_member=trade_union_fee_member,
                                       family_deduction=family_deduction,taxable_income=taxable_income,taxed_income=taxed_income,PIT=PIT,first_payment_cash_advance_euro=first_payment_cash_advance_euro,
                                       second_payment_net_income_vnd=second_payment_net_income_vnd,second_payment_net_income_euro=second_payment_net_income_euro,net_income=net_income,total_cost_vnd=total_cost_vnd,total_cost_usd=total_cost_usd,
                                       note=note)
        payroll_update_info.save()

        # Update Payment Info
        # Salary + allowance serverine
        payment_salary_and_allowance_ser = Report_Payment_Payroll_Tedis_VietHa.objects.get(month=month,item='SALARY + ALLOWANCE',description='Severine')
        payment_salary_and_allowance_ser_info = Report_Payment_Payroll_Tedis_VietHa(id=payment_salary_and_allowance_ser.id,month=payment_salary_and_allowance_ser.month,
                                                                        item=payment_salary_and_allowance_ser.item,description=payment_salary_and_allowance_ser.description,amount_vnd=payment_salary_and_allowance_ser.amount_vnd,amount_euro=net_income,
                                                                        paidby=payment_salary_and_allowance_ser.paidby,paidto=payment_salary_and_allowance_ser.paidto,account_no=payment_salary_and_allowance_ser.account_no)
        payment_salary_and_allowance_ser_info.save()
        # SHUI Company ser      
        payment_SHUI_Company_ser = Report_Payment_Payroll_Tedis_VietHa.objects.get(id=payment_salary_and_allowance_ser.id + 4) 
        payment_SHUI_Company_ser_info = Report_Payment_Payroll_Tedis_VietHa(id=payment_SHUI_Company_ser.id,month=payment_SHUI_Company_ser.month,
                                                                    item=payment_SHUI_Company_ser.item,description=payment_SHUI_Company_ser.description,amount_vnd=float(SHUI_9point5percent_employee_pay) + float(SHUI_20point5percent_employer_pay),amount_euro=payment_SHUI_Company_ser.amount_euro,
                                                                    paidby=payment_SHUI_Company_ser.paidby,paidto=payment_SHUI_Company_ser.paidto,account_no=payment_SHUI_Company_ser.account_no)
        payment_SHUI_Company_ser_info.save()
        '''PIT'''
        site_JV = Site.objects.get(site='JV')
        list_employee_tedis_vietha = Employee.objects.filter(site=site_JV)
        PIT_info = Report_Payment_Payroll_Tedis_VietHa.objects.get(month=month,item='PIT',description='Salary PIT')
        
        PIT_amount = 0
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha,month=month)
        for payroll in payroll_tedis_vietha:
            PIT_amount += round(payroll.PIT_balance)
        PIT_amount += float(PIT)
        payment_PIT_info = Report_Payment_Payroll_Tedis_VietHa(id=PIT_info.id,month=PIT_info.month,
                                                                item=PIT_info.item,description=PIT_info.description,amount_vnd=PIT_amount,amount_euro=PIT_info.amount_euro,
                                                                paidby=PIT_info.paidby,paidto=PIT_info.paidto,account_no=PIT_info.account_no)
        payment_PIT_info.save()
        # TRADE UNION company
        trade_union_company = Report_Payment_Payroll_Tedis_VietHa.objects.get(month=month,item='TRADE UNION',description='Trade Union fee')
        
        trade_union_company_amount = 0
        payroll_tedis_vietha = Payroll_Tedis_Vietha.objects.filter(employee__in=list_employee_tedis_vietha,month=month)
        for payroll in payroll_tedis_vietha:
            trade_union_company_amount += round(payroll.trade_union_fee_company_pay)
        trade_union_company_amount += float(trade_union_fee_company_pay)
        payment_trade_union_company_info = Report_Payment_Payroll_Tedis_VietHa(id=trade_union_company.id,month=trade_union_company.month,
                                                                item=trade_union_company.item,description=trade_union_company.description,amount_vnd=trade_union_company_amount,amount_euro=trade_union_company.amount_euro,
                                                                paidby=trade_union_company.paidby,paidto=trade_union_company.paidto,account_no=trade_union_company.account_no)
        payment_trade_union_company_info.save()
        
        
        messages.success(request, 'SUCCESS: Payroll updated')
        return redirect('employee:payroll_ser_edit',pk=payroll_info.id)
        
        
        
    
    return render(request, 'employee/edit_payroll_ser.html', {
        'payroll_info' : payroll_info,
        
    })
    

def payment_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get payroll info
    payment_info = Report_Payment_Payroll_Tedis_VietHa.objects.get(pk=pk)
    
    # Update payroll info
    if request.POST.get('btnupdatepayment'):
        month = payment_info.month
        item = request.POST.get('item')
        description = request.POST.get('description')
        amount_vnd = request.POST.get('amount_vnd')
        amount_euro = request.POST.get('amount_euro')
        paidby = request.POST.get('paidby')
        paidto = request.POST.get('paidto')
        account_no = request.POST.get('account_no')
    
        # Update and save
        payment_update_info = Report_Payment_Payroll_Tedis_VietHa(id=payment_info.id,month=month,
                                                   item=item,description=description,amount_vnd=amount_vnd,
                                                   amount_euro=amount_euro,paidby=paidby,paidto=paidto,
                                                   account_no=account_no,
                                                   created_by=payment_info.created_by,created_at=payment_info.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        payment_update_info.save()
        messages.success(request, 'SUCCESS: Payment updated')
        return redirect('employee:payment_report_payroll_tedis_vietha_edit',pk=payment_info.id)
        
        
        
    
    return render(request, 'employee/edit_payment_report_payroll_tedis_vietha.html', {
        'payment_info' : payment_info,
        
    })


def new_staff_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get Report_new_staff_Tedis_VietHa info
    new_staff_info = Report_new_staff_Tedis_VietHa.objects.get(pk=pk)
    
    # Update payroll info
    if request.POST.get('btnupdateNewStaff'):
        remark = request.POST.get('remark')

        # Update and save
        new_staff_update_info = Report_new_staff_Tedis_VietHa(id=new_staff_info.id,month=new_staff_info.month,employee=new_staff_info.employee,
                                                   department=new_staff_info.department,joining_date=new_staff_info.joining_date,
                                                   gross_salary=new_staff_info.gross_salary,allowance=new_staff_info.allowance,
                                                   remark=remark,dependant_deduction=new_staff_info.dependant_deduction,
                                                   hospital_for_HI=new_staff_info.hospital_for_HI,account_no=new_staff_info.account_no,
                                                   bank_name=new_staff_info.bank_name,PIT_code=new_staff_info.PIT_code,
                                                   created_by=new_staff_info.created_by,created_at=new_staff_info.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        new_staff_update_info.save()
        messages.success(request, 'SUCCESS: Report updated!')
        return redirect('employee:new_staff_report_payroll_tedis_vietha_edit',pk=new_staff_info.id)
        
        
        
    
    return render(request, 'employee/edit_new_staff_report_payroll_tedis_vietha.html', {
        'new_staff_info' : new_staff_info, 
    })


def confirmed_after_probation_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get Report_confirmed_after_probation_Tedis_VietHa info
    confirmed_after_probation_info = Report_confirmed_after_probation_Tedis_VietHa.objects.get(pk=pk)
    
    # Update payroll info
    if request.POST.get('btnupdateConfirmedAfterProbation'):
        sign_LC_date = request.POST.get('sign_LC_date')
        allowance = request.POST.get('allowance')
        salary_after_probation = request.POST.get('salary_after_probation')

        # Update and save
        confirmed_after_probation_update_info = Report_confirmed_after_probation_Tedis_VietHa(id=confirmed_after_probation_info.id,month=confirmed_after_probation_info.month,employee=confirmed_after_probation_info.employee,
                                                   department=confirmed_after_probation_info.department,joining_date=confirmed_after_probation_info.joining_date,
                                                   sign_LC_date=sign_LC_date,allowance=allowance,salary_after_probation=salary_after_probation,
                                                   SI_book_no=confirmed_after_probation_info.SI_book_no,hospital_for_HI=confirmed_after_probation_info.hospital_for_HI,
                                                   created_by=confirmed_after_probation_info.created_by,created_at=confirmed_after_probation_info.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        confirmed_after_probation_update_info.save()
        messages.success(request, 'SUCCESS: Report updated!')
        return redirect('employee:confirmed_after_probation_report_payroll_tedis_vietha_edit',pk=confirmed_after_probation_info.id)
        
        
        
    
    return render(request, 'employee/edit_confirmed_after_probation_report_payroll_tedis_vietha.html', {
        'confirmed_after_probation_info' : confirmed_after_probation_info, 
    })


def resigned_staff_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get Report_resigned_staff_Tedis_VietHa info
    resigned_staff_info = Report_resigned_staff_Tedis_VietHa.objects.get(pk=pk)
    
    # Update payroll info
    if request.POST.get('btnupdateResignedStaff'):
        allowance = request.POST.get('allowance')
        unused_AL = request.POST.get('unused_AL')
        month_13_salary = request.POST.get('month_13_salary')
        severance_allowance = request.POST.get('severance_allowance')
        other_allowance = request.POST.get('other_allowance')
        incentive = request.POST.get('incentive')
        remark = request.POST.get('remark')

        # Update and save
        resigned_staff_update_info = Report_resigned_staff_Tedis_VietHa(id=resigned_staff_info.id,month=resigned_staff_info.month,employee=resigned_staff_info.employee,
                                                   department=resigned_staff_info.department,joining_date=resigned_staff_info.joining_date,leaving_date=resigned_staff_info.leaving_date,
                                                   allowance=allowance,unused_AL=unused_AL,
                                                   month_13_salary=month_13_salary,severance_allowance=severance_allowance,
                                                   other_allowance=other_allowance,incentive=incentive,
                                                   remark=remark,
                                                   created_by=resigned_staff_info.created_by,created_at=resigned_staff_info.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        resigned_staff_update_info.save()
        messages.success(request, 'SUCCESS: Report updated!')
        return redirect('employee:resigned_staff_report_payroll_tedis_vietha_edit',pk=resigned_staff_info.id)
        
        
        
    
    return render(request, 'employee/edit_resigned_staff_report_payroll_tedis_vietha.html', {
        'resigned_staff_info' : resigned_staff_info, 
    })
    

def other_changes_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get Report_other_changes_Tedis_VietHa info
    other_changes_info = Report_other_changes_Tedis_VietHa.objects.get(pk=pk)
    
    # Update payroll info
    if request.POST.get('btnupdateResignedStaff'):
        new_salary = request.POST.get('new_salary')
        allowance = request.POST.get('allowance')
        effective_date = request.POST.get('effective_date')
        remark = request.POST.get('remark')

        # Update and save
        other_changes_update_info = Report_other_changes_Tedis_VietHa(id=other_changes_info.id,month=other_changes_info.month,employee=other_changes_info.employee,
                                                   new_salary=new_salary,allowance=allowance,
                                                   effective_date=effective_date,remark=remark,
                                                   created_by=other_changes_info.created_by,created_at=other_changes_info.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        other_changes_update_info.save()
        messages.success(request, 'SUCCESS: Report updated!')
        return redirect('employee:other_changes_report_payroll_tedis_vietha_edit',pk=other_changes_info.id)
        
        
        
    
    return render(request, 'employee/edit_other_changes_report_payroll_tedis_vietha.html', {
        'other_changes_info' : other_changes_info, 
    })
    

def maternity_leave_report_payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get Report_maternity_leave_Tedis_VietHa info
    maternity_leave_info = Report_maternity_leave_Tedis_VietHa.objects.get(pk=pk)
    
    # Update payroll info
    if request.POST.get('btnupdateMaternityLeave'):
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        # Update and save
        maternity_leave_update_info = Report_maternity_leave_Tedis_VietHa(id=maternity_leave_info.id,month=maternity_leave_info.month,employee=maternity_leave_info.employee,department=maternity_leave_info.department,
                                                   from_date=from_date,to_date=to_date,
                                                   created_by=maternity_leave_info.created_by,created_at=maternity_leave_info.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        maternity_leave_update_info.save()
        messages.success(request, 'SUCCESS: Report updated!')
        return redirect('employee:maternity_leave_report_payroll_tedis_vietha_edit',pk=maternity_leave_info.id)
        
        
        
    
    return render(request, 'employee/edit_maternity_leave_report_payroll_tedis_vietha.html', {
        'maternity_leave_info' : maternity_leave_info, 
    })


def reconcile_report_payroll_tedis_vietha_edit(request, remark_id):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get reconcile_remark info
    reconcile_remark = Report_reconcile_Tedis_VietHa.objects.get(id=remark_id)
    if request.POST.get('btnupdateReconcile'):
        remark = request.POST.get('remark')
        reconcile_update_info = Report_reconcile_Tedis_VietHa(id=reconcile_remark.id,month=reconcile_remark.month,employee=reconcile_remark.employee,
                                                   remark=remark,
                                                   created_by=reconcile_remark.created_by,created_at=reconcile_remark.created_at,
                                                   updated_by=s_user[2],updated_at=datetime.now())
        reconcile_update_info.save()
        messages.success(request, 'SUCCESS: Report updated!')
        return redirect('employee:reconcile_report_payroll_tedis_vietha_edit',remark_id=reconcile_remark.id)
        
        
        
    
    return render(request, 'employee/edit_reconcile_report_payroll_tedis_vietha.html', {
        'reconcile_remark' : reconcile_remark, 
    })
    
# PDF
def pdf_time_sheets(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 1 or s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Get month
    period_month = Month_in_period.objects.get(pk=pk)
    
    if role == 3:
        list_employees = Employee.objects.all()
    else:
        list_staff = Employee_manager.objects.filter(manager=s_user[2])
        list_employee_id = []
        for staff in list_staff:
            list_employee_id.append(staff.employee.id)
        list_employees = Employee.objects.filter(id__in=list_employee_id)
    list_days_in_month = Daily_work.objects.filter(month=period_month)
    list_data = []
    for employee in list_employees:
        # Get daily work for employee
        list_employee_days = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_days_in_month)
        # Get Working day of BO and Working day of WH
        working_day_bo = period_month.total_work_days_bo
        working_day_wh = period_month.total_work_days_wh
            
        # Get total_salary_working_day 
        list_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, work__gt=0)
        total_working_day = 0
        for daily_work_info in list_daily_work_info:
            total_working_day += daily_work_info.work
        # Get leave
        list_paid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,work__gt=0, paid_leave__gt=0)
        total_paid_leave_day = 0
        for paid_leave_info in list_paid_leave_info:
            total_paid_leave_day += paid_leave_info.paid_leave
        
        list_unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,work__gt=0, unpaid_leave__gt=0)
        total_unpaid_leave_day = 0
        for unpaid_leave_info in list_unpaid_leave_info:
            total_unpaid_leave_day += unpaid_leave_info.unpaid_leave
        # Get OT hour to pay salary
        ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
        total_paid_hour = 0
        for application in ot_applications:
            total_paid_hour += application.ot_paid_hour
        # Make data    
        data = {
            'employee': employee,
            'total_paid_leave_days': total_paid_leave_day,
            'total_unpaid_leave_days': total_unpaid_leave_day,
            'total_salary_working_day': total_working_day - total_unpaid_leave_day,
            'total_ot_paid_hour': total_paid_hour,
            'list_employee_days' : list_employee_days,
             
        }
        list_data.append(data)
        
    
    html_string = render_to_string('employee/pdf_time_sheets.html', {
        'today': today,
        'period_month' : period_month,
        'list_data' : list_data,
        'list_days_in_month':list_days_in_month,
    })
    
    options = {
    'page-height': '900mm',
    'page-width':'500mm',
    'encoding': "UTF-8",
    'orientation': 'landscape',
}

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'timesheets_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config, options=options)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)


    return HttpResponse(html_string)
    
    
    
    
def report_leave(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')

    s_user = request.session.get('s_user')
    role = s_user[1]
    if s_user[1] == 1 or s_user[1] == 3:
        pass
    else:
        messages.error(request, 'Access Denied')
        return redirect('hr:index')
    
    # Lấy Employee_id
    s_user = request.session.get('s_user')
    employee_pk = s_user[2]
    role = s_user[1]
    
    # Redirect to present period
    default_period = Period.objects.get(period_year=today.year)

    
    # Previous and next period button
    if request.POST.get('btn_previousperiod'):
        try:
            previous_period = Period.objects.get(period_year=default_period.period_year-1)
            return redirect('employee:report_leave',pk=previous_period.id)
        except Period.DoesNotExist:
            messages.error(request, 'Period does not exist.')
    
    if request.POST.get('btn_nextperiod'):
        try:
            previous_period = Period.objects.get(period_year=default_period.period_year+1)
            return redirect('employee:report_leave',pk=previous_period.id)
        except Period.DoesNotExist:
            messages.error(request, 'Period does not exist.')
    
    # Data
    if role == 1:
        list_staff = Employee_manager.objects.filter(manager=employee_pk)
        list_employee_id = []
        for staff in list_staff:
            list_employee_id.append(staff.employee.id)
        list_employees = Employee.objects.filter(id__in=list_employee_id)
        list_data = []
        for employee in list_employees:
            # Get total, used and leave balance
            dayoff_info = Dayoff.objects.get(employee=employee,period=default_period)
            # Get total recuperation
            ot_applications = Overtime_application.objects.filter(employee=employee, application_date__year=default_period.period_year,ot_unpaid_day__gt=0)
            total_recuperation = 0
            for ot_application in ot_applications:
                total_recuperation += ot_application.ot_unpaid_day
            # Used recuperation
            leave_applications = Leave_application.objects.filter(employee=employee,application_date__year=default_period.period_year,offinlieu_number_of_leave_days__gt=0)
            used_recuperation = 0
            for leave_application in leave_applications:
                used_recuperation += float(leave_application.offinlieu_number_of_leave_days)
            # Recuperation balance 
            recuperation_balance = total_recuperation - used_recuperation
            # Make data    
            data = {
                'employee': employee,
                'dayoff': dayoff_info,
                'total_recuperation': total_recuperation,
                'used_recuperation': used_recuperation,
                'recuperation_balance': recuperation_balance,
        
            }
            list_data.append(data)
            
    if role == 3:
        list_employees = Employee.objects.all()
        list_data = []
        for employee in list_employees:
            # Get total, used and leave balance
            try:
                dayoff_info = Dayoff.objects.get(employee=employee,period=default_period)
            except Dayoff.DoesNotExist:
                dayoff_info = ''
            # Get total recuperation
            ot_applications = Overtime_application.objects.filter(employee=employee, application_date__year=default_period.period_year,ot_unpaid_day__gt=0)
            total_recuperation = 0
            for ot_application in ot_applications:
                total_recuperation += ot_application.ot_unpaid_day
            # Used recuperation
            leave_applications = Leave_application.objects.filter(employee=employee,application_date__year=default_period.period_year,offinlieu_number_of_leave_days__gt=0)
            used_recuperation = 0
            for leave_application in leave_applications:
                used_recuperation += float(leave_application.offinlieu_number_of_leave_days)
            # Recuperation balance 
            recuperation_balance = total_recuperation - used_recuperation
            # Make data    
            data = {
                'employee': employee,
                'dayoff': dayoff_info,
                'total_recuperation': total_recuperation,
                'used_recuperation': used_recuperation,
                'recuperation_balance': recuperation_balance,
        
            }
            list_data.append(data)
        
    if request.POST.get('get_report'):   
        file_name = str(default_period.period_year) + '_leave_report.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 640, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'pale_blue')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Leave & OT')
        
        # Set col width
        for col in range(0,10):
            ws.col(col).width = 5000

        # Table
        # Top
        ws.write_merge(0, 0, 0, 6, 'Leave & OT Report', style_head)
        ws.write(0, 9, str(default_period.period_year),style_head)
        
        # Body
        # Body head
        ws.write(2, 0, 'Employee code', style_table_head)
        ws.write(2, 1, 'Full name', style_table_head)
        ws.write(2, 2, 'Department', style_table_head)
        ws.write(2, 3, 'Joining date', style_table_head)
        ws.write(2, 4, 'Total leave', style_table_head)
        ws.write(2, 5, 'Used leave', style_table_head)
        ws.write(2, 6, 'Leave balance', style_table_head)
        ws.write(2, 7, 'Total recuperation', style_table_head)
        ws.write(2, 8, 'Used recuperation', style_table_head)
        ws.write(2, 9, 'Recuperation balance', style_table_head)
        for index, data in enumerate(list_data):
            ws.write(3+index, 0, str(data['employee'].employee_code),style_normal)
            ws.write(3+index, 1, str(data['employee'].full_name),style_normal)
            ws.write(3+index, 2, str(data['employee'].department_e),style_normal)
            ws.write(3+index, 3, str(data['employee'].joining_date),style_normal)
            ws.write(3+index, 4, str(data['dayoff'].total_dayoff),style_normal)
            ws.write(3+index, 5, str(data['dayoff'].used_dayoff),style_normal)
            ws.write(3+index, 6, str(data['dayoff'].remain_dayoff),style_normal)
            ws.write(3+index, 7, str(data['total_recuperation']),style_normal)
            ws.write(3+index, 8, str(data['used_recuperation']),style_normal)
            ws.write(3+index, 9, str(data['recuperation_balance']),style_normal)
        
        wb.save(response)
        return response    
    
    return render(request, 'employee/report_leave.html', {
        'default_period' : default_period,
        'list_data' : list_data,
    })




#TEST





    

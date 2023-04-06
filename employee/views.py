from asyncio.windows_events import NULL
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from django.db.models import Q
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
from io import StringIO
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


def add_staff_for_manager(request,pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get user
    s_user = request.session.get('s_user')
    role = s_user[1]
    
    # Get employee
    employee = Employee.objects.get(id = pk)
    
    # Get employee list
    list_employee = Employee.objects.all()
    
    # Form
    
    if request.POST.get('btn_addmanager'):
        manager_name = request.POST.get('employee_id') # lấy từ <input type="hidden">
        manager = Employee.objects.only('id').get(id=manager_name)
        employee_manager_info = Employee_manager(employee=employee, manager=manager)
        employee_manager_info.save()
        messages.success(request, 'Staff added')
        return redirect('/employee/')
    
    
    return render(request, 'employee/form_add_staff.html', {
        'employee' : employee,
        'list_employee' : list_employee,
        
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

def add_contract(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee & list of contract type:
    employee = Employee.objects.get(pk=pk)
    employee_site = employee.site
    list_contract_type = Contract_type.objects.all()
    
    # Create contract
    if request.POST.get('btn_addcontract'):
        employee_id = Employee.objects.only('id').get(id=pk)
        contract_no = request.POST.get('contract_no')
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
        contract_info = Employee_contract(employee=employee_id, contract_no=contract_no, contract_type=contract_type,signed_contract_date=signed_contract_date,from_date=from_date,to_date=to_date,basic_salary=basic_salary,responsibility_allowance=responsibility_allowance,lunch_support=lunch_support,transportation_support=transportation_support,telephone_support=telephone_support,seniority_bonus=seniority_bonus,travel_support=travel_support)                 
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
                                 total_dayoff=total_dayoff,remain_dayoff=total_dayoff,previous_remain_dayoff=previous_remain_dayoff,previous_remain_recuperation=previous_remain_recuperation,
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
        list_employee = Employee.objects.all()
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
        total_work_days = request.POST.get('total_work_days')
        month_info = Month_in_period(period=period,month_name=month_name,month_number=month_number,
                                     total_days=total_days,holidays=holidays,total_work_days=total_work_days)  
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
        list_employee = Employee.objects.all()
        list_daily_work = Daily_work.objects.filter(month=month)
        for employee in list_employee:
            for daily_work in list_daily_work:
                daily_work_info_for_employee = Daily_work_for_employee(employee=employee,daily_work=daily_work)
                daily_work_info_for_employee.save()
        # Add 1/2 OT day for Warehouse employees
        list_daily_work = Daily_work.objects.filter(month=38)
        list_warehouse_employees = Employee.objects.filter(department_e=6)
        for warehouse_employee in list_warehouse_employees:
            list_warehouse_employee_daily_work = Daily_work_for_employee.objects.filter(employee=warehouse_employee,daily_work__in=list_daily_work)
            for daily_work_warehouse_employee in list_warehouse_employee_daily_work:
                if daily_work_warehouse_employee.daily_work.date.weekday() == 5:
                    daily_work_warehouse_employee.ot_time = 0.5
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
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    list_data = []
    for employee in list_employees:
        daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
        paid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, paid_leave__gt=0)
        unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
        # Get OT hour to pay salary
        ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
        total_paid_hour = 0
        for application in ot_applications:
            total_paid_hour += application.ot_paid_hour
        # Make data    
        data = {
            'employee': employee,
            'total_paid_leave_days': paid_leave_info.count(),
            'total_unpaid_leave_days': unpaid_leave_info.count(),
            'total_salary_working_day': daily_work_info.count() - unpaid_leave_info.count(),
            'total_ot_paid_hour': total_paid_hour,
             
        }
        list_data.append(data)
        total_working_day = daily_work_info.count()
        
    # Add month to current PERIOD
    list_employee_days = None
    employee_full_name = None
    if request.POST.get('get_timesheet'):   
        file_name = str(period_month.month_name) + '_timesheets.xls'
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        # Style
        style_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 640, colour black;' % 'white')
        style_table_head = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold 1,height 220, colour black;' % 'white')
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'white')
        # Style for day
        # Weekend
        style_weekend = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'pale_blue')
        # Holiday
        style_holiday = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'lavender')
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
                    if day.ot_time == 0.5:
                        ws.write(3+row, 7+index, str('1/2OT'),style_weekend)
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
                else:
                    ws.write(3+row, 7+index, str('X'),style_normal)
            row += 1   


        wb.save(response)
        return response  
    
    return render(request, 'employee/time_sheets_list.html', {
        'role' : role,
        'period_month' : period_month,
        'list_data' : list_data,
        'employee_full_name' : employee_full_name,
        'list_employee_days' : list_employee_days,
        'total_working_day' : total_working_day,
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
    
    
    # Get payroll data
    site_RO = Site.objects.get(site='RO')
    list_employee_tedis = Employee.objects.filter(site=site_RO)
    # Get total_working_days
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    daily_work_info = Daily_work_for_employee.objects.filter(employee=list_employee_tedis[0], daily_work__in=list_work_days)
    total_working_day = daily_work_info.count()
    # Create payroll dict
    list_payroll_info = []
    for employee in list_employee_tedis:
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
            list_payroll_info.append(data)
        except Payroll_Tedis.DoesNotExist:
            payrollExist = 0
        
    # Create payroll data
    if request.POST.get('btn_adjust_percent'):
        # Get % Adjust  
        adjust_percent = float(request.POST.get('adjust_percent'))
        
        site_RO = Site.objects.get(site='RO')
        list_employee_tedis = Employee.objects.filter(site=site_RO)
        for employee in list_employee_tedis:
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT:
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT:
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
            # Get occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
            occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = 0
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
            contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus :
                    sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
                    taxable_income = sum_K_AA - lunch - severance_allowance + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
                else:
                    taxable_income = sum_K_AA - severance_allowance + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
            else:
                taxable_income = 0
            # Get taxed_income
            if taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction < 0:
                taxed_income = 0
            else:
                taxed_income = taxable_income - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - family_deduction
            # Get PIT
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus :
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
            net_income = sum_K_AA + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - PIT - deduct
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            sum_K_AA = gross_income + salary_recuperation + overtime + transportation + phone + lunch + training_fee + toxic_allowance + travel + responsibility + seniority_bonus + other + total_allowance_recuperation + benefits + severance_allowance + outstanding_annual_leave + month_13_salary_Pro_ata
            total_cost = round((sum_K_AA + SHUI_21point5percent_company_pay + recuperation_of_SHU_Ins_21point5percent_company_pay + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs + trade_union_fee_company_pay_2percent + trade_union_fee_member + transfer_bank - deduct),1)
            

    
            
            payroll_employee_info = Payroll_Tedis(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,
                                                  gross_income=gross_income,salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch, training_fee=training_fee, toxic_allowance=toxic_allowance, travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                  other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata, 
                                                  recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs=occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs,
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
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'pale_blue')
        style_table_head.alignment.wrap = 1
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black; align: horiz center, vert center' % 'white')
        style_normal.alignment.wrap = 1

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Payroll Tedis')

        # Table
        
        # Set col width
        for col in range(0,41):
            ws.col(col).width = 5000
        

        
        # Top
        ws.write_merge(0, 0, 0, 6, 'TEDIS REP. OFFICE IN HO CHI MINH', style_head)
        ws.write(1, 0, 'Room 2B, Floor 2 & 4 - 150 Nguyen Luong Bang, Tan Phu Ward, District 7', style_head_small)
        ws.write_merge(0, 0, 9, 11, 'PAYROLL IN ' + str(period_month.month_name),style_head)
        
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
        ws.write(2, 6, 'Salary ' + str(period_month.period.period_year) + ' (VND)', style_table_head)
        ws.write(2, 7, 'Working days', style_table_head)
        ws.write(2, 8, '% Adjust', style_table_head)
        ws.write(2, 9, 'Gross Income', style_table_head)
        ws.write(2, 10, 'Salary recuperation', style_table_head)
        ws.write(2, 11, 'Overtime', style_table_head)
        ws.write(2, 12, 'Transportation', style_table_head)
        ws.write(2, 13, 'Phone', style_table_head)
        ws.write(2, 14, 'Lunch', style_table_head)
        ws.write(2, 15, 'Training fee', style_table_head)
        ws.write(2, 16, 'Toxic Allowance', style_table_head)
        ws.write(2, 17, 'Travel', style_table_head)
        ws.write(2, 18, 'Responsibility', style_table_head)
        ws.write(2, 19, 'Seniority Bonus', style_table_head)
        ws.write(2, 20, 'Other', style_table_head)
        ws.write(2, 21, 'Total allowance recuperation', style_table_head)
        ws.write(2, 22, 'Benefits', style_table_head)
        ws.write(2, 23, 'Severance Allowance', style_table_head)
        ws.write(2, 24, 'Outstanding annual leave', style_table_head)
        ws.write(2, 25, '13th salary (pro-rata)', style_table_head)
        ws.write(2, 26, 'SHUI(10.5%)(Employee pay)', style_table_head)
        ws.write(2, 27, 'Recuperation of SHU Ins.(10.5%)(staff pay)', style_table_head)
        ws.write(2, 28, 'SHUI(21.5%)(Company pay)', style_table_head)
        ws.write(2, 29, 'Recuperation of SHU Ins.(21.5%)(Company pay)', style_table_head)
        ws.write(2, 30, 'Occupational accident and disease Ins.(0.5%)(Pay for staffs)', style_table_head)
        ws.write(2, 31, 'Trade Union fee (Company pay 2%)', style_table_head)
        ws.write(2, 32, 'Trade Union fee (Employee pay)', style_table_head)
        ws.write(2, 33, 'Family deduction', style_table_head)
        ws.write(2, 34, 'Taxable Income', style_table_head)
        ws.write(2, 35, 'Taxed Income', style_table_head)
        ws.write(2, 36, 'PIT', style_table_head)
        ws.write(2, 37, 'Deduct', style_table_head)
        ws.write(2, 38, 'Net Income', style_table_head)
        ws.write(2, 39, 'Transfer Bank', style_table_head)
        ws.write(2, 40, 'Total Cost', style_table_head)
        
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
        ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = 0
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
            ws.write(3+index, 6, str("{:,}".format(data['payroll_info'].newest_salary)),style_normal)
            ws.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws.write(3+index, 8, str(data['payroll_info'].adjust_percent) + '%',style_normal)
            ws.write(3+index, 9, str("{:,}".format(data['payroll_info'].gross_income)),style_normal)
            ws.write(3+index, 10, str("{:,}".format(data['payroll_info'].salary_recuperation)),style_normal)
            ws.write(3+index, 11, str("{:,}".format(data['payroll_info'].overtime)),style_normal)
            ws.write(3+index, 12, str("{:,}".format(data['payroll_info'].transportation)),style_normal)
            ws.write(3+index, 13, str("{:,}".format(data['payroll_info'].phone)),style_normal)
            ws.write(3+index, 14, str("{:,}".format(data['payroll_info'].lunch)),style_normal)
            ws.write(3+index, 15, str("{:,}".format(data['payroll_info'].training_fee)),style_normal)
            ws.write(3+index, 16, str("{:,}".format(data['payroll_info'].toxic_allowance)),style_normal)
            ws.write(3+index, 17, str("{:,}".format(data['payroll_info'].travel)),style_normal)
            ws.write(3+index, 18, str("{:,}".format(data['payroll_info'].responsibility)),style_normal)
            ws.write(3+index, 19, str("{:,}".format(data['payroll_info'].seniority_bonus)),style_normal)
            ws.write(3+index, 20, str("{:,}".format(data['payroll_info'].other)),style_normal)
            ws.write(3+index, 21, str("{:,}".format(data['payroll_info'].total_allowance_recuperation)),style_normal)
            ws.write(3+index, 22, str("{:,}".format(data['payroll_info'].benefits)),style_normal)
            ws.write(3+index, 23, str("{:,}".format(data['payroll_info'].severance_allowance)),style_normal)
            ws.write(3+index, 24, str("{:,}".format(data['payroll_info'].outstanding_annual_leave)),style_normal)
            ws.write(3+index, 25, str("{:,}".format(data['payroll_info'].month_13_salary_Pro_ata)),style_normal)
            ws.write(3+index, 26, str("{:,}".format(data['payroll_info'].SHUI_10point5percent_employee_pay)),style_normal)
            ws.write(3+index, 27, str("{:,}".format(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay)),style_normal)
            ws.write(3+index, 28, str("{:,}".format(data['payroll_info'].SHUI_21point5percent_company_pay)),style_normal)
            ws.write(3+index, 29, str("{:,}".format(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay)),style_normal)
            ws.write(3+index, 30, str("{:,}".format(data['payroll_info'].occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)),style_normal)
            ws.write(3+index, 31, str("{:,}".format(data['payroll_info'].trade_union_fee_company_pay_2percent)),style_normal)
            ws.write(3+index, 32, str("{:,}".format(data['payroll_info'].trade_union_fee_member)),style_normal)
            ws.write(3+index, 33, str("{:,}".format(data['payroll_info'].family_deduction)),style_normal)
            ws.write(3+index, 34, str("{:,}".format(data['payroll_info'].taxable_income)),style_normal)
            ws.write(3+index, 35, str("{:,}".format(data['payroll_info'].taxed_income)),style_normal)
            ws.write(3+index, 36, str("{:,}".format(data['payroll_info'].PIT)),style_normal)
            ws.write(3+index, 37, str("{:,}".format(data['payroll_info'].deduct)),style_normal)
            ws.write(3+index, 38, str("{:,}".format(data['payroll_info'].net_income)),style_normal)
            ws.write(3+index, 39, str("{:,}".format(data['payroll_info'].transfer_bank)),style_normal)
            ws.write(3+index, 40, str("{:,}".format(data['payroll_info'].total_cost)),style_normal)
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
            ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs += data['payroll_info'].occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
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
        ws.write(last_row, 15, str("{:,}".format(tttraining_fee)),style_table_head)
        ws.write(last_row, 16, str("{:,}".format(tttoxic_allowance)),style_table_head)
        ws.write(last_row, 17, str("{:,}".format(tttravel)),style_table_head)
        ws.write(last_row, 18, str("{:,}".format(ttresponsibility)),style_table_head)
        ws.write(last_row, 19, str("{:,}".format(ttseniority_bonus)),style_table_head)
        ws.write(last_row, 20, str("{:,}".format(ttother)),style_table_head)
        ws.write(last_row, 21, str("{:,}".format(tttotal_allowance_recuperation)),style_table_head)
        ws.write(last_row, 22, str("{:,}".format(ttbenefits)),style_table_head)
        ws.write(last_row, 23, str("{:,}".format(ttseverance_allowance)),style_table_head)
        ws.write(last_row, 24, str("{:,}".format(ttoutstanding_annual_leave)),style_table_head)
        ws.write(last_row, 25, str("{:,}".format(ttmonth_13_salary_Pro_ata)),style_table_head)
        ws.write(last_row, 26, str("{:,}".format(ttSHUI_10point5percent_employee_pay)),style_table_head)
        ws.write(last_row, 27, str("{:,}".format(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay)),style_table_head)
        ws.write(last_row, 28, str("{:,}".format(ttSHUI_21point5percent_company_pay)),style_table_head)
        ws.write(last_row, 29, str("{:,}".format(ttrecuperation_of_SHU_Ins_21point5percent_company_pay)),style_table_head)
        ws.write(last_row, 30, str("{:,}".format(ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)),style_table_head)
        ws.write(last_row, 31, str("{:,}".format(tttrade_union_fee_company_pay_2percent)),style_table_head)
        ws.write(last_row, 32, str("{:,}".format(tttrade_union_fee_member)),style_table_head)
        ws.write(last_row, 33, str("{:,}".format(ttfamily_deduction)),style_table_head)
        ws.write(last_row, 34, str("{:,}".format(tttaxable_income)),style_table_head)
        ws.write(last_row, 35, str("{:,}".format(tttaxed_income)),style_table_head)
        ws.write(last_row, 36, str("{:,}".format(ttPIT)),style_table_head)
        ws.write(last_row, 37, str("{:,}".format(ttdeduct)),style_table_head)
        ws.write(last_row, 38, str("{:,}".format(ttnet_income)),style_table_head)
        ws.write(last_row, 39, str("{:,}".format(tttransfer_bank)),style_table_head)
        ws.write(last_row, 40, str("{:,}".format(tttotal_cost)),style_table_head)
         


        wb.save(response)
        return response

  
    
    return render(request, 'employee/view_payroll_tedis.html', {
        'period_month' : period_month,
        'payrollExist': payrollExist,
        'list_payroll_info' : list_payroll_info,
        'total_working_day' : total_working_day,
    })


def payroll_tedis_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get payroll info
    payroll_info = Payroll_Tedis.objects.get(pk=pk)
    
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')
        list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT:
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT:
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
        # Get recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
        recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
        occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = request.POST.get('occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs')
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
        contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus :
                sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
                taxable_income = sum_K_AA - float(lunch) - float(severance_allowance) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)
            else:
                taxable_income = sum_K_AA - float(severance_allowance) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)
        else:
            taxable_income = 0
        # Get taxed_income
        if taxable_income - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction) < 0:
            taxed_income = 0
        else:
            taxed_income = float(taxable_income) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(family_deduction)
        # Get PIT
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus :
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
        net_income = sum_K_AA + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(PIT) - float(deduct)
        # Get transfer_bank
        transfer_bank = request.POST.get('transfer_bank')
        # Get total_cost
        sum_K_AA = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(training_fee) + float(toxic_allowance) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(total_allowance_recuperation) + float(benefits) + float(severance_allowance) + float(outstanding_annual_leave) + float(month_13_salary_Pro_ata)
        total_cost = round((sum_K_AA + float(SHUI_21point5percent_company_pay) + float(recuperation_of_SHU_Ins_21point5percent_company_pay) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) + float(trade_union_fee_company_pay_2percent) + float(trade_union_fee_member) + float(transfer_bank) - float(deduct)),0)
        # Update and save
        payroll_update_info = Payroll_Tedis(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                            salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,training_fee=training_fee,toxic_allowance=toxic_allowance,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                            other=other,total_allowance_recuperation=total_allowance_recuperation,benefits=benefits,severance_allowance=severance_allowance,outstanding_annual_leave=outstanding_annual_leave,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                            SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                            occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs=occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs,
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
    list_employee_tedis_vietha = Employee.objects.filter(site=site_JV)
    # Get total_working_days
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    daily_work_info = Daily_work_for_employee.objects.filter(employee=list_employee_tedis_vietha[0], daily_work__in=list_work_days)
    total_working_day = daily_work_info.count()
    # Create payroll dict
    list_payroll_info = []
    for employee in list_employee_tedis_vietha:
        try:
            payroll_info = Payroll_Tedis_Vietha.objects.get(employee=employee,month=period_month)
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
            list_payroll_info.append(data)
        except Payroll_Tedis_Vietha.DoesNotExist:
            payrollExist = 0
        
    # Create payroll data
    if request.POST.get('btn_adjust_percent'):
        # Get % Adjust  
        adjust_percent = float(request.POST.get('adjust_percent'))
        
        site_JV = Site.objects.get(site='JV')
        list_employee_tedis = Employee.objects.filter(site=site_JV)
        for employee in list_employee_tedis:
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT and working_days >= 10:
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')
            contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT and working_days >= 10:
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
                elif list_contracts[0].contract_type == contract_type_CTminus and working_days >= 10:
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
            # Get occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
            occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = 0
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')
            contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
            contract_type_CTminusHUU = Contract_type.objects.get(contract_type='CT-HUU')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus or list_contracts[0].contract_type == contract_type_CTminusHUU:
                    sum_K_Y = gross_income + transportation + phone + lunch + travel + responsibility + seniority_bonus + other + outstanding_annual_leave + OTC_incentive + KPI_achievement + month_13_salary_Pro_ata + incentive_last_month + incentive_last_quy_last_year + taxable_overtime
                    taxable_income = sum_K_Y + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs - lunch
                else:
                    sum_K_Z = gross_income + transportation + phone + lunch + travel + responsibility + seniority_bonus + other + outstanding_annual_leave + OTC_incentive + KPI_achievement + month_13_salary_Pro_ata + incentive_last_month + incentive_last_quy_last_year + taxable_overtime + nontaxable_overtime
                    taxable_income = sum_K_Z + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
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
                if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus or list_contracts[0].contract_type == contract_type_CTminusHUU :
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
            net_income = sum_K_Z + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs - SHUI_10point5percent_employee_pay - recuperation_of_SHU_Ins_10point5percent_staff_pay - PIT_balance - first_payment
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            total_cost = round(sum_K_Z + SHUI_21point5percent_company_pay + recuperation_of_SHU_Ins_21point5percent_company_pay + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs + trade_union_fee_company_pay + trade_union_fee_employee_pay + transfer_bank)
            
            payroll_employee_info = Payroll_Tedis_Vietha(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,
                                                  gross_income=gross_income,transportation=transportation,phone=phone,lunch=lunch,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                                  other=other,outstanding_annual_leave=outstanding_annual_leave,OTC_incentive=OTC_incentive,KPI_achievement=KPI_achievement,month_13_salary_Pro_ata=month_13_salary_Pro_ata,incentive_last_month=incentive_last_month,incentive_last_quy_last_year=incentive_last_quy_last_year,taxable_overtime=taxable_overtime,nontaxable_overtime=nontaxable_overtime,
                                                  SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                                  occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs=occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs,
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
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'pale_blue')
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
        ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = 0
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
            ws.write(3+index, 6, str("{:,}".format(data['payroll_info'].newest_salary)),style_normal)
            ws.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws.write(3+index, 8, str(data['payroll_info'].adjust_percent) + '%',style_normal)
            ws.write(3+index, 9, str("{:,}".format(data['payroll_info'].gross_income)),style_normal)
            ws.write(3+index, 10, str("{:,}".format(data['payroll_info'].transportation)),style_normal)
            ws.write(3+index, 11, str("{:,}".format(data['payroll_info'].phone)),style_normal)
            ws.write(3+index, 12, str("{:,}".format(data['payroll_info'].lunch)),style_normal)
            ws.write(3+index, 13, str("{:,}".format(data['payroll_info'].travel)),style_normal)
            ws.write(3+index, 14, str("{:,}".format(data['payroll_info'].responsibility)),style_normal)
            ws.write(3+index, 15, str("{:,}".format(data['payroll_info'].seniority_bonus)),style_normal)
            ws.write(3+index, 16, str("{:,}".format(data['payroll_info'].other)),style_normal)
            ws.write(3+index, 17, str("{:,}".format(data['payroll_info'].outstanding_annual_leave)),style_normal)
            ws.write(3+index, 18, str("{:,}".format(data['payroll_info'].OTC_incentive)),style_normal)
            ws.write(3+index, 19, str("{:,}".format(data['payroll_info'].KPI_achievement)),style_normal)
            ws.write(3+index, 20, str("{:,}".format(data['payroll_info'].month_13_salary_Pro_ata)),style_normal)
            ws.write(3+index, 21, str("{:,}".format(data['payroll_info'].incentive_last_month)),style_normal)
            ws.write(3+index, 22, str("{:,}".format(data['payroll_info'].incentive_last_quy_last_year)),style_normal)
            ws.write(3+index, 23, str("{:,}".format(data['payroll_info'].taxable_overtime)),style_normal)
            ws.write(3+index, 24, str("{:,}".format(data['payroll_info'].nontaxable_overtime)),style_normal)
            ws.write(3+index, 25, str("{:,}".format(data['payroll_info'].SHUI_10point5percent_employee_pay)),style_normal)
            ws.write(3+index, 26, str("{:,}".format(data['payroll_info'].recuperation_of_SHU_Ins_10point5percent_staff_pay)),style_normal)
            ws.write(3+index, 27, str("{:,}".format(data['payroll_info'].SHUI_21point5percent_company_pay)),style_normal)
            ws.write(3+index, 28, str("{:,}".format(data['payroll_info'].recuperation_of_SHU_Ins_21point5percent_company_pay)),style_normal)
            ws.write(3+index, 29, str("{:,}".format(data['payroll_info'].occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)),style_normal)
            ws.write(3+index, 30, str("{:,}".format(data['payroll_info'].trade_union_fee_company_pay)),style_normal)
            ws.write(3+index, 31, str("{:,}".format(data['payroll_info'].trade_union_fee_employee_pay)),style_normal)
            ws.write(3+index, 32, str("{:,}".format(data['payroll_info'].family_deduction)),style_normal)
            ws.write(3+index, 33, str("{:,}".format(data['payroll_info'].taxable_income)),style_normal)
            ws.write(3+index, 34, str("{:,}".format(data['payroll_info'].taxed_income)),style_normal)
            ws.write(3+index, 35, str("{:,}".format(data['payroll_info'].PIT_13th_salary)),style_normal)
            ws.write(3+index, 36, str("{:,}".format(data['payroll_info'].PIT)),style_normal)
            ws.write(3+index, 37, str("{:,}".format(data['payroll_info'].PIT_balance)),style_normal)
            ws.write(3+index, 38, str("{:,}".format(data['payroll_info'].first_payment)),style_normal)
            ws.write(3+index, 39, str("{:,}".format(data['payroll_info'].net_income)),style_normal)
            ws.write(3+index, 40, str("{:,}".format(data['payroll_info'].transfer_bank)),style_normal)
            ws.write(3+index, 41, str("{:,}".format(data['payroll_info'].total_cost)),style_normal)
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
            ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs += data['payroll_info'].occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
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
        ws.write(last_row, 6, str("{:,}".format(ttnewest_salary)),style_table_head)
        ws.write(last_row, 7, '-',style_table_head)
        ws.write(last_row, 8, '-',style_table_head)
        ws.write(last_row, 9, str("{:,}".format(ttgross_income)),style_table_head)
        ws.write(last_row, 10, str("{:,}".format(tttransportation)),style_table_head)
        ws.write(last_row, 11, str("{:,}".format(ttphone)),style_table_head)
        ws.write(last_row, 12, str("{:,}".format(ttlunch)),style_table_head)
        ws.write(last_row, 13, str("{:,}".format(tttravel)),style_table_head)
        ws.write(last_row, 14, str("{:,}".format(ttresponsibility)),style_table_head)
        ws.write(last_row, 15, str("{:,}".format(ttseniority_bonus)),style_table_head)
        ws.write(last_row, 16, str("{:,}".format(ttother)),style_table_head)
        ws.write(last_row, 17, str("{:,}".format(ttoutstanding_annual_leave)),style_table_head)
        ws.write(last_row, 18, str("{:,}".format(ttOTC_incentive)),style_table_head)
        ws.write(last_row, 19, str("{:,}".format(ttKPI_achievement)),style_table_head)
        ws.write(last_row, 20, str("{:,}".format(ttmonth_13_salary_Pro_ata)),style_table_head)
        ws.write(last_row, 21, str("{:,}".format(ttincentive_last_month)),style_table_head)
        ws.write(last_row, 22, str("{:,}".format(ttincentive_last_quy_last_year)),style_table_head)
        ws.write(last_row, 23, str("{:,}".format(tttaxable_overtime)),style_table_head)
        ws.write(last_row, 24, str("{:,}".format(ttnontaxable_overtime)),style_table_head)
        ws.write(last_row, 25, str("{:,}".format(ttSHUI_10point5percent_employee_pay)),style_table_head)
        ws.write(last_row, 26, str("{:,}".format(ttrecuperation_of_SHU_Ins_10point5percent_staff_pay)),style_table_head)
        ws.write(last_row, 27, str("{:,}".format(ttSHUI_21point5percent_company_pay)),style_table_head)
        ws.write(last_row, 28, str("{:,}".format(ttrecuperation_of_SHU_Ins_21point5percent_company_pay)),style_table_head)
        ws.write(last_row, 29, str("{:,}".format(ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)),style_table_head)
        ws.write(last_row, 30, str("{:,}".format(tttrade_union_fee_company_pay)),style_table_head)
        ws.write(last_row, 31, str("{:,}".format(tttrade_union_fee_employee_pay)),style_table_head)
        ws.write(last_row, 32, str("{:,}".format(ttfamily_deduction)),style_table_head)
        ws.write(last_row, 33, str("{:,}".format(tttaxable_income)),style_table_head)
        ws.write(last_row, 34, str("{:,}".format(tttaxed_income)),style_table_head)
        ws.write(last_row, 35, str("{:,}".format(ttPIT_13th_salary)),style_table_head)
        ws.write(last_row, 36, str("{:,}".format(ttPIT)),style_table_head)
        ws.write(last_row, 37, str("{:,}".format(ttPIT_balance)),style_table_head)
        ws.write(last_row, 38, str("{:,}".format(ttfirst_payment)),style_table_head)
        ws.write(last_row, 39, str("{:,}".format(ttnet_income)),style_table_head)
        ws.write(last_row, 40, str("{:,}".format(tttransfer_bank)),style_table_head)
        ws.write(last_row, 41, str("{:,}".format(tttotal_cost)),style_table_head)
         


        wb.save(response)
        return response

  
    
    return render(request, 'employee/view_payroll_tedisvietha.html', {
        'period_month' : period_month,
        'payrollExist': payrollExist,
        'list_payroll_info' : list_payroll_info,
        'total_working_day' : total_working_day,
    })


def payroll_tedis_vietha_edit(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get payroll info
    payroll_info = Payroll_Tedis_Vietha.objects.get(pk=pk)
    
    # Get month total working days
    list_work_days = Daily_work.objects.filter(month=payroll_info.month,weekend=False,holiday=False)
    month_total_working_days = list_work_days.count()
    
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')
        list_contracts = Employee_contract.objects.filter(employee=employee).order_by('-created_at')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT and working_days >= 10:
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')
        contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT and working_days >= 10:
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
            elif list_contracts[0].contract_type == contract_type_CTminus and working_days >= 10:
                combo = newest_salary + responsibility/float(adjust_percent/100) + seniority_bonus/float(adjust_percent/100)
                if combo > 29800000:
                    SHUI_21point5percent_company_pay = 29800000 * 0.005
                else:
                    SHUI_21point5percent_company_pay = combo * 0.005      
            else:
                SHUI_21point5percent_company_pay = 0    
        else:
            SHUI_21point5percent_company_pay = 0
        # Get recuperation_of_SHU_Ins_21point5percent_company_pay,occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
        recuperation_of_SHU_Ins_21point5percent_company_pay = request.POST.get('recuperation_of_SHU_Ins_21point5percent_company_pay')
        occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = request.POST.get('occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs')
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')
        contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
        contract_type_CTminusHUU = Contract_type.objects.get(contract_type='CT-HUU')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus or list_contracts[0].contract_type == contract_type_CTminusHUU:
                sum_K_Y = float(gross_income) + float(transportation) + float(phone) + float(lunch) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(outstanding_annual_leave) + float(OTC_incentive) + float(KPI_achievement) + float(month_13_salary_Pro_ata) + float(incentive_last_month) + float(incentive_last_quy_last_year) + float(taxable_overtime)
                taxable_income = float(sum_K_Y) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) - float(lunch)
            else:
                sum_K_Z = float(gross_income) + float(transportation) + float(phone) + float(lunch) + float(travel) + float(responsibility) + float(seniority_bonus) + float(other) + float(outstanding_annual_leave) + float(OTC_incentive) + float(KPI_achievement) + float(month_13_salary_Pro_ata) + float(incentive_last_month) + float(incentive_last_quy_last_year) + float(taxable_overtime) + float(nontaxable_overtime)
                taxable_income = float(sum_K_Z) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)
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
            if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus or list_contracts[0].contract_type == contract_type_CTminusHUU :
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
        net_income = sum_K_Z + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) - float(SHUI_10point5percent_employee_pay) - float(recuperation_of_SHU_Ins_10point5percent_staff_pay) - float(PIT_balance) - float(first_payment)
        # Get transfer_bank
        transfer_bank = request.POST.get('transfer_bank')
        # Get total_cost
        total_cost = round(sum_K_Z + float(SHUI_21point5percent_company_pay) + float(recuperation_of_SHU_Ins_21point5percent_company_pay) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) + float(trade_union_fee_company_pay) + float(trade_union_fee_employee_pay) + float(transfer_bank))
        # Update and save
        payroll_update_info = Payroll_Tedis_Vietha(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                            transportation=transportation,phone=phone,lunch=lunch,travel=travel,responsibility=responsibility,seniority_bonus=seniority_bonus,
                                            other=other,outstanding_annual_leave=outstanding_annual_leave,OTC_incentive=OTC_incentive,KPI_achievement=KPI_achievement,month_13_salary_Pro_ata=month_13_salary_Pro_ata,incentive_last_month=incentive_last_month,incentive_last_quy_last_year=incentive_last_quy_last_year,taxable_overtime=taxable_overtime,nontaxable_overtime=nontaxable_overtime,
                                            SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,recuperation_of_SHU_Ins_10point5percent_staff_pay=recuperation_of_SHU_Ins_10point5percent_staff_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,recuperation_of_SHU_Ins_21point5percent_company_pay=recuperation_of_SHU_Ins_21point5percent_company_pay,
                                            occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs=occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs,
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')  
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT and working_days >= 11:
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')  
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT and working_days >= 11:
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
            # Get occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
            occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = 0
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
            contract_type_CT = Contract_type.objects.get(contract_type='CT')
            contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
            if list_contracts.count() != 0:
                if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus:
                    sum_K_X = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year + month_13_salary_Pro_ata
                    taxable_income = sum_K_X + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs - lunch
                else:
                    sum_K_X = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year + month_13_salary_Pro_ata
                    taxable_income = sum_K_X + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
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
                if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus:
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
            net_income = round(sum_K_W + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs - SHUI_10point5percent_employee_pay - PIT_balance, 0)
            # Get transfer_bank
            transfer_bank = 0
            # Get total_cost
            sum_K_W = gross_income + salary_recuperation + overtime + transportation + phone + lunch + responsibility + outstanding_annual_leave + bonus_open_new_pharmacy + other + incentive_last_quy_last_year + incentive_last_month + yearly_incentive_last_year
            total_cost = round(sum_K_W + SHUI_21point5percent_company_pay + occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs + trade_union_fee_company_pay + trade_union_fee_staff_pay + transfer_bank,0)

            
            payroll_employee_info = Payroll_Vietha(month=period_month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                                   salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,responsibility=responsibility,
                                                   outstanding_annual_leave=outstanding_annual_leave,bonus_open_new_pharmacy=bonus_open_new_pharmacy,other=other,
                                                   incentive_last_quy_last_year=incentive_last_quy_last_year,incentive_last_month=incentive_last_month,yearly_incentive_last_year=yearly_incentive_last_year,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                                   SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,
                                                   occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs=occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs,
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
                                    'font: bold 1,height 220, colour black; align: horiz center, vert center' % 'pale_blue')
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
        ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = 0
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
            ws.write(3+index, 6, str("{:,}".format(data['payroll_info'].newest_salary)),style_normal)
            ws.write(3+index, 7, str(data['payroll_info'].working_days),style_normal)
            ws.write(3+index, 8, str(data['payroll_info'].adjust_percent) + '%',style_normal)
            ws.write(3+index, 9, str("{:,}".format(data['payroll_info'].gross_income)),style_normal)
            ws.write(3+index, 10, str("{:,}".format(data['payroll_info'].salary_recuperation)),style_normal)
            ws.write(3+index, 11, str("{:,}".format(data['payroll_info'].overtime)),style_normal)
            ws.write(3+index, 12, str("{:,}".format(data['payroll_info'].transportation)),style_normal)
            ws.write(3+index, 13, str("{:,}".format(data['payroll_info'].phone)),style_normal)
            ws.write(3+index, 14, str("{:,}".format(data['payroll_info'].lunch)),style_normal)
            ws.write(3+index, 15, str("{:,}".format(data['payroll_info'].responsibility)),style_normal)
            ws.write(3+index, 16, str("{:,}".format(data['payroll_info'].outstanding_annual_leave)),style_normal)
            ws.write(3+index, 17, str("{:,}".format(data['payroll_info'].bonus_open_new_pharmacy)),style_normal)
            ws.write(3+index, 18, str("{:,}".format(data['payroll_info'].other)),style_normal)
            ws.write(3+index, 19, str("{:,}".format(data['payroll_info'].incentive_last_quy_last_year)),style_normal)
            ws.write(3+index, 20, str("{:,}".format(data['payroll_info'].incentive_last_month)),style_normal)
            ws.write(3+index, 21, str("{:,}".format(data['payroll_info'].yearly_incentive_last_year)),style_normal)
            ws.write(3+index, 22, str("{:,}".format(data['payroll_info'].month_13_salary_Pro_ata)),style_normal)
            ws.write(3+index, 23, str("{:,}".format(data['payroll_info'].SHUI_10point5percent_employee_pay)),style_normal)
            ws.write(3+index, 24, str("{:,}".format(data['payroll_info'].SHUI_21point5percent_company_pay)),style_normal)
            ws.write(3+index, 25, str("{:,}".format(data['payroll_info'].occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)),style_normal)
            ws.write(3+index, 26, str("{:,}".format(data['payroll_info'].trade_union_fee_company_pay)),style_normal)
            ws.write(3+index, 27, str("{:,}".format(data['payroll_info'].trade_union_fee_staff_pay)),style_normal)
            ws.write(3+index, 28, str("{:,}".format(data['payroll_info'].family_deduction)),style_normal)
            ws.write(3+index, 29, str("{:,}".format(data['payroll_info'].taxable_income)),style_normal)
            ws.write(3+index, 30, str("{:,}".format(data['payroll_info'].taxed_income)),style_normal)
            ws.write(3+index, 31, str("{:,}".format(data['payroll_info'].PIT_for_13th_salary)),style_normal)
            ws.write(3+index, 32, str("{:,}".format(data['payroll_info'].PIT_this_month)),style_normal)
            ws.write(3+index, 33, str("{:,}".format(data['payroll_info'].PIT_finalization)),style_normal)
            ws.write(3+index, 34, str("{:,}".format(data['payroll_info'].PIT_balance)),style_normal)
            ws.write(3+index, 35, str("{:,}".format(data['payroll_info'].net_income)),style_normal)
            ws.write(3+index, 36, str("{:,}".format(data['payroll_info'].transfer_bank)),style_normal)
            ws.write(3+index, 37, str("{:,}".format(data['payroll_info'].total_cost)),style_normal)
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
            ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs += data['payroll_info'].occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
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
        ws.write(last_row, 25, str("{:,}".format(ttoccupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)),style_table_head)
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')  
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT and working_days >= 11:
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')  
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT and working_days >= 11:
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
        # Get occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs
        occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs = request.POST.get('occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs')
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
        contract_type_CT = Contract_type.objects.get(contract_type='CT')
        contract_type_CTminus = Contract_type.objects.get(contract_type='CT-')
        if list_contracts.count() != 0:
            if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus:
                sum_K_X = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year) + float(month_13_salary_Pro_ata)
                taxable_income = sum_K_X + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) - float(lunch)
            else:
                sum_K_X = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year) + float(month_13_salary_Pro_ata)
                taxable_income = sum_K_X + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs)
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
            if list_contracts[0].contract_type == contract_type_CT or list_contracts[0].contract_type == contract_type_CTminus:
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
        net_income = round(sum_K_W + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) - float(SHUI_10point5percent_employee_pay) - float(PIT_balance), 0)
        # Get transfer_bank
        transfer_bank = request.POST.get('transfer_bank')
        # Get total_cost
        sum_K_W = float(gross_income) + float(salary_recuperation) + float(overtime) + float(transportation) + float(phone) + float(lunch) + float(responsibility) + float(outstanding_annual_leave) + float(bonus_open_new_pharmacy) + float(other) + float(incentive_last_quy_last_year) + float(incentive_last_month) + float(yearly_incentive_last_year)
        total_cost = round(sum_K_W + float(SHUI_21point5percent_company_pay) + float(occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs) + float(trade_union_fee_company_pay) + float(trade_union_fee_staff_pay) + float(transfer_bank),0)
        
        # Update and save
        payroll_update_info = Payroll_Vietha(id=payroll_info.id,month=month,employee=employee,newest_salary=newest_salary,working_days=working_days,adjust_percent=adjust_percent,gross_income=gross_income,
                                            salary_recuperation=salary_recuperation,overtime=overtime,transportation=transportation,phone=phone,lunch=lunch,responsibility=responsibility,
                                            outstanding_annual_leave=outstanding_annual_leave,bonus_open_new_pharmacy=bonus_open_new_pharmacy,other=other,
                                            incentive_last_quy_last_year=incentive_last_quy_last_year,incentive_last_month=incentive_last_month,yearly_incentive_last_year=yearly_incentive_last_year,month_13_salary_Pro_ata=month_13_salary_Pro_ata,
                                            SHUI_10point5percent_employee_pay=SHUI_10point5percent_employee_pay,SHUI_21point5percent_company_pay=SHUI_21point5percent_company_pay,
                                            occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs=occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs,
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
    list_work_days = Daily_work.objects.filter(month=period_month,weekend=False,holiday=False)
    list_days_in_month = Daily_work.objects.filter(month=period_month)
    list_data = []
    for employee in list_employees:
        daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_work_days)
        ot_daily_work_info = Daily_work_for_employee.objects.filter(employee=employee, daily_work__in=list_days_in_month, ot_time__gt=0)
        paid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, paid_leave__gt=0)
        unpaid_leave_info = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_work_days, unpaid_leave__gt=0)
        # Get OT hour to pay salary
        ot_applications = Overtime_application.objects.filter(employee=employee,application_date__month=period_month.month_number,application_date__year=period_month.period.period_year, ot_paid_hour__gt=0)
        total_paid_hour = 0
        for application in ot_applications:
            total_paid_hour += application.ot_paid_hour
        # Get daily_employee
        list_employee_days = Daily_work_for_employee.objects.filter(employee=employee,daily_work__in=list_days_in_month)
        # Count total salary working day
        total_salary_working_day = daily_work_info.count() - unpaid_leave_info.count()
        for ot_daily_work in ot_daily_work_info:
            total_salary_working_day += ot_daily_work.ot_time
        # Make data    
        data = {
            'employee': employee,
            'total_paid_leave_days': paid_leave_info.count(),
            'total_unpaid_leave_days': unpaid_leave_info.count(),
            'total_salary_working_day': total_salary_working_day,
            'total_ot_paid_hour': total_paid_hour,
            'list_employee_days' : list_employee_days,
             
        }
        list_data.append(data)
        total_working_day = daily_work_info.count()
        
    
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
    
    
    
    
def report_leave(request,pk):
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
    try:
        default_period = Period.objects.get(pk=pk)
    except Period.DoesNotExist:
        current_period = Period.objects.get(period_year=today.year)
        return redirect('employee:report_leave', pk=current_period.id)
    
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
                                    'font: bold 1,height 220, colour black;' % 'white')
        style_normal = xlwt.easyxf('pattern:pattern solid, fore_colour %s;'
                            'borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;'
                                    'font: bold off, colour black;' % 'white')   

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Leave & OT')

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





    

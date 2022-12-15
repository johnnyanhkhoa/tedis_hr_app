from asyncio.windows_events import NULL
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, CryptPasswordHasher, BCryptPasswordHasher
from django.db.models import Q
from employee.models import *
from hr.models import User
from employee.form import *
from datetime import datetime, date
from django.shortcuts import get_object_or_404

import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse
import os

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
        messages.success(request, 'Staff added!')
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
        responsibility_allowance = request.POST.get('responsibility_allowance')
        lunch_support = request.POST.get('lunch_support')
        transportation_support = request.POST.get('transportation_support')
        telephone_support = request.POST.get('telephone_support')
        contract_info = Employee_contract(employee=employee_id, contract_no=contract_no, contract_type=contract_type,signed_contract_date=signed_contract_date,from_date=from_date,to_date=to_date,basic_salary=basic_salary,responsibility_allowance=responsibility_allowance,lunch_support=lunch_support,transportation_support=transportation_support,telephone_support=telephone_support)                 
        if str(employee_site) == 'RO':
            contract_info.save()
            return redirect('employee:RO_HDLD', pk=employee.pk)
        if str(employee_site) == "JV":
            contract_info.save()
            return redirect('employee:JV_HDLD', pk=employee.pk)
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
            return redirect('employee:TD_job_offer_FORM', pk=employee.pk)
        if str(employee_site) == "JV":
            period_info.save()
            return redirect('employee:JV_job_offer_FORM', pk=employee.pk)
        else:
            messages.error(request, 'MISSING DATA: Employee Site')
    
    return render(request, 'employee/form_probationary_period.html', {
        'employee' : employee,
    })
    

def TD_job_offer_FORM(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
    employee = Employee.objects.get(pk=pk)
    
    
    return render(request, 'employee/TD_letter_job_offer.html', {
        'employee' : employee,
    })
    

def JV_job_offer_FORM(request, pk):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
    # Get employee:
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
    
    
    return render(request, 'employee/JV_letter_job_offer.html', {
        'employee' : employee,
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
    

def RO_HDLD(request, pk):
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
    
    
    return render(request, 'employee/RO_HDLD.html', {
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
    filename = 'report_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def JV_HDLD_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)

    html_string = render_to_string('employee/JV_HDLD.html', {
        'today': today,
        'employee': employee,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'report_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "C:\\" + filename, configuration=config)

    return HttpResponse(html_string)


def RO_HDLD_PDF(request, pk):
    today = datetime.now().strftime('%d-%m-%Y')

    employee = Employee.objects.get(pk=pk)

    html_string = render_to_string('employee/RO_HDLD.html', {
        'today': today,
        'employee': employee,
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    filename = 'report_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
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
    
    # Get Leave application
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
    approved_date = date.today()
    
    # Get Leave application
    leave_application = Leave_application.objects.get(pk=pk)
    
     # Data input
    if request.POST.get('btn_approve'):
        status = Status.objects.get(id=2)
        # Annual
        annual_from = request.POST.get('annual_from')
        annual_to = request.POST.get('annual_to')
        annual_number_of_leave_days = request.POST.get('annual_number_of_leave_days')
        # Non-paid
        non_paid_from = request.POST.get('non_paid_from')
        non_paid_to = request.POST.get('non_paid_to')
        non_paid_number_of_leave_days = request.POST.get('non_paid_number_of_leave_days')
        # Wedding
        wedding_from = request.POST.get('wedding_from')
        wedding_to = request.POST.get('wedding_to')
        wedding_number_of_leave_days = request.POST.get('wedding_number_of_leave_days')
        # Bereavement
        bereavement_from = request.POST.get('bereavement_from')
        bereavement_to = request.POST.get('bereavement_to')
        bereavement_number_of_leave_days = request.POST.get('bereavement_number_of_leave_days')
        # Maternity / Obstetric
        maternity_obstetric_from = request.POST.get('maternity_obstetric_from')
        maternity_obstetric_to = request.POST.get('maternity_obstetric_to')
        maternity_obstetric_number_of_leave_days = request.POST.get('maternity_obstetric_number_of_leave_days')
        # Sick
        sick_from = request.POST.get('sick_from')
        sick_to = request.POST.get('sick_to')
        sick_number_of_leave_days = request.POST.get('sick_number_of_leave_days')
        # Off in-lieu
        offinlieu_from = request.POST.get('offinlieu_from')
        offinlieu_to = request.POST.get('offinlieu_to')
        offinlieu_number_of_leave_days = request.POST.get('offinlieu_number_of_leave_days')
        # Other
        other_from = request.POST.get('other_from')
        other_to = request.POST.get('other_to')
        other_number_of_leave_days = request.POST.get('other_number_of_leave_days')
        # SAVE LEAVE APLLICATION AFTER EDIT AND APPROVE
        # Annual
        leave_application.annual_from = annual_from
        leave_application.annual_to = annual_to
        leave_application.annual_number_of_leave_days = annual_number_of_leave_days
        # Non-paid
        leave_application.non_paid_from = non_paid_from
        leave_application.non_paid_to = non_paid_to
        leave_application.non_paid_number_of_leave_days = non_paid_number_of_leave_days
        # Wedding
        leave_application.wedding_from = wedding_from
        leave_application.wedding_to = wedding_to
        leave_application.wedding_number_of_leave_days = wedding_number_of_leave_days
        # Bereavement
        leave_application.bereavement_from = bereavement_from
        leave_application.bereavement_to = bereavement_to
        leave_application.bereavement_number_of_leave_days = bereavement_number_of_leave_days
        # Maternity / Obstetric
        leave_application.maternity_obstetric_from = maternity_obstetric_from
        leave_application.maternity_obstetric_to = maternity_obstetric_to
        leave_application.maternity_obstetric_number_of_leave_days = maternity_obstetric_number_of_leave_days
        # Sick
        leave_application.sick_from = sick_from
        leave_application.sick_to = sick_to
        leave_application.sick_number_of_leave_days = sick_number_of_leave_days
        # Off in-lieu
        leave_application.offinlieu_from = offinlieu_from
        leave_application.offinlieu_to = offinlieu_to
        leave_application.offinlieu_number_of_leave_days = offinlieu_number_of_leave_days
        # Other
        leave_application.other_from = other_from
        leave_application.other_to = other_to
        leave_application.other_number_of_leave_days = other_number_of_leave_days
        # Status
        leave_application.hr_status = status
        leave_application.hr_approved_date = approved_date
        leave_application.save()
        return redirect('/leave_verification/')
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
        'hr_ot_leave_application' : hr_ot_leave_application
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
            status = Status.objects.get(id=2)
            ot_application.hr_status = status
            ot_application.hr_approved_date = approved_date
            ot_application.save()
            return redirect('/ot_verification/')
    if request.POST.get('btn_reject'):
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
        if request.POST.get('btn_reject'):
            status = Status.objects.get(id=3)
            ot_application.status = status
            ot_application.approved_date = approved_date
            ot_application.save()
            return redirect('/ot_verification/')
    
    
        
    return render(request, 'employee/form_ot_approve.html', {
        'employee' : employee,
        'ot_application' : ot_application,
        'approved_date' : approved_date,
        
    })


# Period and Dayoff
def start_period(request):
    # Kiểm tra session xem khách hàng đã đăng nhập chưa?
    if 's_user' not in request.session:
        return redirect('hr:signin')
    
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
                remain_dayoff = previous_dayoff.total_dayoff
            except Period.DoesNotExist:
                previous_period = None
                remain_dayoff = 0              
            dayoff_info = Dayoff(period=period,employee=employee,total_dayoff=total_dayoff,remain_dayoff=remain_dayoff)
            dayoff_info.save()
        
    if request.POST.get('btnReset'):    
        present_period = Period.objects.get(period_year=today.year)
        list_dayoff = Dayoff.objects.filter(period=present_period)
        print(list_dayoff)
        

    
    return render(request, 'employee/period.html', {
    
    })


# def dayoff(request):
#     # Kiểm tra session xem khách hàng đã đăng nhập chưa?
#     if 's_user' not in request.session:
#         return redirect('hr:signin')
    
#     list_dayoff = Employee_dayoff.objects.all()
#     today = datetime.now().strftime('%d-%m-%Y')
#     str_today = str(today)
#     if str_today == "01-01-2022":
#         for dayoff in list_dayoff:
#             employee_dayoff = Employee_dayoff.objects.get(employee=dayoff.employee.id)
#             employee_dayoff.used_dayoff = 0
#             employee_dayoff.save()
#         return redirect('employee:dayoff')
#     else: 
#         pass
    
#     return render(request, 'employee/dayoff.html', {
#         'list_dayoff' : list_dayoff,
#     })



    

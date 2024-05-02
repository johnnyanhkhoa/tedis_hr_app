from django import forms
from .models import *

# YEARS
years = []
for year in range(1930,2050):
    years.append(year)
# Queryset
site_list = Site.objects.only('id')
division_list = Division.objects.only('id')
department_e_list = Department_E.objects.only('id')
department_v_list = Department_V.objects.only('id')
area_list = Area.objects.only('id')
provinces_list = Provinces.objects.only('id')
gp_list = Gp.objects.only('id')
function_list = Function.objects.only('id')
position_e_list = Position_E.objects.only('id')
abb_position_list = Abbreviation_Position.objects.only('id')
position_v_list = Position_V.objects.only('id')
contract_type_list = Contract_type.objects.only('id')
sexual_list = Sexual.objects.only('id')
ethic_group_list = Ethic_group.objects.only('id')
marital_status_list = Marital_status.objects.only('id')
certificate_e_list = Certificate_E.objects.only('id')
certificate_v_list = Certificate_V.objects.only('id')
university_list = University.objects.only('id')
hi_medical_place_list = Hi_medical_place.objects.only('id')
relation_1_list = Relation_1.objects.only('id')
relation_2_list = Relation_2.objects.only('id')
staff_info_submission_list = Staff_info_submission.objects.only('id')
employee_list = Employee.objects.only('id')

class DateInput(forms.DateInput):
    input_type = 'date'

# Form
class CreateEmployeeForm(forms.ModelForm):
    employee_code = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "Employee code",
    }))
    full_name = forms.CharField(strip=False, required=True, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Full name",
    }))
    site = forms.ModelChoiceField(required=False, queryset=site_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Site",
    }))
    division = forms.ModelChoiceField(required=False, queryset=division_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Division",
    }))
    department_e = forms.ModelChoiceField(required=False, queryset=department_e_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Department E",
    }))
    department_v = forms.ModelChoiceField(required=False, queryset=department_v_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Department V",
    }))
    sub_department_1 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Sub-Department 1",
    }))
    sub_department_2 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Sub-Department 2",
    }))
    sub_department_3 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Sub-Department 3",
    }))
    area = forms.ModelChoiceField(required=False, queryset=area_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Area",
    }))
    provinces = forms.ModelChoiceField(required=False, queryset=provinces_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Province",
    }))
    sub_province = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Sub-Province",
    }))
    gp = forms.ModelChoiceField(required=False, queryset=gp_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Group",
    }))
    function = forms.ModelChoiceField(required=False, queryset=function_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Function",
    }))
    position_e = forms.ModelChoiceField(required=False, queryset=position_e_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Positon E",
    }))
    abb_position = forms.ModelChoiceField(required=False, queryset=abb_position_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Abbreviation position",
    }))
    position_v = forms.ModelChoiceField(required=False, queryset=position_v_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Position V",
    }))
    joining_date = forms.DateField(required=True, widget=DateInput())
    out_date = forms.DateField(required=False, widget=DateInput())
    years_of_service = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Years of service",
    }))
    from_date = forms.DateField(required=False, widget=DateInput())
    to_date = forms.DateField(required=False, widget=DateInput())
    sexual = forms.ModelChoiceField(required=False, queryset=sexual_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Sexual",
    }))
    date_of_birth = forms.DateField(required=True, widget=DateInput())
    place_of_birth = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Place of birth",
    }))
    ethic_group = forms.ModelChoiceField(required=False, queryset=ethic_group_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Ethic group",
    }))
    id_card_no = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "ID card number",
    }))
    issued_date_of_id_card = forms.DateField(required=False, widget=DateInput())
    issued_place_of_id_card = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Issued place of ID card",
    }))
    permanent_address = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Permanent address",
    }))
    contact_address = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Send documents to address",
    }))
    cellphone_no = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Cellphone number",
    }))
    marital_status = forms.ModelChoiceField(required=False, queryset=marital_status_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Marital status",
    }))
    company_email = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Company email",
    }))
    personal_email = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Personal email",
    }))
    account_no = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Account number",
    }))
    bank = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Bank",
    }))
    bank_address = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Bank address",
    }))
    branch = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Branch",
    }))
    certificate_e = forms.ModelChoiceField(required=False, queryset=certificate_e_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Certificate E",
    }))
    certificate_v = forms.ModelChoiceField(required=False, queryset=certificate_v_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Certificate V",
    }))
    university = forms.ModelChoiceField(required=False, queryset=university_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "University",
    }))
    major_e = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Major E",
    }))
    major_v = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Major V",
    }))
    social_insurrance_book = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Social insurrance book",
    }))
    hi_medical_place = forms.ModelChoiceField(required=False, queryset=hi_medical_place_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "HI medical place",
    }))
    personal_income_tax = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Personal income tax",
    }))
    children = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Children",
    }))
    birthday_of_children = forms.DateField(required=False, widget=DateInput())
    emergency_contact_1 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Emergency contact 1",
    }))
    relation_1 = forms.ModelChoiceField(required=False, queryset=relation_1_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Relation 1",
    }))
    contact_address_1 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Contact address 1",
    }))
    phone_1 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Phone 1",
    }))
    emergency_contact_2 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Emergency contact 2",
    }))
    relation_2 = forms.ModelChoiceField(required=False, queryset=relation_2_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Relation 2",
    }))
    contact_address_2 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Contact address 2",
    }))
    phone_2 = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Phone 2",
    }))
    year_of_birth = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "Year of birth",
    }))
    age = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "Age",
    }))
    remark = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Remark",
    }))
    staff_info_submission = forms.ModelChoiceField(required=False, queryset=staff_info_submission_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Staff information submission",
    }))
    active = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "1: Active ; 0: Inactive",
    }))
    created_at = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "created_at",
    }))
    class Meta:
        model = Employee
        fields = '__all__'
        

class AddChildrenForm(forms.ModelForm):
    employee = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Employee",
    }))
    children = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Children",
    }))
    birthday_of_children = forms.DateField(required=False, widget=DateInput())
    class Meta:
        model = Employee_children
        fields = '__all__'

class AddContractForm(forms.ModelForm):
    employee = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Employee",
    }))
    contract_no = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Contract number",
    }))
    contract_type = forms.ModelChoiceField(required=False, queryset=contract_type_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Contract type",
    }))
    signed_contract_date = forms.DateField(required=False, widget=DateInput())
    class Meta:
        model = Employee_contract
        fields = '__all__'
    
class Probationary_period_form(forms.ModelForm):
    employee = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Employee",
    }))
    letter_date = forms.DateField(required=False, widget=DateInput())
    from_date = forms.DateField(required=False, widget=DateInput())
    to_date = forms.DateField(required=False, widget=DateInput())
    monthly_gross_salary = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "Monthly gross salary",
    }))
    monthly_allowance = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "Monthly allowance",
    }))
    
    class Meta:
        model = Probationary_period
        fields = '__all__'


class AddManager(forms.ModelForm):
    employee = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Employee",
    }))
    manager = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Employee",
    }))
    
    class Meta:
        model = Employee_manager
        fields = '__all__'
        

# leave_type_list = Type_of_leave.objects.only('id')   
# hour_list = Hour.objects.only('id') 
# minute_list = Minute.objects.only('id') 
# class Leave_application_form(forms.ModelForm):
#     employee = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
#         "class": "form-control bg-white", "placeholder": "Employee",
#     }))
#     leave_type = forms.ModelChoiceField(required=False, queryset=leave_type_list ,widget=forms.Select(attrs={
#         "class": "form-control bg-white", "placeholder": "Leave type",
#     }))
#     from_hour = forms.ModelChoiceField(required=False, queryset=hour_list ,widget=forms.Select(attrs={
#         "class": "form-control bg-white", "placeholder": "Hour",
#     }))
#     from_minute = forms.ModelChoiceField(required=False, queryset=minute_list ,widget=forms.Select(attrs={
#         "class": "form-control bg-white", "placeholder": "Minute",
#     }))
#     from_date = forms.DateField(required=False, widget=DateInput())
#     to_hour = forms.ModelChoiceField(required=False, queryset=hour_list ,widget=forms.Select(attrs={
#         "class": "form-control bg-white", "placeholder": "Hour",
#     }))
#     to_minute = forms.ModelChoiceField(required=False, queryset=minute_list ,widget=forms.Select(attrs={
#         "class": "form-control bg-white", "placeholder": "Minute",
#     }))
#     to_date = forms.DateField(required=False, widget=DateInput())
    
    
#     letter_date = forms.DateField(required=False, widget=DateInput())
#     from_date = forms.DateField(required=False, widget=DateInput())
#     to_date = forms.DateField(required=False, widget=DateInput())
#     monthly_gross_salary = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
#         "class": "form-control", "placeholder": "Monthly gross salary",
#     }))
#     monthly_allowance = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
#         "class": "form-control", "placeholder": "Monthly allowance",
#     }))
    
#     class Meta:
#         model = Probationary_period
#         fields = '__all__'
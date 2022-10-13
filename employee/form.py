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
department_area_list = Department_area.objects.only('id')
function_list = Function.objects.only('id')
job_title_list = Job_title.objects.only('id')
position_e_list = Position_E.objects.only('id')
position_v_list = Position_V.objects.only('id')
contract_type_list = Contract_type.objects.only('id')
sexual_list = Sexual.objects.only('id')
ethic_group_list = Ethic_group.objects.only('id')
marital_status_list = Marital_status.objects.only('id')
certificate_e_list = Certificate_E.objects.only('id')
certificate_v_list = Certificate_V.objects.only('id')
hi_registered_place_list = Hi_registered_place.objects.only('id')
relation_1_list = Relation_1.objects.only('id')
relation_2_list = Relation_2.objects.only('id')
bo_sung_ho_so_list = Bo_sung_ho_so.objects.only('id')
da_nop_thong_tin_nhan_vien_list = Da_nop_thong_tin_nhan_vien.objects.only('id')
employee_list = Employee.objects.only('id')

class DateInput(forms.DateInput):
    input_type = 'date'

# Form
class CreateEmployeeForm(forms.ModelForm):
    employee_code = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        "class": "form-control", "placeholder": "Employee code",
    }))
    full_name = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
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
    area = forms.ModelChoiceField(required=False, queryset=area_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Area",
    }))
    provinces = forms.ModelChoiceField(required=False, queryset=provinces_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Province",
    }))
    gp = forms.ModelChoiceField(required=False, queryset=gp_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "GP",
    }))
    department_area = forms.ModelChoiceField(required=False, queryset=department_area_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Department area",
    }))
    function = forms.ModelChoiceField(required=False, queryset=function_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Function",
    }))
    job_title = forms.ModelChoiceField(required=False, queryset=job_title_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Job title",
    }))
    position_e = forms.ModelChoiceField(required=False, queryset=position_e_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Positon E",
    }))
    position_v = forms.ModelChoiceField(required=False, queryset=position_v_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Position V",
    }))
    joining_date = forms.DateField(required=False, widget=DateInput())
    out_date = forms.DateField(required=False, widget=DateInput())
    years_of_service = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Years of service",
    }))
    promotion_effective_date = forms.DateField(required=False, widget=DateInput())
    contract_no = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Contract number",
    }))
    contract_type = forms.ModelChoiceField(required=False, queryset=contract_type_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Contract type",
    }))
    signed_contract_date = forms.DateField(required=False, widget=DateInput())
    from_date = forms.DateField(required=False, widget=DateInput())
    to_date = forms.DateField(required=False, widget=DateInput())
    sexual = forms.ModelChoiceField(required=False, queryset=sexual_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Sexual",
    }))
    date_of_birth = forms.DateField(required=False, widget=DateInput())
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
    current_address = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Current address",
    }))
    send_documents_to_address = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
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
    with_bank = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "With bank",
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
    major_e = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Major E",
    }))
    major_v = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Major V",
    }))
    social_insurrance_book = forms.CharField(strip=False, required=False, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Social insurrance book",
    }))
    hi_registered_place = forms.ModelChoiceField(required=False, queryset=hi_registered_place_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "HI registered place",
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
    bo_sung_ho_so = forms.ModelChoiceField(required=False, queryset=bo_sung_ho_so_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Bo sung ho so",
    }))
    da_nop_thong_tin_nhan_vien = forms.ModelChoiceField(required=False, queryset=da_nop_thong_tin_nhan_vien_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Da nop thong tin nhan vien",
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
    
class Probationary_period_form(forms.ModelForm):
    employee = forms.ModelChoiceField(required=False, queryset=employee_list ,widget=forms.Select(attrs={
        "class": "form-control bg-white", "placeholder": "Employee",
    }))
    from_date = forms.DateField(required=False, widget=DateInput())
    to_date = forms.DateField(required=False, widget=DateInput())
    class Meta:
        model = Probationary_period
        fields = '__all__'
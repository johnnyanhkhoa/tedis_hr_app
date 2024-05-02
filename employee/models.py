from django.db import models
from django.utils.timezone import now
from datetime import datetime
today = datetime.now()

# Employee
class Site(models.Model):
    site = models.CharField(max_length=10, blank=False, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.site


class Division(models.Model):
    division = models.CharField(max_length=50, blank=False, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.division
    

class Department_E(models.Model):
    department_e = models.CharField(max_length=50, blank=False, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.department_e
    

class Department_V(models.Model):
    department_v = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.department_v


class Area(models.Model):
    area = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.area


class Provinces(models.Model):
    provinces = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.provinces
    

class Gp(models.Model):
    gp = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.gp
        

class Function(models.Model):
    function = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.function
       

class Position_E(models.Model):
    position_e = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.position_e
    

class Position_V(models.Model):
    position_v = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.position_v


class Abbreviation_Position(models.Model):
    abb_position = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.abb_position


class Contract_category(models.Model):
    contract_category = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.contract_category
    

class Contract_type(models.Model):
    contract_type = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.contract_type
    

class Sexual(models.Model):
    sexual = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sexual


class Ethic_group(models.Model):
    ethic_group = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ethic_group
    

class Marital_status(models.Model):
    marital_status = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.marital_status
    

class Certificate_E(models.Model):
    certificate_e = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.certificate_e
    

class Certificate_V(models.Model):
    certificate_v = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.certificate_v
    

class University(models.Model):
    university = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.university
    

class Hi_medical_place(models.Model):
    hi_medical_place = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hi_medical_place


class Relation_1(models.Model):
    relation_1 = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.relation_1  
    

class Relation_2(models.Model):
    relation_2 = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.relation_2  
    

class Staff_info_submission(models.Model):
    staff_info_submission = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.staff_info_submission  

    
class Employee(models.Model):
    employee_code = models.IntegerField(blank=False) #JOB
    full_name = models.CharField(max_length=100, blank=False) #PERSONAL
    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True) #JOB
    division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True) #JOB
    department_e = models.ForeignKey(Department_E, on_delete=models.PROTECT, null=True) #JOB
    department_v = models.ForeignKey(Department_V, on_delete=models.PROTECT, null=True, blank=True) #JOB
    sub_department_1 = models.CharField(max_length=25, blank=True, null=True)
    sub_department_2 = models.CharField(max_length=25, blank=True, null=True)
    sub_department_3 = models.CharField(max_length=25, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True) #JOB
    provinces = models.ForeignKey(Provinces, on_delete=models.PROTECT, null=True, blank=True) #JOB
    sub_province = models.CharField(max_length=25, blank=True, null=True)
    gp = models.ForeignKey(Gp, on_delete=models.PROTECT, null=True, blank=True) #JOB
    function = models.ForeignKey(Function, on_delete=models.PROTECT, null=True, blank=True) #JOB
    position_e = models.ForeignKey(Position_E, on_delete=models.PROTECT, null=True) #JOB
    position_v = models.ForeignKey(Position_V, on_delete=models.PROTECT, null=True) #JOB
    abb_position = models.ForeignKey(Abbreviation_Position, on_delete=models.PROTECT, null=True, blank=True) #JOB
    joining_date = models.DateField(max_length=50, null=True) #JOB
    joining_year = models.IntegerField(blank=True,null=True) #JOB
    out_date = models.DateField(max_length=50, null=True, blank=True) #JOB 
    years_of_service = models.FloatField(null=True, blank=True) #JOB
    from_date = models.DateField(max_length=30, blank=True,null=True) #JOB
    to_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    sexual = models.ForeignKey(Sexual, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    date_of_birth = models.DateField(max_length=30, blank=True, null=True) #PERSONAL
    place_of_birth = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    ethic_group = models.ForeignKey(Ethic_group, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    id_card_no = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    issued_date_of_id_card = models.DateField(max_length=30, blank=True, null=True) #PERSONAL
    issued_place_of_id_card = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    permanent_address = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    contact_address = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    cellphone_no = models.CharField(max_length=20, blank=True, null=True) #PERSONAL
    marital_status = models.ForeignKey(Marital_status, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    company_email = models.CharField(max_length=50, blank=True, null=True) #JOB
    personal_email = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    account_no = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    bank = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    bank_address = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    branch = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    certificate_e = models.ForeignKey(Certificate_E, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    certificate_v = models.ForeignKey(Certificate_V, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    university = models.ForeignKey(University, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    major_e = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    major_v = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    social_insurrance_book = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    hi_medical_place = models.ForeignKey(Hi_medical_place, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    personal_income_tax = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    children = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    birthday_of_children = models.DateField(max_length=30, blank=True, null=True) #PERSONAL
    emergency_contact_1 = models.CharField(max_length=50, blank=True, null=True) #EMERGENCY CONTACT
    relation_1 = models.ForeignKey(Relation_1, on_delete=models.PROTECT, null=True, blank=True) #EMERGENCY CONTACT
    contact_address_1 = models.CharField(max_length=50, blank=True, null=True) #EMERGENCY CONTACT
    phone_1 = models.CharField(max_length=30, blank=True, null=True) #EMERGENCY CONTACT
    emergency_contact_2 = models.CharField(max_length=50, blank=True, null=True) #EMERGENCY CONTACT
    relation_2 = models.ForeignKey(Relation_2, on_delete=models.PROTECT, null=True, blank=True) #EMERGENCY CONTACT
    contact_address_2 = models.CharField(max_length=50, blank=True, null=True) #EMERGENCY CONTACT
    phone_2 = models.CharField(max_length=30, blank=True, null=True) #EMERGENCY CONTACT
    year_of_birth = models.IntegerField(blank=True, null=True) #PERSONAL
    age = models.IntegerField(blank=True, null=True) #PERSONAL
    remark = models.CharField(max_length=200, blank=True, null=True) #ANOTHER
    staff_info_submisstion = models.ForeignKey(Staff_info_submission, on_delete=models.PROTECT, null=True, blank=True) #ANOTHER
    # Active 
    active = models.IntegerField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name
    

class Employee_manager(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, related_name='employee')
    manager = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, related_name='manager_of_employee')

    def __int__(self):
        return self.employee 


class Employee_children(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    children = models.CharField(max_length=50, blank=True, null=True)
    birthday_of_children = models.DateField(max_length=30, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True,)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee 
    

class Probationary_period(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    letter_date = models.DateField(max_length=30, blank=True, null=True)
    from_date = models.DateField(max_length=30, blank=True, null=True)
    to_date = models.DateField(max_length=30, blank=True, null=True) 
    monthly_gross_salary = models.FloatField(blank=True, null=True)
    monthly_allowance = models.FloatField(blank=True, null=True)
    letter_returning_date = models.DateField(max_length=30, blank=True, null=True)

    def __int__(self):
        return self.employee 


class Employee_contract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    contract_no = models.CharField(max_length=50, blank=True, null=True) #JOB
    contract_category = models.ForeignKey(Contract_category, on_delete=models.PROTECT, null=True, blank=True) #JOB
    contract_type = models.ForeignKey(Contract_type, on_delete=models.PROTECT, null=True, blank=True) #JOB
    signed_contract_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    from_date = models.DateField(max_length=30, blank=True, null=True)
    to_date = models.DateField(max_length=30, blank=True, null=True)
    basic_salary = models.FloatField(null=True, blank=True)
    responsibility_allowance = models.FloatField(null=True, blank=True)
    lunch_support = models.FloatField(null=True, blank=True)
    transportation_support = models.FloatField(null=True, blank=True)
    telephone_support = models.FloatField(null=True, blank=True)
    travel_support = models.FloatField(null=True, blank=True)
    seniority_bonus = models.FloatField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee 
    
    
class Employee_promotion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    promotion_effective_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    promotion_decision_number = models.CharField(max_length=10, blank=True, null=True) #JOB
    created_by = models.IntegerField(null=True, blank=True,)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee 


# Leave and OT
class Status(models.Model):
    status = models.CharField(max_length=50, blank=True, null=True)

    def __int__(self):
        return self.status    
    

class Type_of_leave(models.Model):
    leave_type_eng = models.CharField(max_length=50, blank=True, null=True)
    leave_type_vn = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True,)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.leave_type_eng
    

class Leave_application(models.Model):    
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=10, blank=True, null=True)
    relation = models.CharField(max_length=10, blank=True, null=True)
    # Annual Leave
    annual_from = models.CharField(max_length=50, blank=True, null=True)
    annual_to = models.CharField(max_length=50, blank=True, null=True)
    annual_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    annual_remark = models.CharField(max_length=200, blank=True, null=True)
    annual_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Non-paid Leave
    non_paid_from = models.CharField(max_length=50, blank=True, null=True)
    non_paid_to = models.CharField(max_length=50, blank=True, null=True)
    non_paid_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    non_paid_remark = models.CharField(max_length=200, blank=True, null=True)
    non_paid_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Wedding Leave
    wedding_from = models.CharField(max_length=50, blank=True, null=True)
    wedding_to = models.CharField(max_length=50, blank=True, null=True)
    wedding_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    wedding_remark = models.CharField(max_length=200, blank=True, null=True)
    wedding_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Bereavement Leave
    bereavement_from = models.CharField(max_length=50, blank=True, null=True)
    bereavement_to = models.CharField(max_length=50, blank=True, null=True)
    bereavement_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    bereavement_remark = models.CharField(max_length=200, blank=True, null=True)
    bereavement_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Maternity/Obstetric Leave
    maternity_obstetric_from = models.CharField(max_length=50, blank=True, null=True)
    maternity_obstetric_to = models.CharField(max_length=50, blank=True, null=True)
    maternity_obstetric_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    maternity_obstetric_remark = models.CharField(max_length=200, blank=True, null=True)
    maternity_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Sick Leave
    sick_from = models.CharField(max_length=50, blank=True, null=True)
    sick_to = models.CharField(max_length=50, blank=True, null=True)
    sick_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    sick_remark = models.CharField(max_length=200, blank=True, null=True)
    sick_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Off in-lieu Leave
    offinlieu_from = models.CharField(max_length=50, blank=True, null=True)
    offinlieu_to = models.CharField(max_length=50, blank=True, null=True)
    offinlieu_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    offinlieu_remark = models.CharField(max_length=200, blank=True, null=True)
    offinlieu_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    # Other Leave
    other_from = models.CharField(max_length=50, blank=True, null=True)
    other_to = models.CharField(max_length=50, blank=True, null=True)
    other_number_of_leave_days = models.CharField(max_length=10, blank=True, null=True)
    other_remark = models.CharField(max_length=200, blank=True, null=True)
    offinlieu_halfday_note = models.CharField(max_length=200, blank=True, null=True)
    
    total_days = models.FloatField(null=True, blank=True)
    temporary_replacement = models.CharField(max_length=50, blank=True, null=True)
    application_date = models.DateField(max_length=30, blank=True, null=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, related_name='leave_approved_by')
    approved_date = models.DateField(max_length=30, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    hr_approved_date = models.DateField(max_length=30, blank=True, null=True)
    hr_status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, related_name='hr_leave_status')
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee 
    
    
class Overtime_application(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    application_date = models.DateField(max_length=30, blank=True, null=True)
    month = models.CharField(max_length=5, blank=True, null=True, default=today.month)
    ot_date = models.DateField(max_length=30, blank=True, null=True)
    ot_time_from = models.TimeField(max_length=30, blank=True, null=True)
    ot_time_to = models.TimeField(max_length=30, blank=True, null=True)
    ot_total_time = models.FloatField(null=True, blank=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    approved_by = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, related_name='ot_approved_by')
    approved_date = models.DateField(max_length=30, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    hr_approved_date = models.DateField(max_length=30, blank=True, null=True)
    hr_status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, related_name='hr_ot_status')
    ot_paid_hour = models.IntegerField(null=True, blank=True)
    ot_unpaid_day = models.FloatField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee 
    

# Period and Day off
class Period(models.Model):
    period_year = models.IntegerField(null=True, blank=True)
    start_period_date = models.DateField(max_length=30, blank=True, null=True)
    end_period_date = models.DateField(max_length=30, blank=True, null=True)
    total_months = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.period_year


class Month_in_period(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    month_name = models.CharField(max_length=100, blank=True, null=True)
    month_number = models.IntegerField(null=True, blank=True)
    total_days = models.IntegerField(null=True, blank=True)
    holidays = models.CharField(max_length=500, blank=True, null=True)
    total_work_days_bo = models.FloatField(null=True, blank=True)
    total_work_days_wh = models.FloatField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.period
    

class Dayoff(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    total_dayoff = models.FloatField(null=True, blank=True, default=12)
    used_dayoff = models.FloatField(null=True, blank=True)
    remain_dayoff = models.FloatField(null=True, blank=True)
    previous_remain_dayoff = models.FloatField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee 
    

class Update_dayoff(models.Model):
    leave_application = models.ForeignKey(Leave_application, on_delete=models.PROTECT, null=True)
    ot_application = models.ForeignKey(Overtime_application, on_delete=models.PROTECT, null=True)
    day_off = models.ForeignKey(Dayoff, on_delete=models.PROTECT, null=True)
    plus_dayoff = models.FloatField(null=True, blank=True)
    minus_dayoff = models.FloatField(null=True, blank=True)
    reason_of_changing = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.day_off 
    

class Daily_work(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    date = models.DateField(max_length=100, blank=True, null=True)
    weekend = models.BooleanField(blank=True, null=True)
    holiday = models.BooleanField(blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.date


class Daily_work_for_employee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    daily_work = models.ForeignKey(Daily_work, on_delete=models.PROTECT, null=True)
    work = models.FloatField(blank=True, null=True, default=0)
    paid_leave = models.FloatField(blank=True, null=True, default=0)
    unpaid_leave = models.FloatField(blank=True, null=True, default=0)
    leave_application = models.ForeignKey(Leave_application, on_delete=models.PROTECT, null=True)
    overtime = models.BooleanField(blank=True, null=True)
    overtime_application = models.ForeignKey(Overtime_application, on_delete=models.PROTECT, null=True)
    ot_time = models.FloatField(blank=True, null=True, default=0)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee
    

# Payroll
class Payroll_Tedis(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    newest_salary = models.FloatField(blank=True, null=True)
    working_days = models.FloatField(blank=True, null=True)
    adjust_percent = models.FloatField(blank=True, null=True)
    gross_income = models.FloatField(blank=True, null=True)
    salary_recuperation = models.FloatField(blank=True, null=True, default=0)
    overtime = models.FloatField(blank=True, null=True, default=0)
    transportation = models.FloatField(blank=True, null=True)
    phone = models.FloatField(blank=True, null=True)
    lunch = models.FloatField(blank=True, null=True)
    training_fee = models.FloatField(blank=True, null=True, default=0)
    toxic_allowance = models.FloatField(blank=True, null=True, default=0)
    travel = models.FloatField(blank=True, null=True, default=0)
    responsibility = models.FloatField(blank=True, null=True)
    seniority_bonus = models.FloatField(blank=True, null=True, default=0)
    other = models.FloatField(blank=True, null=True, default=0)
    total_allowance_recuperation = models.FloatField(blank=True, null=True, default=0)
    benefits = models.FloatField(blank=True, null=True, default=0)
    severance_allowance = models.FloatField(blank=True, null=True, default=0)
    outstanding_annual_leave = models.FloatField(blank=True, null=True, default=0)
    month_13_salary_Pro_ata = models.FloatField(blank=True, null=True, default=0)
    SHUI_10point5percent_employee_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_10point5percent_staff_pay = models.FloatField(blank=True, null=True, default=0)
    SHUI_21point5percent_company_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_21point5percent_company_pay = models.FloatField(blank=True, null=True, default=0)
    taxable_overtime = models.FloatField(blank=True, null=True, default=0)
    nontaxable_overtime = models.FloatField(blank=True, null=True, default=0)
    occupational_accident_and_disease = models.FloatField(blank=True, null=True, default=0)
    trade_union_fee_company_pay_2percent = models.FloatField(blank=True, null=True)
    trade_union_fee_member = models.FloatField(blank=True, null=True)
    family_deduction = models.FloatField(blank=True, null=True)
    taxable_income  = models.FloatField(blank=True, null=True)
    taxed_income  = models.FloatField(blank=True, null=True)
    PIT  = models.FloatField(blank=True, null=True)
    deduct = models.FloatField(blank=True, null=True, default=0)
    net_income = models.FloatField(blank=True, null=True)
    transfer_bank = models.FloatField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Payroll_Vietha(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    newest_salary = models.FloatField(blank=True, null=True)
    working_days = models.FloatField(blank=True, null=True)
    adjust_percent = models.FloatField(blank=True, null=True)
    gross_income = models.FloatField(blank=True, null=True)
    salary_recuperation = models.FloatField(blank=True, null=True, default=0)
    overtime = models.FloatField(blank=True, null=True, default=0)
    transportation = models.FloatField(blank=True, null=True)
    phone = models.FloatField(blank=True, null=True)
    lunch = models.FloatField(blank=True, null=True)
    responsibility = models.FloatField(blank=True, null=True)
    seniority_bonus = models.FloatField(blank=True, null=True, default=0)
    outstanding_annual_leave = models.FloatField(blank=True, null=True, default=0)
    bonus_open_new_pharmacy = models.FloatField(blank=True, null=True, default=0)
    travel = models.FloatField(blank=True, null=True, default=0)
    other = models.FloatField(blank=True, null=True, default=0)
    incentive_last_quy_last_year = models.FloatField(blank=True, null=True, default=0)
    incentive_last_month = models.FloatField(blank=True, null=True, default=0)
    yearly_incentive_last_year = models.FloatField(blank=True, null=True, default=0)
    month_13_salary_Pro_ata = models.FloatField(blank=True, null=True, default=0)
    SHUI_10point5percent_employee_pay = models.FloatField(blank=True, null=True)
    SHUI_21point5percent_company_pay = models.FloatField(blank=True, null=True)
    occupational_accident_and_disease = models.FloatField(blank=True, null=True, default=0)
    trade_union_fee_company_pay = models.FloatField(blank=True, null=True)
    trade_union_fee_staff_pay = models.FloatField(blank=True, null=True)
    family_deduction = models.FloatField(blank=True, null=True)
    taxable_income  = models.FloatField(blank=True, null=True)
    taxed_income  = models.FloatField(blank=True, null=True)
    PIT_for_13th_salary  = models.FloatField(blank=True, null=True)
    PIT_this_month  = models.FloatField(blank=True, null=True)
    PIT_finalization  = models.FloatField(blank=True, null=True)
    PIT_balance  = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True)
    transfer_bank = models.FloatField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Payroll_Tedis_Vietha(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    newest_salary = models.FloatField(blank=True, null=True)
    working_days = models.FloatField(blank=True, null=True)
    adjust_percent = models.FloatField(blank=True, null=True)
    gross_income = models.FloatField(blank=True, null=True)
    overtime = models.FloatField(blank=True, null=True, default=0)
    transportation = models.FloatField(blank=True, null=True)
    phone = models.FloatField(blank=True, null=True)
    lunch = models.FloatField(blank=True, null=True)
    travel = models.FloatField(blank=True, null=True, default=0)
    responsibility = models.FloatField(blank=True, null=True)
    seniority_bonus = models.FloatField(blank=True, null=True, default=0)
    other = models.FloatField(blank=True, null=True, default=0)
    outstanding_annual_leave = models.FloatField(blank=True, null=True, default=0)
    OTC_incentive = models.FloatField(blank=True, null=True, default=0)
    KPI_achievement = models.FloatField(blank=True, null=True, default=0)
    month_13_salary_Pro_ata = models.FloatField(blank=True, null=True, default=0)
    incentive_last_month = models.FloatField(blank=True, null=True, default=0)
    incentive_last_quy_last_year = models.FloatField(blank=True, null=True, default=0)
    taxable_overtime = models.FloatField(blank=True, null=True, default=0)
    nontaxable_overtime = models.FloatField(blank=True, null=True, default=0)
    SHUI_10point5percent_employee_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_10point5percent_staff_pay = models.FloatField(blank=True, null=True, default=0)
    SHUI_21point5percent_company_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_21point5percent_company_pay = models.FloatField(blank=True, null=True, default=0)
    occupational_accident_and_disease = models.FloatField(blank=True, null=True, default=0)
    trade_union_fee_company_pay = models.FloatField(blank=True, null=True)
    trade_union_fee_employee_pay = models.FloatField(blank=True, null=True)
    family_deduction = models.FloatField(blank=True, null=True)
    taxable_income  = models.FloatField(blank=True, null=True)
    taxed_income  = models.FloatField(blank=True, null=True)
    PIT_13th_salary  = models.FloatField(blank=True, null=True)
    PIT  = models.FloatField(blank=True, null=True)
    PIT_balance  = models.FloatField(blank=True, null=True)
    first_payment  = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True)
    transfer_bank = models.FloatField(blank=True, null=True)
    total_cost = models.FloatField(blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    
    
# Report Payroll Tedis
class Payroll_Marjorie(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    # Exchange rate
    exchange_rate_usd = models.FloatField(blank=True, null=True)
    # Payroll
    salary_usd = models.FloatField(blank=True, null=True)
    salary_vnd = models.FloatField(blank=True, null=True)
    working_days = models.FloatField(blank=True, null=True)
    adjust_percent = models.FloatField(blank=True, null=True)
    gross_income = models.FloatField(blank=True, null=True)
    salary_recuperation = models.FloatField(blank=True, null=True)
    overtime = models.FloatField(blank=True, null=True, default=0)
    transportation = models.FloatField(blank=True, null=True)
    phone = models.FloatField(blank=True, null=True)
    lunch = models.FloatField(blank=True, null=True)
    training_fee = models.FloatField(blank=True, null=True)
    toxic_allowance = models.FloatField(blank=True, null=True)
    travel = models.FloatField(blank=True, null=True, default=0)
    responsibility = models.FloatField(blank=True, null=True)
    seniority_bonus = models.FloatField(blank=True, null=True, default=0)
    other = models.FloatField(blank=True, null=True, default=0)
    total_allowance_recuperation = models.FloatField(blank=True, null=True, default=0)
    benefits = models.FloatField(blank=True, null=True, default=0)
    severance_allowance = models.FloatField(blank=True, null=True, default=0)
    outstanding_annual_leave = models.FloatField(blank=True, null=True, default=0)
    month_13_salary_Pro_ata = models.FloatField(blank=True, null=True, default=0)
    SHUI_10point5percent_employee_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_10point5percent_staff_pay = models.FloatField(blank=True, null=True, default=0)
    SHUI_21point5percent_employer_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_21point5percent_company_pay = models.FloatField(blank=True, null=True, default=0)
    occupational_accident_and_disease = models.FloatField(blank=True, null=True, default=0)
    trade_union_fee_company_pay_2percent = models.FloatField(blank=True, null=True)
    trade_union_fee_member = models.FloatField(blank=True, null=True)
    family_deduction = models.FloatField(blank=True, null=True)
    taxable_income  = models.FloatField(blank=True, null=True)
    taxed_income  = models.FloatField(blank=True, null=True)
    PIT  = models.FloatField(blank=True, null=True)
    deduct  = models.FloatField(blank=True, null=True)
    net_income_vnd  = models.FloatField(blank=True, null=True)
    net_income_usd  = models.FloatField(blank=True, null=True)
    transfer_bank = models.FloatField(blank=True, null=True)
    total_cost_vnd = models.FloatField(blank=True, null=True)
    total_cost_usd = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    
    
class Report_PIT_Payroll_Tedis(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    payroll = models.ForeignKey(Payroll_Tedis, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    # Thu nhập chịu thuế
    thu_nhap_chiu_thue = models.FloatField(blank=True, null=True)
    tong_tnct_khau_tru_thue = models.FloatField(blank=True, null=True)
    bao_hiem_bat_buoc = models.FloatField(blank=True, null=True)
    khau_tru = models.FloatField(blank=True, null=True)
    # Thu nhập tính thuế
    thu_nhap_tinh_thue = models.FloatField(blank=True, null=True)
    thuong = models.FloatField(blank=True, null=True)
    khac = models.FloatField(blank=True, null=True)
    cong = models.FloatField(blank=True, null=True)
    # Others
    thue_tnct_phai_nop = models.FloatField(blank=True, null=True)
    ghi_chu = models.CharField(max_length=500, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Report_TransferHCM_Payroll_Tedis(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    payroll = models.ForeignKey(Payroll_Tedis, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    amount = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Report_Payment_Payroll_Tedis(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    item = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=10, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    paidby = models.CharField(max_length=10, blank=True, null=True)
    paidto = models.CharField(max_length=10, blank=True, null=True)
    account_no = models.TextField(null=True,blank=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


# Report Payroll Tedis-VietHa
class Report_PIT_Payroll_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    payroll = models.ForeignKey(Payroll_Tedis_Vietha, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    # Loại cá nhân
    individual_type = models.CharField(max_length=50, blank=True, null=True)
    # Thu nhập chịu thuế
    thu_nhap_chiu_thue = models.FloatField(blank=True, null=True)
    tong_tnct_khau_tru_thue = models.FloatField(blank=True, null=True)
    bao_hiem_bat_buoc = models.FloatField(blank=True, null=True)
    khau_tru = models.FloatField(blank=True, null=True)
    # Thu nhập tính thuế
    thu_nhap_tinh_thue = models.FloatField(blank=True, null=True)
    thuong = models.FloatField(blank=True, null=True)
    khac = models.FloatField(blank=True, null=True)
    cong = models.FloatField(blank=True, null=True)
    # Others
    thue_tnct_phai_nop = models.FloatField(blank=True, null=True)
    ghi_chu = models.CharField(max_length=500, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Report_Transfer_Payroll_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    payroll = models.ForeignKey(Payroll_Tedis_Vietha, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    amount = models.FloatField(blank=True, null=True)
    # Loại employee
    employee_type = models.CharField(max_length=50, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Report_Payment_Payroll_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    item = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    amount_vnd = models.FloatField(blank=True, null=True)
    amount_euro = models.FloatField(blank=True, null=True)
    paidby = models.CharField(max_length=10, blank=True, null=True)
    paidto = models.CharField(max_length=10, blank=True, null=True)
    account_no = models.TextField(null=True,blank=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Payroll_Ser(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    # Exchange rate
    exchange_rate_usd = models.FloatField(blank=True, null=True)
    exchange_rate_euro = models.FloatField(blank=True, null=True)
    # Payroll
    salary_usd = models.FloatField(blank=True, null=True)
    salary_vnd = models.FloatField(blank=True, null=True)
    working_days = models.FloatField(blank=True, null=True)
    gross_income = models.FloatField(blank=True, null=True)
    salary_recuperation = models.FloatField(blank=True, null=True)
    housing_euro = models.FloatField(blank=True, null=True)
    housing_vnd = models.FloatField(blank=True, null=True)
    phone = models.FloatField(blank=True, null=True)
    lunch = models.FloatField(blank=True, null=True)
    training_fee = models.FloatField(blank=True, null=True)
    toxic_allowance = models.FloatField(blank=True, null=True)
    travel = models.FloatField(blank=True, null=True, default=0)
    responsibility = models.FloatField(blank=True, null=True)
    seniority_bonus = models.FloatField(blank=True, null=True, default=0)
    other = models.FloatField(blank=True, null=True, default=0)
    total_allowance_recuperation = models.FloatField(blank=True, null=True, default=0)
    benefits = models.FloatField(blank=True, null=True, default=0)
    severance_allowance = models.FloatField(blank=True, null=True, default=0)
    outstanding_annual_leave = models.FloatField(blank=True, null=True, default=0)
    month_13_salary_Pro_ata = models.FloatField(blank=True, null=True, default=0)
    SHUI_9point5percent_employee_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_10point5percent_staff_pay = models.FloatField(blank=True, null=True, default=0)
    SHUI_20point5percent_employer_pay = models.FloatField(blank=True, null=True)
    recuperation_of_SHU_Ins_21point5percent_company_pay = models.FloatField(blank=True, null=True, default=0)
    occupational_accident_and_disease = models.FloatField(blank=True, null=True, default=0)
    trade_union_fee_company_pay = models.FloatField(blank=True, null=True)
    trade_union_fee_member = models.FloatField(blank=True, null=True)
    family_deduction = models.FloatField(blank=True, null=True)
    taxable_income  = models.FloatField(blank=True, null=True)
    taxed_income  = models.FloatField(blank=True, null=True)
    PIT  = models.FloatField(blank=True, null=True)
    first_payment_cash_advance_euro  = models.FloatField(blank=True, null=True)
    second_payment_net_income_vnd  = models.FloatField(blank=True, null=True)
    second_payment_net_income_euro  = models.FloatField(blank=True, null=True)
    net_income = models.FloatField(blank=True, null=True)
    total_cost_vnd = models.FloatField(blank=True, null=True)
    total_cost_usd = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    

# Report Infor Payroll Tedis Vietha    
class Report_new_staff_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department_E, on_delete=models.PROTECT, null=True)
    joining_date = models.DateField(max_length=50, null=True)
    gross_salary = models.FloatField(blank=True, null=True)
    allowance = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    dependant_deduction = models.FloatField(blank=True, null=True)
    hospital_for_HI = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=30, blank=True, null=True)
    PIT_code = models.IntegerField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Report_confirmed_after_probation_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department_E, on_delete=models.PROTECT, null=True)
    joining_date = models.DateField(max_length=50, null=True)
    sign_LC_date = models.DateField(max_length=50, null=True)
    allowance = models.FloatField(blank=True, null=True)
    salary_after_probation = models.FloatField(blank=True, null=True)
    SI_book_no = models.CharField(max_length=100, blank=True, null=True)
    hospital_for_HI = models.CharField(max_length=100, blank=True, null=True)    
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    

class Report_resigned_staff_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department_E, on_delete=models.PROTECT, null=True)
    joining_date = models.DateField(max_length=50, null=True)
    leaving_date = models.DateField(max_length=50, null=True)
    allowance = models.FloatField(blank=True, null=True)
    unused_AL = models.FloatField(max_length=200, blank=True, null=True)
    month_13_salary = models.FloatField(blank=True, null=True, default=0)
    severance_allowance = models.FloatField(blank=True, null=True)
    other_allowance = models.FloatField(blank=True, null=True)
    incentive = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    

class Report_other_changes_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    new_salary = models.FloatField(blank=True, null=True, default=0)
    allowance = models.FloatField(blank=True, null=True)
    effective_date = models.DateField(max_length=50, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month


class Report_maternity_leave_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    department = models.ForeignKey(Department_E, on_delete=models.PROTECT, null=True)
    from_date = models.DateField(max_length=50, null=True)
    to_date = models.DateField(max_length=50, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    

class Report_reconcile_Tedis_VietHa(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.month
    

'''Landing'''
class Report_landing_incentive(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    incentive = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=200, blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.period
 
    
class Report_landing_Best_reward(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    best_reward = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.period
    

class Report_landing_month_14_salary(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    month_14_salary = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.period
    

class Report_landing_target_value(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    target_value = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee
    

class Report_landing_achievement(models.Model):
    month = models.ForeignKey(Month_in_period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    achievement = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee
    

class Report_company_celebration_rate(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    celebration = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.year
    

class Report_health_check_up(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    health_check_up_fee = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.year
    

class Report_healthcare_insurance(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    insurance_fee = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee
    

class Report_saving_from_vacant(models.Model):
    period = models.ForeignKey(Period, on_delete=models.PROTECT, null=True)
    # fields
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    saving_from_vacant = models.FloatField(blank=True, null=True)
    # Properties
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __int__(self):
        return self.employee
    


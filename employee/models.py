from turtle import position
from django.db import models
from django.utils.timezone import now

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
    

class Department_area(models.Model):
    department_area = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.department_area
    

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
    

class Job_title(models.Model):
    job_title = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.job_title
    

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
    

class Hi_registered_place(models.Model):
    hi_registered_place = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hi_registered_place


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


class Bo_sung_ho_so(models.Model):
    bo_sung_ho_so = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.bo_sung_ho_so  
    

class Da_nop_thong_tin_nhan_vien(models.Model):
    da_nop_thong_tin_nhan_vien = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.da_nop_thong_tin_nhan_vien  

    
class Employee(models.Model):
    employee_code = models.IntegerField(blank=False) #JOB
    full_name = models.CharField(max_length=100, blank=False) #PERSONAL
    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True) #JOB
    division = models.ForeignKey(Division, on_delete=models.PROTECT, null=True) #JOB
    department_e = models.ForeignKey(Department_E, on_delete=models.PROTECT, null=True) #JOB
    department_v = models.ForeignKey(Department_V, on_delete=models.PROTECT, null=True, blank=True) #JOB
    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True) #JOB
    provinces = models.ForeignKey(Provinces, on_delete=models.PROTECT, null=True, blank=True) #JOB
    gp = models.ForeignKey(Gp, on_delete=models.PROTECT, null=True, blank=True) #JOB
    department_area = models.ForeignKey(Department_area, on_delete=models.PROTECT, null=True) #JOB
    function = models.ForeignKey(Function, on_delete=models.PROTECT, null=True) #JOB
    job_title = models.ForeignKey(Job_title, on_delete=models.PROTECT, null=True) #JOB
    position_e = models.ForeignKey(Position_E, on_delete=models.PROTECT, null=True) #JOB
    position_v = models.ForeignKey(Position_V, on_delete=models.PROTECT, null=True) #JOB
    joining_date = models.DateField(max_length=50, null=True) #JOB
    out_date = models.DateField(max_length=50, null=True, blank=True) #JOB 
    years_of_service = models.CharField(max_length=10, blank=True, null=True) #JOB
    promotion_effective_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    contract_no = models.CharField(max_length=50, blank=True, null=True) #JOB
    contract_type = models.ForeignKey(Contract_type, on_delete=models.PROTECT, null=True, blank=True) #JOB
    signed_contract_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    from_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    to_date = models.DateField(max_length=30, blank=True, null=True) #JOB
    sexual = models.ForeignKey(Sexual, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    date_of_birth = models.DateField(max_length=30, blank=True, null=True) #PERSONAL
    place_of_birth = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    ethic_group = models.ForeignKey(Ethic_group, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    id_card_no = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    issued_date_of_id_card = models.DateField(max_length=30, blank=True, null=True) #PERSONAL
    issued_place_of_id_card = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    permanent_address = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    current_address = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    send_documents_to_address = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    cellphone_no = models.CharField(max_length=20, blank=True, null=True) #PERSONAL
    marital_status = models.ForeignKey(Marital_status, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    company_email = models.CharField(max_length=30, blank=True, null=True) #JOB
    personal_email = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    account_no = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    with_bank = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    branch = models.CharField(max_length=100, blank=True, null=True) #PERSONAL
    certificate_e = models.ForeignKey(Certificate_E, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    certificate_v = models.ForeignKey(Certificate_V, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
    major_e = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    major_v = models.CharField(max_length=30, blank=True, null=True) #PERSONAL
    social_insurrance_book = models.CharField(max_length=50, blank=True, null=True) #PERSONAL
    hi_registered_place = models.ForeignKey(Hi_registered_place, on_delete=models.PROTECT, null=True, blank=True) #PERSONAL
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
    bo_sung_ho_so = models.ForeignKey(Bo_sung_ho_so, on_delete=models.PROTECT, null=True, blank=True) #ANOTHER
    da_nop_thong_tin_nhan_vien = models.ForeignKey(Da_nop_thong_tin_nhan_vien, on_delete=models.PROTECT, null=True, blank=True) #ANOTHER

    def __str__(self):
        return self.full_name


class Employee_children(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    children = models.CharField(max_length=50, blank=True, null=True)
    birthday_of_children = models.DateField(max_length=30, blank=True, null=True)

    def __int__(self):
        return self.employee 
    
class Probationary_period(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    letter_date = models.DateField(max_length=30, blank=True, null=True)
    from_date = models.DateField(max_length=30, blank=True, null=True)
    to_date = models.DateField(max_length=30, blank=True, null=True) 
    monthly_gross_salary = models.IntegerField(blank=True, null=True)
    monthly_allowance = models.IntegerField(blank=True, null=True)

    def __int__(self):
        return self.employee 
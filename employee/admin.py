from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Site)
admin.site.register(Division)
admin.site.register(Department_E)
admin.site.register(Department_V)
admin.site.register(Area)
admin.site.register(Provinces)
admin.site.register(Gp)
admin.site.register(Function)
admin.site.register(Position_E)
admin.site.register(Position_V)
admin.site.register(Abbreviation_Position)
admin.site.register(Contract_category)
admin.site.register(Contract_type)
admin.site.register(Sexual)
admin.site.register(Ethic_group)
admin.site.register(Marital_status)
admin.site.register(Certificate_E)
admin.site.register(Certificate_V)
admin.site.register(University)
admin.site.register(Hi_medical_place)
admin.site.register(Relation_1)
admin.site.register(Relation_2)
admin.site.register(Staff_info_submission)
admin.site.register(Employee)
admin.site.register(Employee_manager)
admin.site.register(Employee_children)
admin.site.register(Probationary_period)
admin.site.register(Employee_contract)
admin.site.register(Employee_promotion)

admin.site.register(Status)
admin.site.register(Type_of_leave)
admin.site.register(Leave_application)
admin.site.register(Overtime_application)

admin.site.register(Period)
admin.site.register(Month_in_period)
admin.site.register(Dayoff)
admin.site.register(Update_dayoff)
admin.site.register(Daily_work)
admin.site.register(Daily_work_for_employee)

admin.site.register(Payroll_Tedis)
admin.site.register(Payroll_Vietha)
admin.site.register(Payroll_Tedis_Vietha)

admin.site.register(Report_PIT_Payroll_Tedis)
admin.site.register(Report_TransferHCM_Payroll_Tedis)
admin.site.register(Report_Payment_Payroll_Tedis)

admin.site.register(Report_PIT_Payroll_Tedis_VietHa)
admin.site.register(Report_Transfer_Payroll_Tedis_VietHa)
admin.site.register(Report_Payment_Payroll_Tedis_VietHa)
admin.site.register(Payroll_Ser)

admin.site.register(Report_new_staff_Tedis_VietHa)
admin.site.register(Report_confirmed_after_probation_Tedis_VietHa)
admin.site.register(Report_resigned_staff_Tedis_VietHa)
admin.site.register(Report_other_changes_Tedis_VietHa)
admin.site.register(Report_maternity_leave_Tedis_VietHa)
admin.site.register(Report_reconcile_Tedis_VietHa)





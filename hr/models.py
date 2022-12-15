from django.db import models
from django.utils.timezone import now
from employee.models import Employee


# User
class Permission(models.Model):
    permission = models.CharField(max_length=10, blank=False, null=True)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.permission


class User(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    user_id = models.IntegerField(blank=False)
    user_name = models.CharField(max_length=20, blank=False)
    user_password = models.CharField(max_length=100, blank=False)
    user_full_name = models.CharField(max_length=300, blank=False)
    user_title = models.CharField(max_length=100, blank=False)
    user_mobile_1 = models.CharField(max_length=20, blank=False)
    user_mobile_2 = models.CharField(max_length=20, blank=False)
    user_email = models.EmailField(max_length=50, blank=False)
    user_active = models.CharField(max_length=10)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, null=True) #JOB
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True, blank=True, default=now)
    updated_by = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return self.user_full_name
    

    
    
# Generated by Django 4.0.5 on 2023-04-10 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0083_employee_contract_travel_support'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payroll_tedis',
            old_name='occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs',
            new_name='occupational_accident_and_disease',
        ),
        migrations.RenameField(
            model_name='payroll_tedis_vietha',
            old_name='occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs',
            new_name='occupational_accident_and_disease',
        ),
        migrations.RenameField(
            model_name='payroll_vietha',
            old_name='occupational_accident_and_disease_Ins_0point5percent_pay_for_staffs',
            new_name='occupational_accident_and_disease',
        ),
        migrations.AlterField(
            model_name='overtime_application',
            name='month',
            field=models.CharField(blank=True, default=4, max_length=5, null=True),
        ),
    ]
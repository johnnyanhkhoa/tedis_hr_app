# Generated by Django 4.0.5 on 2023-10-12 16:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0113_alter_employee_years_of_service_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overtime_application',
            name='month',
            field=models.CharField(blank=True, default=10, max_length=5, null=True),
        ),
        migrations.CreateModel(
            name='Payroll_Marjorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchange_rate_usd', models.FloatField(blank=True, null=True)),
                ('salary_usd', models.FloatField(blank=True, null=True)),
                ('salary_vnd', models.FloatField(blank=True, null=True)),
                ('working_days', models.FloatField(blank=True, null=True)),
                ('adjust_percent', models.FloatField(blank=True, null=True)),
                ('gross_income', models.FloatField(blank=True, null=True)),
                ('salary_recuperation', models.FloatField(blank=True, null=True)),
                ('overtime', models.FloatField(blank=True, default=0, null=True)),
                ('transportation', models.FloatField(blank=True, null=True)),
                ('phone', models.FloatField(blank=True, null=True)),
                ('lunch', models.FloatField(blank=True, null=True)),
                ('training_fee', models.FloatField(blank=True, null=True)),
                ('toxic_allowance', models.FloatField(blank=True, null=True)),
                ('travel', models.FloatField(blank=True, default=0, null=True)),
                ('responsibility', models.FloatField(blank=True, null=True)),
                ('seniority_bonus', models.FloatField(blank=True, default=0, null=True)),
                ('other', models.FloatField(blank=True, default=0, null=True)),
                ('total_allowance_recuperation', models.FloatField(blank=True, default=0, null=True)),
                ('benefits', models.FloatField(blank=True, default=0, null=True)),
                ('severance_allowance', models.FloatField(blank=True, default=0, null=True)),
                ('outstanding_annual_leave', models.FloatField(blank=True, default=0, null=True)),
                ('month_13_salary_Pro_ata', models.FloatField(blank=True, default=0, null=True)),
                ('SHUI_10point5percent_employee_pay', models.FloatField(blank=True, null=True)),
                ('recuperation_of_SHU_Ins_10point5percent_staff_pay', models.FloatField(blank=True, default=0, null=True)),
                ('SHUI_21point5percent_employer_pay', models.FloatField(blank=True, null=True)),
                ('recuperation_of_SHU_Ins_21point5percent_company_pay', models.FloatField(blank=True, default=0, null=True)),
                ('occupational_accident_and_disease', models.FloatField(blank=True, default=0, null=True)),
                ('trade_union_fee_company_pay_2percent', models.FloatField(blank=True, null=True)),
                ('trade_union_fee_member', models.FloatField(blank=True, null=True)),
                ('family_deduction', models.FloatField(blank=True, null=True)),
                ('taxable_income', models.FloatField(blank=True, null=True)),
                ('taxed_income', models.FloatField(blank=True, null=True)),
                ('PIT', models.FloatField(blank=True, null=True)),
                ('deduct', models.FloatField(blank=True, null=True)),
                ('net_income_vnd', models.FloatField(blank=True, null=True)),
                ('net_income_usd', models.FloatField(blank=True, null=True)),
                ('transfer_bank', models.FloatField(blank=True, null=True)),
                ('total_cost_vnd', models.FloatField(blank=True, null=True)),
                ('total_cost_usd', models.FloatField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=500, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee')),
                ('month', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.month_in_period')),
            ],
        ),
    ]

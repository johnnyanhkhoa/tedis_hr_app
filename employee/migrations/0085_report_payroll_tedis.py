# Generated by Django 4.0.5 on 2023-04-14 15:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0084_rename_occupational_accident_and_disease_ins_0point5percent_pay_for_staffs_payroll_tedis_occupationa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_Payroll_Tedis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thu_nhap_chiu_thue', models.FloatField(blank=True, null=True)),
                ('tong_tnct_khau_tru_thue', models.FloatField(blank=True, null=True)),
                ('bao_hiem_bat_buoc', models.FloatField(blank=True, null=True)),
                ('khau_tru', models.FloatField(blank=True, null=True)),
                ('thu_nhap_tinh_thue', models.FloatField(blank=True, null=True)),
                ('thuong', models.FloatField(blank=True, null=True)),
                ('khac', models.FloatField(blank=True, null=True)),
                ('cong', models.FloatField(blank=True, null=True)),
                ('thue_tnct_phai_nop', models.FloatField(blank=True, null=True)),
                ('ghi_chu', models.CharField(blank=True, max_length=500, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee')),
                ('month', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.month_in_period')),
                ('payroll', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.payroll_tedis')),
            ],
        ),
    ]

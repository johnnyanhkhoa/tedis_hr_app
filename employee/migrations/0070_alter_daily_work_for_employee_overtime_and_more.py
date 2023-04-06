# Generated by Django 4.0.5 on 2023-01-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0069_alter_overtime_application_ot_unpaid_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_work_for_employee',
            name='overtime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='daily_work_for_employee',
            name='paid_leave',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='daily_work_for_employee',
            name='unpaid_leave',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

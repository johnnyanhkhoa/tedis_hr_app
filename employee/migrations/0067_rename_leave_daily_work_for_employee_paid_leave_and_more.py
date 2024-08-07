# Generated by Django 4.0.5 on 2023-01-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0066_daily_work_daily_work_for_employee_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='daily_work_for_employee',
            old_name='leave',
            new_name='paid_leave',
        ),
        migrations.AddField(
            model_name='daily_work_for_employee',
            name='unpaid_leave',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

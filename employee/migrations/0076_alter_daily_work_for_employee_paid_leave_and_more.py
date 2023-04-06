# Generated by Django 4.0.5 on 2023-02-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0075_alter_update_dayoff_minus_dayoff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_work_for_employee',
            name='paid_leave',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='daily_work_for_employee',
            name='unpaid_leave',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='overtime_application',
            name='month',
            field=models.CharField(blank=True, default=2, max_length=5, null=True),
        ),
    ]
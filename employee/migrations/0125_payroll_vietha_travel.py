# Generated by Django 4.0.5 on 2024-01-16 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0124_alter_month_in_period_total_work_days_bo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll_vietha',
            name='travel',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]

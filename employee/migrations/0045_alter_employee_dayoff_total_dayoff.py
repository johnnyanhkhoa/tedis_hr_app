# Generated by Django 4.0.5 on 2022-12-08 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0044_alter_employee_manager_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_dayoff',
            name='total_dayoff',
            field=models.IntegerField(blank=True, default=12, null=True),
        ),
    ]

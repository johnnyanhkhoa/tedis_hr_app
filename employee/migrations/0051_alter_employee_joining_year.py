# Generated by Django 4.0.5 on 2022-12-13 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0050_employee_joining_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='joining_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

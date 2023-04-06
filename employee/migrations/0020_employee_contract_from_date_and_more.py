# Generated by Django 4.0.5 on 2022-11-08 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0019_employee_children_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_contract',
            name='from_date',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='employee_contract',
            name='to_date',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
    ]
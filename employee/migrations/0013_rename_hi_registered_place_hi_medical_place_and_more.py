# Generated by Django 4.0.5 on 2022-10-20 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0012_rename_with_bank_employee_bank'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hi_registered_place',
            new_name='Hi_medical_place',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='hi_registered_place',
            new_name='hi_medical_place',
        ),
        migrations.RenameField(
            model_name='hi_medical_place',
            old_name='hi_registered_place',
            new_name='hi_medical_place',
        ),
    ]
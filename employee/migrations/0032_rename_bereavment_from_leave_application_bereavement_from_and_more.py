# Generated by Django 4.0.5 on 2022-11-17 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0031_leave_application_total_days'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave_application',
            old_name='bereavment_from',
            new_name='bereavement_from',
        ),
        migrations.RenameField(
            model_name='leave_application',
            old_name='bereavment_to',
            new_name='bereavement_to',
        ),
    ]

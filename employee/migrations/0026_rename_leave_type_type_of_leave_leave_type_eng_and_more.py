# Generated by Django 4.0.5 on 2022-11-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0025_hour_minute_remove_leave_application_from_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type_of_leave',
            old_name='leave_type',
            new_name='leave_type_eng',
        ),
        migrations.AddField(
            model_name='type_of_leave',
            name='leave_type_vn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

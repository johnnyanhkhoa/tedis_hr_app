# Generated by Django 4.0.5 on 2022-11-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0034_alter_leave_application_total_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave_application',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
# Generated by Django 4.0.5 on 2023-07-06 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0104_alter_leave_application_annual_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave_application',
            name='annual_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='leave_application',
            name='annual_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
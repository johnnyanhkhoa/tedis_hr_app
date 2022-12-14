# Generated by Django 4.0.5 on 2022-11-16 11:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0022_type_of_leave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave_application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_time', models.CharField(blank=True, max_length=20, null=True)),
                ('from_date', models.DateField(blank=True, max_length=30, null=True)),
                ('to_time', models.CharField(blank=True, max_length=20, null=True)),
                ('to_date', models.DateField(blank=True, max_length=30, null=True)),
                ('number_of_leave_days', models.CharField(blank=True, max_length=10, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('application_date', models.DateField(blank=True, max_length=30, null=True)),
                ('approved_date', models.DateField(blank=True, max_length=30, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee')),
                ('leave_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.type_of_leave')),
            ],
        ),
    ]

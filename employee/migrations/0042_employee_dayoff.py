# Generated by Django 4.0.5 on 2022-12-07 11:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0041_alter_leave_application_temporary_replacement_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_dayoff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_dayoff', models.IntegerField(blank=True, null=True)),
                ('used_dayoff', models.IntegerField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee')),
            ],
        ),
    ]
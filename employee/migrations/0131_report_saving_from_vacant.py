# Generated by Django 4.0.5 on 2024-01-31 14:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0130_report_healthcare_insurance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_saving_from_vacant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saving_from_vacant', models.FloatField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee')),
                ('period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.period')),
            ],
        ),
    ]
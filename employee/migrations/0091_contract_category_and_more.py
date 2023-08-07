# Generated by Django 4.0.5 on 2023-05-15 10:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0090_report_pit_payroll_tedis_vietha_individual_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_category', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='employee_contract',
            name='contract_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.contract_category'),
        ),
    ]
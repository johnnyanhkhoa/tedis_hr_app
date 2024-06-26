# Generated by Django 4.0.5 on 2022-12-22 15:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0056_dayoff_remain_recuperation_dayoff_total_recuperation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Update_recuperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plus_recuperation', models.IntegerField(blank=True, null=True)),
                ('minus_recuperation', models.IntegerField(blank=True, null=True)),
                ('reason_of_changing', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('day_off', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.dayoff')),
            ],
        ),
    ]

# Generated by Django 4.0.5 on 2023-01-31 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0073_alter_leave_application_annual_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayoff',
            name='previous_remain_dayoff',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='previous_remain_recuperation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='remain_dayoff',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='remain_recuperation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='total_dayoff',
            field=models.FloatField(blank=True, default=12, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='total_recuperation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='used_dayoff',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dayoff',
            name='used_recuperation',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
# Generated by Django 4.0.5 on 2022-12-13 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0048_period_total_months'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='years_of_service',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

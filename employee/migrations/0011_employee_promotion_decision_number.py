# Generated by Django 4.0.5 on 2022-10-20 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_abbreviation_position_employee_abb_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='promotion_decision_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
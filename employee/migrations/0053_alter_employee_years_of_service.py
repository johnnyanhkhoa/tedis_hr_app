# Generated by Django 4.0.5 on 2022-12-13 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0052_alter_period_period_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='years_of_service',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

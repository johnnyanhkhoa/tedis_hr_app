# Generated by Django 4.0.5 on 2024-01-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0122_remove_report_landing_achievement_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overtime_application',
            name='month',
            field=models.CharField(blank=True, default=1, max_length=5, null=True),
        ),
    ]

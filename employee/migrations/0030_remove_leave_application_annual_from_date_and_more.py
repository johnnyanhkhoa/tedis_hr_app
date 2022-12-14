# Generated by Django 4.0.5 on 2022-11-17 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0029_rename_from_date_leave_application_annual_from_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave_application',
            name='annual_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='annual_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='annual_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='annual_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='annual_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='annual_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='bereavement_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='bereavement_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='bereavement_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='bereavement_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='bereavement_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='bereavement_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='maternity_obstetric_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='maternity_obstetric_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='maternity_obstetric_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='maternity_obstetric_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='maternity_obstetric_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='maternity_obstetric_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='non_paid_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='non_paid_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='non_paid_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='non_paid_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='non_paid_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='non_paid_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='offinlieu_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='offinlieu_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='offinlieu_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='offinlieu_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='offinlieu_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='offinlieu_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='other_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='other_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='other_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='other_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='other_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='other_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='sick_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='sick_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='sick_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='sick_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='sick_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='sick_to_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='wedding_from_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='wedding_from_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='wedding_from_minute',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='wedding_to_date',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='wedding_to_hour',
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='wedding_to_minute',
        ),
        migrations.AddField(
            model_name='leave_application',
            name='annual_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='annual_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='bereavment_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='bereavment_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='maternity_obstetric_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='maternity_obstetric_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='non_paid_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='non_paid_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='ofinlieu_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='ofinlieu_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='other_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='other_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='sick_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='sick_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='wedding_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='leave_application',
            name='wedding_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

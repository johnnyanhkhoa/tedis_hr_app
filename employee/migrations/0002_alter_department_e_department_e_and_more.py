# Generated by Django 4.0.5 on 2022-09-26 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department_e',
            name='department_e',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='division',
            name='division',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='year_of_birth',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='site',
            field=models.CharField(max_length=10, null=True),
        ),
    ]

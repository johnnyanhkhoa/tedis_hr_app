# Generated by Django 4.0.5 on 2022-12-22 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0055_alter_update_dayoff_plus_dayoff'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayoff',
            name='remain_recuperation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayoff',
            name='total_recuperation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayoff',
            name='used_dayoff',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayoff',
            name='used_recuperation',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

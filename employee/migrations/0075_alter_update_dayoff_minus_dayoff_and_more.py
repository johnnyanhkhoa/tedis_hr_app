# Generated by Django 4.0.5 on 2023-01-31 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0074_alter_dayoff_previous_remain_dayoff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update_dayoff',
            name='minus_dayoff',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='update_dayoff',
            name='plus_dayoff',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

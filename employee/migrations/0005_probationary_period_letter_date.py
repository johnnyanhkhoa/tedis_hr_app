# Generated by Django 4.0.5 on 2022-10-17 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_probationary_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='probationary_period',
            name='letter_date',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
    ]

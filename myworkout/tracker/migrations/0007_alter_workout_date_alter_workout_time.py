# Generated by Django 4.2.1 on 2024-01-08 22:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_alter_workout_date_alter_workout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2024, 1, 9), null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(1, 48, 32, 234141), null=True),
        ),
    ]

# Generated by Django 4.2.1 on 2024-01-08 22:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_workout_time_alter_setanothertype_exercise_workout_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2024, 1, 9)),
        ),
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(1, 47, 39, 844122)),
        ),
    ]

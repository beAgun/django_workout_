# Generated by Django 4.2.1 on 2024-01-17 16:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_alter_workout_date_alter_workout_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseworkout',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2024, 1, 17), null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.TimeField(blank=True, default=datetime.time(19, 35, 5, 839769), null=True),
        ),
    ]

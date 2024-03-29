# Generated by Django 4.2.1 on 2024-02-11 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_programcategory_programperiod_workout_day_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='program_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.programcategory'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.program'),
        ),
    ]

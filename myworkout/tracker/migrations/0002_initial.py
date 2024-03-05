# Generated by Django 4.2.1 on 2024-01-22 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workout', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='setweighttraining',
            name='exercise_workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets1', to='tracker.exerciseworkout'),
        ),
        migrations.AddField(
            model_name='setstretching',
            name='exercise_workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets3', to='tracker.exerciseworkout'),
        ),
        migrations.AddField(
            model_name='setcyclingtraining',
            name='exercise_workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets2', to='tracker.exerciseworkout'),
        ),
        migrations.AddField(
            model_name='setanothertype',
            name='exercise_workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets4', to='tracker.exerciseworkout'),
        ),
        migrations.AddField(
            model_name='exerciseworkout',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='workout.exercise'),
        ),
        migrations.AddField(
            model_name='exerciseworkout',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.workout'),
        ),
    ]

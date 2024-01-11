from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DateTimeField
from workout.models import Exercise


# Create your models here.
class Workout(models.Model):
    title = models.CharField(max_length=200, default='Тренировка')
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.now().date())
    time = models.TimeField(blank=True, null=True, default=datetime.now().time())
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=True)
    workout_type = models.ForeignKey(to='WorkoutType', on_delete=models.RESTRICT)

    objects = models.Manager()

    def __str__(self):
        #date = self.date
        #date, time = date.date(), date.time()
        date, time = self.date, self.time
        return f'{self.title}, {date}, {time.hour}:{time.minute}'


class WorkoutType(models.Model):
    title = models.CharField(max_length=200, unique=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'


class ExerciseWorkout(models.Model):
    exercise = models.ForeignKey(to=Exercise, on_delete=models.RESTRICT)
    workout = models.ForeignKey(to='Workout', on_delete=models.CASCADE)

    objects = models.Manager()


class SetWeightTraining(models.Model):
    exercise_workout = models.ForeignKey(to='ExerciseWorkout', on_delete=models.CASCADE,
                                         related_name='sets1')
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reps = models.PositiveSmallIntegerField(blank=True, null=True)
    time = models.DurationField(blank=True, null=True)

    objects = models.Manager()


class SetCyclingTraining(models.Model):
    exercise_workout = models.ForeignKey(to='ExerciseWorkout', on_delete=models.CASCADE,
                                         related_name='sets2')
    distance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    time = models.DurationField(blank=True, null=True)

    objects = models.Manager()


class SetStretching(models.Model):
    exercise_workout = models.ForeignKey(to='ExerciseWorkout', on_delete=models.CASCADE,
                                         related_name='sets3')
    time = models.DurationField(blank=True, null=True)

    objects = models.Manager()


class SetAnotherType(models.Model):
    exercise_workout = models.ForeignKey(to='ExerciseWorkout', on_delete=models.CASCADE,
                                         related_name='sets4')
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    reps = models.PositiveSmallIntegerField(blank=True, null=True)
    time = models.DurationField(blank=True, null=True)
    distance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    objects = models.Manager()

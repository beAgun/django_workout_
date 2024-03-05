from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DateTimeField
from django.urls import reverse, reverse_lazy
from workout.models import Exercise
from django.utils.timezone import now


# Create your models here.
class Workout(models.Model):

    class IsCompound(models.IntegerChoices):
        compound = 1, 'Таблица'
        isolation = 0, 'Сетка'

    title = models.CharField(max_length=100, default='Тренировка')
    description = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    # workout_type = models.ForeignKey(to='WorkoutType', on_delete=models.SET_NULL,
    #                                  null=True,
    #                                  verbose_name='Тип тренировки')
    workout_type = models.CharField(max_length=100, default='Силовая тренировка')
    view = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), IsCompound.choices)),
                               default=True,
                               verbose_name='отображение подходов')
    day_number = models.PositiveSmallIntegerField(blank=True, null=True)
    program = models.ForeignKey(to='Program', on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        date, time = self.date, self.time
        res = f'{self.title}, {date}'
        if time:
            res += f', {time.hour}:{time.minute}'
        return res


class ExerciseWorkout(models.Model):

    exercise = models.ForeignKey(to=Exercise, on_delete=models.RESTRICT)
    workout = models.ForeignKey(to='Workout', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.exercise.name}, {self.workout.id}'


class SetWeightTraining(models.Model):
    exercise_workout = models.ForeignKey(to='ExerciseWorkout', on_delete=models.CASCADE,
                                         related_name='sets1')
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reps = models.PositiveSmallIntegerField(blank=True, null=True)
    time = models.DurationField(blank=True, null=True)
    is_work = models.BooleanField(blank=True, null=True, default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['id']


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


# class WorkoutType(models.Model):
#     title = models.CharField(max_length=200, unique=True)
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return f'{self.title}'


class Program(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    program_category = models.ForeignKey(to='ProgramCategory', on_delete=models.SET_NULL, null=True, blank=True)
    period = models.ForeignKey(to='ProgramPeriod', on_delete=models.RESTRICT)

    def get_absolute_url(self):
        if self.period.id == 1:
            return reverse('tracker:week_program_view', kwargs={'pr_slug': self.slug})
        return reverse('tracker:day_program_view', kwargs={'pr_slug': self.slug})

    def __str__(self):
        return f'{self.title}'


class ProgramCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title}'


class ProgramPeriod(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.title}'



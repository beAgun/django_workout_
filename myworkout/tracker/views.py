from datetime import datetime, timedelta, date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, WeekArchiveView, DetailView

from .forms import AddWorkoutForm
from .models import Workout, WorkoutType, ExerciseWorkout, SetWeightTraining, SetCyclingTraining, SetStretching, \
    SetAnotherType
from workout.models import Exercise


# Create your views here.
class Tracker(TemplateView):
    template_name='tracker/workout_tracker.html'
    week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    extra_context = {'week_days': week_days}


class WorkoutWeekArchiveView(LoginRequiredMixin, WeekArchiveView):

    date_field = "date"
    week_format = "%W"
    allow_future = False

    #week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    #extra_context = {'week_days': week_days}
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        (date_list, items, context) = self.get_dated_items()
        week_days = []
        week_date = context['week']
        for i in range(7):
            week_days += [week_date + timedelta(i)]
        context['week_days'] = week_days

        object_list_by_week_day = [[] for i in range(7)]
        if object_list:
            cnt = 0
            for item in self.object_list:
                cnt += 1
                object_list_by_week_day[item.date.isoweekday() - 1] += [(item, cnt)]

        context['object_list_by_week_day'] = object_list_by_week_day
        print(self.queryset)
        return super().get_context_data(**context)

    def get_queryset(self):
        queryset = Workout.objects.filter(user_id=self.request.user.id).order_by('date')
        return queryset

    # def get_dated_queryset(self, **lookup):
    #     try:
    #         qs = super().get_dated_queryset(**lookup)
    #     except Http404:
    #         print(qs)
    #         return qs


def add_training(req):
    if req.method == 'GET':
        user = req.user
        workout = Workout.objects.create(user_id=user.pk, workout_type=WorkoutType.objects.filter(pk=1))


class UserWorkout(LoginRequiredMixin, DetailView):
    model = Workout
    pk_url_kwarg = 'workout_id'
    context_object_name = 'workout'

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user.pk)

    def get_context_data(self, **kwargs):

        context = {
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']),
        }
        # for i in context['exercise_workout_list']:
        #     print('aa', i.id)
        return super().get_context_data(**context)


class AddWorkout(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = AddWorkoutForm
    template_name = 'workout/add_exercise.html'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        if not w.date:
            w.date = date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])
        if not w.time and w.date == datetime.now().date():
            w.time = datetime.now().time()
        return super().form_valid(form)

    def get_success_url(self):
        print('--------', self.object.id)
        return reverse('tracker:workout', kwargs={'workout_id': self.object.id})


class AddExerciseWorkout(CreateView):
    model = ExerciseWorkout
    fields = 'exercise',
    template_name = 'tracker/add_workout_exercise_form.html'

    def get_context_data(self, **kwargs):
        context = {
            'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']),
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        w = form.save(commit=False)
        w.workout = self.get_context_data().get('workout')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})


class AddSet(CreateView):
    #fields = 'weight', 'reps', 'time'
    template_name = 'tracker/add_set_form.html'

    def get_queryset(self):
        workout_type = Workout.objects.get(id=self.kwargs['workout_id']).workout_type
        if workout_type.id == 1:
            self.fields = 'weight', 'reps', 'time'
            return SetWeightTraining.objects.all()

        elif workout_type.id == 2:
            self.fields = 'time', 'distance'
            return SetCyclingTraining.objects.all()

        elif workout_type.id == 3:
            self.fields = 'time',
            return SetStretching.objects.all()

        elif workout_type.id == 4:
            self.fields = 'weight', 'reps', 'time', 'distance'
            return SetAnotherType.objects.all()

    def get_context_data(self, **kwargs):
        context = {
            'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']),
            'ex_slug': self.kwargs['ex_slug'],
        }

        return super().get_context_data(**context)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})

    def form_valid(self, form):
        w = form.save(commit=False)
        print(self.get_context_data())
        ex_id = Exercise.objects.get(slug=self.kwargs['ex_slug']).id
        w.exercise_workout = self.get_context_data().get('exercise_workout_list').get(exercise_id=ex_id)
        return super().form_valid(form)


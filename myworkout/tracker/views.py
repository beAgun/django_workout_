from datetime import datetime, timedelta, date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, WeekArchiveView, DetailView, UpdateView, DeleteView, ListView

from .forms import AddWorkoutForm, AddExerciseWorkoutForm, AddSetWeightTrainingForm, AddSetCyclingTrainingForm, \
    AddSetStretchingForm, AddSetAnotherTypeForm, UpdateWorkoutForm, UpdateExerciseWorkoutForm, \
    UpdateSetWeightTrainingForm, UpdateSetCyclingTrainingForm, UpdateSetStretchingForm, UpdateSetAnotherTypeForm, \
    CreateProgramForm, AddProgramWorkoutForm
from .models import Workout, ExerciseWorkout, SetWeightTraining, SetCyclingTraining, SetStretching, \
    SetAnotherType, Program, ProgramCategory
from workout.models import Exercise, WorkoutType


class Tracker(TemplateView):
    template_name='tracker/workout_tracker.html'
    week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    extra_context = {'week_days': week_days}


class WorkoutWeekArchiveView(LoginRequiredMixin, WeekArchiveView):

    date_field = "date"
    week_format = "%W"
    allow_future = True

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


class UserWorkout(LoginRequiredMixin, DetailView):
    model = Workout
    pk_url_kwarg = 'workout_id'
    context_object_name = 'workout'

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = {
            'exercise_workout_list':
                ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
        }
        return super().get_context_data(**context)


class UserWorkoutGrid(View):
    pass


def workout_grid_view(req, workout_id):
    workout = Workout.objects.get(user_id=req.user.pk, id=workout_id)
    workout.view = False
    workout.save()
    return redirect('tracker:workout', workout_id)


def workout_table_view(req, workout_id):
    workout = Workout.objects.get(user_id=req.user.pk, id=workout_id)
    workout.view = True
    workout.save()
    return redirect('tracker:workout', workout_id)


class UserPrograms(LoginRequiredMixin, ListView):
    context_object_name = 'programs'

    def get_queryset(self):
        return Program.objects.filter(user=self.request.user)


class WeekProgramView(DetailView):
    model = Program
    slug_url_kwarg = 'pr_slug'
    context_object_name = 'program'
    week_days = [{'week_day':'Понедельник', 'number': 1},
                 {'week_day': 'Вторник', 'number': 2},
                 {'week_day': 'Среда', 'number': 3},
                 {'week_day': 'Четверг', 'number': 4},
                 {'week_day': 'Пятница', 'number': 5},
                 {'week_day': 'Суббота', 'number': 6},
                 {'week_day': 'Воскресенье', 'number': 7},]
    extra_context = {'week_days': week_days}

    def get_context_data(self, **kwargs):
        context = {}
        program = Program.objects.get(slug=self.kwargs['pr_slug'])
        context['program_slug'] = self.kwargs['pr_slug']
        object_list = Workout.objects.filter(program=program)
        object_list_by_week_day = [[] for i in range(7)]
        if object_list:
            cnt = 0
            for item in object_list:
                cnt += 1
                object_list_by_week_day[item.day_number - 1] += [(item, cnt)]

        context['object_list_by_week_day'] = object_list_by_week_day
        return super().get_context_data(**context)


class DayProgramView(DetailView):
    model = Program
    slug_url_kwarg = 'pr_slug'
    context_object_name = 'program'
    template_name = 'tracker/day_program_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        program = Program.objects.get(slug=self.kwargs['pr_slug'])
        context['program_slug'] = self.kwargs['pr_slug']
        training = Workout.objects.filter(program=program)
        if training:
            context['training'] = training[0]
        else:
            context['training'] = None
        return super().get_context_data(**context)

class CreateProgram(LoginRequiredMixin, CreateView):
    model = Program
    form_class = CreateProgramForm
    extra_context = {'subtitle': 'Создание программы'}

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        return super().form_valid(form)


class UpdateProgram(LoginRequiredMixin, UpdateView):
    model = Program
    form_class = CreateProgramForm
    slug_url_kwarg = 'pr_slug'
    extra_context = {'subtitle': 'Редактирование программы'}

    def get_success_url(self):
        return reverse('tracker:user_programs')


class AddWorkout(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = AddWorkoutForm
    template_name = 'tracker/workout_form.html'
    extra_context = {'subtitle': 'Добавление тренировки'}

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        # if not w.date:
        #     w.date = date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])
        w.date = date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])
        # if not w.time and w.date == datetime.now().date():
        #     w.time = datetime.now().time()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.object.id})


class AddProgramWorkout(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = AddProgramWorkoutForm
    template_name = 'tracker/workout_form.html'
    extra_context = {'subtitle': 'Добавление тренировки'}

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        if self.request.GET['period'] == 'week':
            w.day_number = self.request.GET['day']
        w.program = Program.objects.get(slug=self.request.GET['program_slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.object.id})


class UpdateWorkout(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = UpdateWorkoutForm
    pk_url_kwarg = 'workout_id'
    extra_context = {'subtitle': 'Редактирование тренировки'}

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user.pk)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.object.id})

class UpdateProgramWorkout(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = AddProgramWorkoutForm
    pk_url_kwarg = 'workout_id'
    extra_context = {'subtitle': 'Редактирование тренировки'}

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user.pk)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.object.id})


class DeleteWorkout(LoginRequiredMixin, DeleteView):
    model = Workout
    pk_url_kwarg = 'workout_id'
    template_name = 'tracker/workout_delete_confirm.html'
    extra_context = {'subtitle': 'Удаление тренировки'}

    def get_queryset(self):
        return Workout.objects.filter(user_id=self.request.user.pk)

    def get_success_url(self):
        date = self.object.date
        return reverse('tracker:archive_week', kwargs={'year': date.year, 'week': date.isocalendar().week})


class AddExerciseWorkout(LoginRequiredMixin, CreateView):
    # model = ExerciseWorkout
    # fields = 'exercise',
    #form_class = AddExerciseWorkoutForm
    template_name = 'tracker/add_workout_exercise_form.html'
    extra_context = {'subtitle': 'Добавление упражнения'}

    # def get_initial(self):
    #     initial = super(AddExerciseWorkout, self).get_initial()
    #     initial['workout'] = Workout.objects.get(id=self.kwargs['workout_id'])
    #     return initial

    def get_form_class(self):
        workout = Workout.objects.get(id=self.kwargs['workout_id'])
        if workout.user.id != self.request.user.pk:
            raise Http404
        self.extra_context['workout'] = workout
        self.form_class = AddExerciseWorkoutForm
        self.form_class.put_workout(self.form_class, self.kwargs['workout_id'])
        #return form
        return self.form_class

    def get_queryset(self):
        return ExerciseWorkout.objects.select_related('workout')

    def get_context_data(self, **kwargs):
        context = {
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        #workout = self.get_context_data().get('workout')
        workout = self.extra_context['workout']
        w = form.save(commit=False)
        w.workout = workout
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})


class UpdateExerciseWorkout(LoginRequiredMixin, UpdateView):
    model = ExerciseWorkout
    form_class = UpdateExerciseWorkoutForm
    extra_context = {}

    def get_form_class(self):
        workout = Workout.objects.get(id=self.kwargs['workout_id'])
        if workout.user.id != self.request.user.pk:
            raise Http404
        self.extra_context['workout'] = workout
        return super(UpdateExerciseWorkout, self).get_form_class()

    def get_object(self, queryset=None):
        pk = self.request.GET['exerciseworkout_id']
        #self.pk_url_kwarg = self.request.GET['exerciseworkout_id']
        if queryset is None:
            queryset = self.get_queryset()
        try:
            super().get_object()
        except AttributeError:
            queryset = queryset.filter(pk=pk)
            try:
                # Get the single item from the filtered queryset
                obj = queryset.get()
            except queryset.model.DoesNotExist:
                raise Http404(
                    ("No %(verbose_name)s found matching the query")
                    % {"verbose_name": queryset.model._meta.verbose_name}
                )
            return obj


    # def get_queryset(self):
    #     ex = Exercise.objects.get(slug=self.kwargs['ex_slug'])
    #     ex_w = ExerciseWorkout.objects.get(exercise_id=ex.id, workout_id=self.kwargs['workout_id'])
    #     self.pk_url_kwarg = ex_w.id
    #     return ex_w


    def get_context_data(self, **kwargs):
        context = {
            #'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
        }
        return super().get_context_data(**context)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})


class DeleteExerciseWorkout(LoginRequiredMixin, DeleteView):
    model = ExerciseWorkout
    template_name = 'tracker/workout_exercise_confirm_delete.html'
    extra_context = {'subtitle': 'Удаление упражнения'}

    def get_form_class(self):
        workout = Workout.objects.get(id=self.kwargs['workout_id'])
        if workout.user.id != self.request.user.pk:
            raise Http404
        self.extra_context['workout'] = workout
        return super(DeleteExerciseWorkout, self).get_form_class()

    def get_object(self, queryset=None):
        pk = self.request.GET['exerciseworkout_id']
        #self.pk_url_kwarg = self.request.GET['exerciseworkout_id']
        if queryset is None:
            queryset = self.get_queryset()
        try:
            super().get_object()
        except AttributeError:
            queryset = queryset.filter(pk=pk)
            try:
                # Get the single item from the filtered queryset
                obj = queryset.get()
            except queryset.model.DoesNotExist:
                raise Http404(
                    ("No %(verbose_name)s found matching the query")
                    % {"verbose_name": queryset.model._meta.verbose_name}
                )
            return obj

    def get_context_data(self, **kwargs):
        context = {
            #'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
        }
        return super().get_context_data(**context)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})


class AddSet(LoginRequiredMixin, CreateView):
    #fields = 'weight', 'reps', 'time'
    #form_class = AddSetWeightTrainingForm
    template_name = 'tracker/add_set_form.html'
    extra_context = {'subtitle': 'Добавление подхода'}

    def get_form_class(self):
        workout = Workout.objects.get(id=self.kwargs['workout_id'])
        if workout.user.id != self.request.user.pk:
            raise Http404
        self.extra_context['workout'] = workout
        #workout_type = Workout.objects.get(id=self.kwargs['workout_id']).workout_type
        workout_type = Exercise.objects.get(slug=self.kwargs['ex_slug']).workout_type
        if workout_type.id == 1:
            # self.fields = 'weight', 'reps', 'time'
            self.form_class = AddSetWeightTrainingForm

        elif workout_type.id == 2:
            # self.fields = 'time', 'distance'
            self.form_class = AddSetCyclingTrainingForm


        elif workout_type.id == 3:
            # self.fields = 'time',
            self.form_class = AddSetStretchingForm


        elif workout_type.id == 4:
            # self.fields = 'weight', 'reps', 'time', 'distance'
            self.form_class = AddSetAnotherTypeForm

        return self.form_class

    # def get_queryset(self):
    #     workout_type = Workout.objects.get(id=self.kwargs['workout_id']).workout_type
    #     workout_type = Exercise.objects.get(slug=self.kwargs['ex_slug']).workout_type
    #     if workout_type.id == 1:
    #         #self.fields = 'weight', 'reps', 'time'
    #         self.form_class = AddSetWeightTrainingForm
    #         return SetWeightTraining.objects.all()
    #
    #     elif workout_type.id == 2:
    #         #self.fields = 'time', 'distance'
    #         self.form_class = AddSetCyclingTrainingForm
    #         return SetCyclingTraining.objects.all()
    #
    #     elif workout_type.id == 3:
    #         #self.fields = 'time',
    #         self.form_class = AddSetStretchingForm
    #         return SetStretching.objects.all()
    #
    #     elif workout_type.id == 4:
    #         #self.fields = 'weight', 'reps', 'time', 'distance'
    #         self.form_class = AddSetAnotherTypeForm
    #         return SetAnotherType.objects.all()

    def get_context_data(self, **kwargs):
        context = {
            #'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
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


class UpdateSet(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = 'set_id'
    template_name = 'tracker/add_set_form.html'
    extra_context = {'subtitle': 'Редактирование подхода'}

    def get_queryset(self):
        workout = Workout.objects.get(id=self.kwargs['workout_id'])
        if workout.user.id != self.request.user.pk:
            raise Http404
        self.extra_context['workout'] = workout
        #workout_type = Workout.objects.get(id=self.kwargs['workout_id']).workout_type
        workout_type = Exercise.objects.get(slug=self.kwargs['ex_slug']).workout_type
        if workout_type.id == 1:
            #self.fields = 'weight', 'reps', 'time'
            self.form_class = UpdateSetWeightTrainingForm
            return SetWeightTraining.objects.all()

        elif workout_type.id == 2:
            #self.fields = 'time', 'distance'
            self.form_class = UpdateSetCyclingTrainingForm
            return SetCyclingTraining.objects.all()

        elif workout_type.id == 3:
            #self.fields = 'time',
            self.form_class = UpdateSetStretchingForm
            return SetStretching.objects.all()

        elif workout_type.id == 4:
            #self.fields = 'weight', 'reps', 'time', 'distance'
            self.form_class = UpdateSetAnotherTypeForm
            return SetAnotherType.objects.all()

    def get_context_data(self, **kwargs):
        context = {
            #'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
            'ex_slug': self.kwargs['ex_slug'],
        }

        return super().get_context_data(**context)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})


class DeleteSet(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'set_id'
    template_name =  'tracker/set_confirm_delete.html'
    extra_context = {'subtitle': 'Удаление подхода'}

    def get_queryset(self):
        workout = Workout.objects.get(id=self.kwargs['workout_id'])
        if workout.user.id != self.request.user.pk:
            raise Http404
        self.extra_context['workout'] = workout
        #workout_type = Workout.objects.get(id=self.kwargs['workout_id']).workout_type
        workout_type = Exercise.objects.get(slug=self.kwargs['ex_slug']).workout_type
        if workout_type.id == 1:
            #self.fields = 'weight', 'reps', 'time'
            #self.form_class = UpdateSetWeightTrainingForm
            return SetWeightTraining.objects.all()

        elif workout_type.id == 2:
            #self.fields = 'time', 'distance'
            #self.form_class = UpdateSetCyclingTrainingForm
            return SetCyclingTraining.objects.all()

        elif workout_type.id == 3:
            #self.fields = 'time',
            #self.form_class = UpdateSetStretchingForm
            return SetStretching.objects.all()

        elif workout_type.id == 4:
            #self.fields = 'weight', 'reps', 'time', 'distance'
            #self.form_class = UpdateSetAnotherTypeForm
            return SetAnotherType.objects.all()

    def get_context_data(self, **kwargs):
        context = {
            #'workout': Workout.objects.get(id=self.kwargs['workout_id']),
            'exercise_workout_list': ExerciseWorkout.objects.filter(workout_id=self.kwargs['workout_id']).select_related('exercise'),
            'ex_slug': self.kwargs['ex_slug'],
        }

        return super().get_context_data(**context)

    def get_success_url(self):
        return reverse('tracker:workout', kwargs={'workout_id': self.kwargs['workout_id']})


class AddProgramCategory(LoginRequiredMixin, CreateView):
    model = ProgramCategory
    fields = '__all__'
    extra_context = {'subtitle': 'Добавление категории для тренировочных программ'}


class Programs(ListView):
    context_object_name = 'programs'
    template_name = 'tracker/programs.html'

    def get_queryset(self):
        return Program.objects.filter(is_published=True)
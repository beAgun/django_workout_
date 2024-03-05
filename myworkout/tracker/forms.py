from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.forms.utils import ErrorList

from .models import Workout, ExerciseWorkout, SetWeightTraining, SetStretching, SetCyclingTraining, SetAnotherType, Program


class AddWorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ('title', 'workout_type', 'time', 'description', 'view')

        labels = {
            'title': 'Название',
            'workout_type': 'Тип тренировки',
            'date': 'Дата',
            'time': 'Время начала',
            'description': 'Описание',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'date': forms.DateInput(
            #     attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            # ),
            'time': forms.TextInput(
                attrs={'type': 'time', 'placeholder': 'hh-mm-ss', 'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            'workout_type': forms.TextInput(attrs={'placeholder': 'например, силовая', 'class': 'form-control'}),
            'view': forms.Select(attrs={'class': 'form-select'}),
        }


class AddExerciseWorkoutForm(forms.ModelForm):

    class Meta:
        model = ExerciseWorkout
        fields = ('exercise', 'description')
        labels = {
            'exercise': 'Упражнение: ',
            'description': 'Описание:',
        }
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 3, 'cols': 20}),
        }

    def put_workout(self, workout_id=None):
        self.workout_id = workout_id

    def clean_exercise(self):
        exercise = self.cleaned_data['exercise']
        workout_id = self.workout_id
        if workout_id is None:
            return exercise
        lst = ExerciseWorkout.objects.filter(exercise_id=exercise.id, workout_id=workout_id).values('workout_id').annotate(total=Count('workout_id'))
        if lst and lst[0]['total'] == 1:
            raise ValidationError('Такое упражнение уже добавлено!')

        return exercise


class AddSetForm(forms.ModelForm):
    weight = forms.DecimalField(label='вес', min_value=0, step_size=0.25,
                                widget=forms.NumberInput(
                                    attrs={'placeholder': 'кг', 'class': 'form-control',
                                           'style': 'max-width: 5rem; border: 1px solid #dee2e6;'})
                                )
    reps = forms.IntegerField(label='количество повторений', required=False, min_value=1, step_size=1,
                              widget=forms.NumberInput(
                                  attrs={'placeholder': 'повт.', 'class': 'form-control',
                                         'style': 'max-width: 5.5rem; border: 1px solid #dee2e6;'})
                              )
    time = forms.DurationField(label='продолжительность', required=False,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'HH:MM:SS.uu', 'class': 'form-control',
                                          'style': 'max-width: 8.25rem; border: 1px solid #dee2e6;'})
                               )
    distance = forms.DecimalField(label='дистанция', min_value=0, step_size=0.01,
                                  widget=forms.NumberInput(
                                      attrs={'placeholder': 'км', 'class': 'form-control',
                                             'style': 'width: 5rem; border: 1px solid #dee2e6;'})
                                  )
    is_work = forms.BooleanField(label='рабочий', required=False, initial=True,
                                 widget=forms.CheckboxInput(attrs={'placeholder': '',
                                                                   'class': 'form-check-input',
                                                                   'style': ''}))


class AddSetAnotherTypeForm(AddSetForm, forms.ModelForm):

    is_work = None

    class Meta:
        model = SetAnotherType
        fields = ('weight', 'reps', 'time', 'distance', )


class AddSetWeightTrainingForm(AddSetForm, forms.ModelForm):

    distance = None

    class Meta:
        model = SetWeightTraining
        fields = ('weight', 'reps', 'time', 'is_work')


class AddSetStretchingForm(AddSetForm, forms.ModelForm):

    weight = None
    reps = None
    distance = None
    is_work = None

    class Meta:
        model = SetStretching
        fields = ('time',)


class AddSetCyclingTrainingForm(AddSetForm, forms.ModelForm):

    weight = None
    reps = None
    is_work = None

    class Meta:
        model = SetCyclingTraining
        fields = ('time', 'distance')


class UpdateWorkoutForm(forms.ModelForm):
    #date = forms.DateField()
    class Meta:
        model = Workout
        fields = ('title', 'workout_type', 'date', 'time', 'description', 'view')

        labels = {
            'title': 'Название',
            'workout_type': 'Тип тренировки',
            'date': 'Дата',
            'time': 'Время начала',
            'description': 'Описание',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.TextInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'time': forms.TextInput(
                attrs={'type': 'time', 'placeholder': 'hh-mm-ss', 'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            'workout_type': forms.TextInput(attrs={'placeholder': 'например, силовая', 'class': 'form-control'}),
            'view': forms.Select(attrs={'class': 'form-select'})
        }


class UpdateExerciseWorkoutForm(forms.ModelForm):
    class Meta:
        model = ExerciseWorkout
        fields = ('description',)
        labels = {
            'description': 'описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                 'rows': 3, 'cols': 20}),
        }


class UpdateSetForm(forms.ModelForm):
    weight = forms.DecimalField(label='вес', min_value=0, step_size=0.25,
                                widget=forms.NumberInput(
                                    attrs={'placeholder': 'кг', 'class': 'form-control',
                                           'style': 'max-width: 5rem; border: 1px solid #dee2e6;'}
                                ))
    reps = forms.IntegerField(label='количество повторений', required=False, min_value=1, step_size=1,
                              widget=forms.NumberInput(
                                  attrs={'placeholder': 'повт.', 'class': 'form-control',
                                         'style': 'max-width: 5.5rem; border: 1px solid #dee2e6;'}
                              ))
    time = forms.DurationField(label='продолжительность', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'HH:MM:SS.uu', 'class': 'form-control',
               'style': 'max-width: 8.25rem; border: 1px solid #dee2e6;'}
    ))
    distance = forms.DecimalField(label='дистанция', min_value=0, step_size=0.01,
                                  widget=forms.NumberInput(
                                      attrs={'placeholder': 'км', 'class': 'form-control',
                                             'style': 'width: 5rem; border: 1px solid #dee2e6;'}
                                  ))
    is_work = forms.BooleanField(label='рабочий', required=False, initial=True,
                                 widget=forms.CheckboxInput(
                                     attrs={'placeholder': '',
                                            'class': 'form-check-input',
                                            'style': 'max-width: 8.25rem; border: 1px solid #dee2e6;'
                                                     ''}))


class UpdateSetAnotherTypeForm(UpdateSetForm, forms.ModelForm):

    is_work = None

    class Meta:
        model = SetAnotherType
        fields = ('weight', 'reps', 'time', 'distance',)


class UpdateSetWeightTrainingForm(UpdateSetForm, forms.ModelForm):

    distance = None

    class Meta:
        model = SetWeightTraining
        fields = ('weight', 'reps', 'time', 'is_work')


class UpdateSetCyclingTrainingForm(UpdateSetForm, forms.ModelForm):

    weight = None
    reps = None
    is_work = None

    class Meta:
        model = SetCyclingTraining
        fields = ('time', 'distance')


class UpdateSetStretchingForm(UpdateSetForm, forms.ModelForm):

    weight = None
    reps = None
    distance = None
    is_work = None

    class Meta:
        model = SetStretching
        fields = ('time', )


class CreateProgramForm(forms.ModelForm):

    class Meta:
        model = Program
        fields = ('title', 'slug',
                  'program_category', 'period',
                  'description', 'is_published')

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'slug': 'URL',
            'is_published': 'Опубликовать',
            'program_category': 'Категория',
            'period': 'Период',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 86, 'rows': 9, 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'program_category': forms.Select(attrs={'class': 'form-select'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
        }


class AddProgramWorkoutForm(forms.ModelForm):
    day_number = forms.IntegerField(min_value=1, max_value=7, label='Номер тренировочного дня',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Workout
        fields = ('title', 'workout_type', 'day_number', 'description',)

        labels = {
            'title': 'Название',
            'workout_type': 'Тип тренировки',
            'description': 'Описание',
            #'view': 'Представление подходов',
            'day_number': 'Номер тренировочного дня',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'day_number': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={'cols': 86, 'rows': 9, 'class': 'form-control'}),
            'workout_type': forms.TextInput(attrs={'placeholder': 'например, силовая', 'class': 'form-control'}),
            'view': forms.Select(attrs={'class': 'form-select'}),
        }

from django import forms

from .models import Workout, ExerciseWorkout, SetWeightTraining, SetStretching, SetCyclingTraining, SetAnotherType

class AddWorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ('title', 'date', 'time', 'description', 'workout_type')

        #label = {}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            ),
            'time': forms.TextInput(
                attrs={'type': 'time', 'placeholder': 'hh-mm-ss', 'class': 'form-control'}
            ),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            'workout_type': forms.Select(attrs={'class': 'form-control'}),
        }
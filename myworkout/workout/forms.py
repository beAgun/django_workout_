from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Exercise, Equipment, TargetMuscle, ExperienceLevel


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
         'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'sh', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu',
         'я': 'ya', ' ': '-', '/': '-', ',': '', '«': '', '»': '',}

    return "".join(map(lambda x: d[x] if x in d else x, s.lower()))


class AddExerciseForm(forms.ModelForm):
    #name = forms.CharField()
    # equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(),
    #                                   empty_label="Категория не выбрана",
    #                                   label="Категории")

    #is_compound = forms.ModelChoiceField(required=False)
    #slug = forms.SlugField(required=False, default=)

    class Meta:
        model = Exercise
        fields = ['name', 'workout_type', 'image', 'is_compound',
                  'description', 'start', 'performing',
                  'remarks', 'variations', 'additional',
                  'muscle', 'equipment', 'level',]

        #label = {}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start': forms.Textarea(attrs={'class': 'form-control'}),
            'performing': forms.Textarea(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
            'variations': forms.Textarea(attrs={'class': 'form-control'}),
            'additional': forms.Textarea(attrs={'class': 'form-control'}),
            'muscle': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'equipment': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'level': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_compound': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'workout_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError('Длина превышает 50 символов')
        #print(name, slugify(name, allow_unicode=True), Exercise.objects.filter(slug=slugify(name, allow_unicode=True)))
        if Exercise.objects.filter(slug=translit_to_eng(name)):
            raise ValidationError('Такое упражнение в базе уже есть!')

        return name


    # def save(self, *args, **kwargs):
    #     self.cleaned_data['slug'] = slugify(self.cleaned_data['name'])
    #     print(self.cleaned_data['slug'])
    #     super().save(*args, **kwargs)



class CatalogueFilteredForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ['muscle', 'equipment', 'level',
                  'is_compound', ]
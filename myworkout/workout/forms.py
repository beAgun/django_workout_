from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Exercise, Equipment, TargetMuscle, ExperienceLevel


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class AddExerciseForm(forms.ModelForm):
    #name = forms.CharField()
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(),
                                      empty_label="Категория не выбрана",
                                      label="Категории")

    #is_compound = forms.ModelChoiceField(required=False)
    #slug = forms.SlugField(required=False)

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'start', 'performing',
                  'remarks', 'variations', 'additional',
                  'muscle', 'equipment', 'level',
                  'is_compound', 'image', 'slug']

        #label = {}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return name



    # def save(self, *args, **kwargs):
    #     self.fields['slug'] = slugify(self.fields['name'])
    #     super().save(*args, **kwargs)
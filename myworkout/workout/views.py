from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .models import Exercise, TargetMuscle, Equipment, ExperienceLevel
from .forms import AddExerciseForm, CatalogueFilteredForm
from .utils import DataMixin


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
         'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'sh', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu',
         'я': 'ya', ' ': '-', '/': '-', ',': '', '«': '', '»': '',}

    return "".join(map(lambda x: d[x] if x in d else x, s.lower()))


class WorkoutHome(DataMixin, TemplateView):
    template_name = 'workout/index.html'
    title_page = 'Главная'


class Catalogue(DataMixin, ListView):
    #model = Exercise
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    title_page = 'Каталог упражнений'
    cat_selected = 0

    def get_queryset(self):
        return Exercise.objects.all().prefetch_related('muscle').prefetch_related('equipment').prefetch_related('level')


class ShowExercise(DataMixin, DetailView):
    model = Exercise
    template_name = 'workout/exercise.html'
    slug_url_kwarg = 'ex_slug'
    context_object_name = 'ex'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['ex'].name,
                                      muscles=self.object.muscle.all(),
                                      equipments=self.object.equipment.all(),
                                      levels=self.object.level.all(),)


class CatalogueByEquipment(DataMixin, ListView):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    #allow_empty = False

    def get_queryset(self):
        equipment = get_object_or_404(Equipment.objects.filter(slug=self.kwargs['eq_slug']))
        self.extra_context = {
            'title': 'Категория: ' + equipment.name,
            'cat_selected': equipment.slug,
        }
        return equipment.exercises.all()
        #return Exercise.objects.prefetch_related('equipment').filter(slug=self.kwargs['eq_slug'])


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     equipment = Equipment.objects.get(slug=self.kwargs['eq_slug'])
    #     return self.get_mixin_context(context, title='Категория: ' + equipment.name,
    #                                            cat_selected=equipment.slug)


class CatalogueByLevel(DataMixin, ListView):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    #allow_empty = False

    def get_queryset(self):
        level = get_object_or_404(ExperienceLevel.objects.filter(slug=self.kwargs['lvl_slug']))
        self.extra_context = {
            'title': 'Категория: ' + level.name,
            'cat_selected': level.slug,
        }
        return level.levels.all()


class CatalogueByMuscle(DataMixin, ListView):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        muscle_path = self.kwargs['muscle_path']
        muscle_slug = muscle_path.split('/')[-1]

        muscle = get_object_or_404(TargetMuscle.objects.filter(slug=muscle_slug))

        self.extra_context = {
            'title': 'Категория: ' + muscle.name,
            'muscle_selected': muscle,
            'path': muscle_path,
        }
        muscles = list(TargetMuscle.objects.filter(id__in=muscle.get_descendants))
        return Exercise.objects.filter(muscle__in=muscles).distinct()
        #return Exercise.objects.filter(muscle__in=muscle.get_descendants(include_self=True)).distinct()
        #muscle = TargetMuscle.objects.filter(id__in=muscle.get_descendants)


class CatalogueFiltered(ListView, View):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    extra_context = {'form': CatalogueFilteredForm()}

    # def get(self, req):
    #     form = CatalogueFilteredForm()
    #     return render(req, 'workout/add_exercise.html', context=data)

    def post(self, req):
        form = CatalogueFilteredForm(req.POST, req.FILES)
        #print(form.fields)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {
            'menu': menu,
            'title': 'Добавление упражнения',
            'form': form,
        }
        return render(req, 'workout/add_exercise.html', context=data)

    def get_queryset(self):
        muscle_slug = self.request.GET['muscle']
        muscle = get_object_or_404(TargetMuscle.objects.filter(slug=muscle_slug))
        muscles = list(TargetMuscle.objects.filter(id__in=muscle.get_descendants))
        equipment_slug = self.request.GET['equipment']
        level_slug = self.request.GET['level']
        return Exercise.objects.filter(muscle__in=muscles, equipment_slug=equipment_slug, level_slug=level_slug).distinct()



# def add_exercise(req):
#     if req.method == 'POST':
#         form = AddExerciseForm(req.POST, req.FILES)
#         #print(form.fields)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     if req.method == 'GET':
#         form = AddExerciseForm()
#
#     data = {
#         'title': 'Добавление упражнения',
#         'form': form,
#     }
#
#     return render(req, 'workout/add_exercise.html', context=data)


# class AddExercise(View):
#     def get(self, req):
#         form = AddExerciseForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление упражнения',
#             'form': form,
#         }
#         return render(req, 'workout/add_exercise.html', context=data)
#
#     def post(self, req):
#         form = AddExerciseForm(req.POST, req.FILES)
#         #print(form.fields)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {
#             'menu': menu,
#             'title': 'Добавление упражнения',
#             'form': form,
#         }
#         return render(req, 'workout/add_exercise.html', context=data)


class AddExercise(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddExerciseForm
    template_name = 'workout/add_exercise.html'
    title_page = 'Добавление упражнения'
    slug = None
    #login_url = '/admin/'

    def form_valid(self, form):
        ex = form.save(commit=False)
        self.slug = translit_to_eng(form.cleaned_data['name'])
        ex.slug = self.slug
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next', False):
            return self.request.GET['next']
        return reverse('exercise', kwargs={'ex_slug': self.slug})


class EditExercise(DataMixin, UpdateView):
    model = Exercise
    fields = '__all__'
    template_name = 'workout/add_exercise.html'
    # success_url = reverse_lazy('home')
    title_page = 'Редактирование упражнения'
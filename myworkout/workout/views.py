from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .models import Exercise, TargetMuscle, Equipment, ExperienceLevel
from .forms import AddExerciseForm
from .utils import DataMixin


# Create your views here.
# def index(req):
#     data = {
#         'title': 'Главная',
#         'menu': menu,
#     }
#     return render(req, template_name='workout/index.html', context=data)


class WorkoutHome(DataMixin, TemplateView):
    template_name = 'workout/index.html'
    title_page = 'Главная'
    # extra_context = {
    #     'title': 'Главная',
    #     'menu': menu,
    # }


# def show_catalogue(req):
#     exercises = Exercise.objects.all()
#     data = {
#         'title': 'Каталог упражнений',
#         'menu': menu,
#         'exercises': exercises,
#         'cat_selected': 0,
#     }
#     return render(req, template_name='workout/catalogue.html', context=data)


class Catalogue(DataMixin, ListView):
    model = Exercise
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    title_page = 'Каталог упражнений'
    cat_selected = 0


# def show_exercise(req, ex_slug):
#     ex = get_object_or_404(Exercise, slug=ex_slug)
#     data = {
#         'title': ex.name,
#         'menu': menu,
#         'ex': ex,
#         'cat_selected': 1,
#         'muscle': 1,
#         #'categories': categories,
#     }
#     return render(req, template_name='workout/exercise.html', context=data)


class ShowExercise(DataMixin, DetailView):
    model = Exercise
    template_name = 'workout/exercise.html'
    slug_url_kwarg = 'ex_slug'
    context_object_name = 'ex'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['ex'].name)


# def show_category_by_equipment(req, cat_slug):
#     equipment = get_object_or_404(Equipment.objects.filter(slug=cat_slug))
#     exercises = equipment.exercises.all()
#
#     data = {
#         'title': 'Отображение по используемому инвентарю',
#         'menu': menu,
#         'exercises': exercises,
#         'cat_selected': equipment.pk,
#     }
#     return render(req, template_name='workout/catalogue.html', context=data)


class CatalogueByEquipment(DataMixin, ListView):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    #allow_empty = False

    # extra_context = {
    #     'menu': menu,
    # }

    def get_queryset(self):
        equipment = get_object_or_404(Equipment.objects.filter(slug=self.kwargs['eq_slug']))
        return equipment.exercises.all()
        #return Exercise.objects.filter(slug=self.kwargs['cat_slug']).select_related('exercises')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = Equipment.objects.get(slug=self.kwargs['eq_slug'])
        return self.get_mixin_context(context, title='Категория: ' + equipment.name,
                                               cat_selected=equipment.slug)


class CatalogueByLevel(DataMixin, ListView):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'
    #allow_empty = False

    # extra_context = {
    #     'menu': menu,
    # }

    def get_queryset(self):
        level = get_object_or_404(ExperienceLevel.objects.filter(slug=self.kwargs['lvl_slug']))
        return level.levels.all()
        #return Exercise.objects.filter(slug=self.kwargs['cat_slug']).select_related('exercises')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        level = ExperienceLevel.objects.get(slug=self.kwargs['lvl_slug'])
        return self.get_mixin_context(context, title='Категория: ' + level.name,
                                               cat_selected=level.slug)


# def show_muscle(req, muscle_path):
#     print(muscle_path)
#     muscle_slug = muscle_path.split('/')[-1]
#     muscle = get_object_or_404(TargetMuscle.objects.filter(slug=muscle_slug))
#     exercises = Exercise.objects.filter(muscle__in=muscle.get_descendants(include_self=True)).distinct()
#
#     data = {
#         'title': 'Отображение по целевой группе мышц',
#         'menu': menu,
#         'exercises': exercises,
#         'muscle_selected': muscle,
#         'path': muscle_path,
#     }
#     return render(req, template_name='workout/catalogue.html', context=data)


class CatalogueByMuscle(DataMixin, ListView):
    template_name = 'workout/catalogue.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        muscle_slug = self.kwargs['muscle_path'].split('/')[-1]
        muscle = get_object_or_404(TargetMuscle.objects.filter(slug=muscle_slug))
        return Exercise.objects.filter(muscle__in=muscle.get_descendants(include_self=True)).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        muscle_path = self.kwargs['muscle_path']
        muscle_slug = muscle_path.split('/')[-1]
        muscle = TargetMuscle.objects.get(slug=muscle_slug)
        return self.get_mixin_context(context, title='Категория: ' + muscle.name,
                                               muscle_selected=muscle,
                                               path=muscle_path)


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
    # form_class = AddExerciseForm
    model = Exercise
    fields = '__all__'
    template_name = 'workout/add_exercise.html'
    # success_url = reverse_lazy('home')
    title_page = 'Добавление упражнения'
    #login_url = '/admin/'

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


class EditExercise(DataMixin, UpdateView):
    model = Exercise
    fields = '__all__'
    template_name = 'workout/add_exercise.html'
    # success_url = reverse_lazy('home')
    title_page = 'Редактирование упражнения'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkoutHome.as_view(), name='home'),
    path('catalogue/', views.Catalogue.as_view(), name='catalogue'),
    path('exercise/<slug:ex_slug>', views.ShowExercise.as_view(), name='exercise'),
    path('equipment/<slug:eq_slug>', views.CatalogueByEquipment.as_view(), name='equipment'),
    path('level/<slug:lvl_slug>', views.CatalogueByLevel.as_view(), name='level'),
    path('muscle/<path:muscle_path>', views.CatalogueByMuscle.as_view(), name='muscle'),
    path('add_exercise/', views.AddExercise.as_view(), name='add_exercise'),
    path('edit_exercise/<int:pk>/', views.EditExercise.as_view(), name='edit_exercise'),
]


from datetime import datetime
from django.urls import path, reverse_lazy
from . import views

app_name = 'tracker'

current_date = datetime.now()

urlpatterns = [
    path('', views.Tracker.as_view(), name='tracker'),
    path("<int:year>/week/<int:week>/", views.WorkoutWeekArchiveView.as_view(), name="archive_week"),
    path(f'{current_date.year}/week/{current_date.isocalendar().week}/',
         views.WorkoutWeekArchiveView.as_view(), name="archive_week"),
    path('<int:year>/<int:month>/<int:day>/add-workout/', views.AddWorkout.as_view(), name='add_workout'),
    path('workout/<int:workout_id>/', views.UserWorkout.as_view(), name='workout'),
    path('workout/<int:workout_id>/add-exercise/',
         views.AddExerciseWorkout.as_view(), name='add_workout_exercise'),
    path('workout/<int:workout_id>/<slug:ex_slug>/add-set/',
         views.AddSet.as_view(), name='add_set'),
]


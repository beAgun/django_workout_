from datetime import datetime
from django.urls import path
from tracker import views

app_name = 'tracker'

current_date = datetime.now()

urlpatterns = [
    path('', views.Tracker.as_view(), name='tracker'),
    path("<int:year>/week/<int:week>/", views.WorkoutWeekArchiveView.as_view(), name="archive_week"),
    path(f'{current_date.year}/week/{current_date.isocalendar().week}/',
         views.WorkoutWeekArchiveView.as_view(), name="archive_week"),

    path('<int:year>/<int:month>/<int:day>/add-workout/', views.AddWorkout.as_view(), name='add_workout'),
    path('workout/<int:workout_id>/', views.UserWorkout.as_view(), name='workout'),
    path('workout/<int:workout_id>/table/', views.workout_table_view, name='workout_table'),
    path('workout/<int:workout_id>/grid/', views.workout_grid_view, name='workout_grid'),

    path('workout/<int:workout_id>/edit/', views.UpdateWorkout.as_view(), name='edit_workout'),
    path('workout/<int:workout_id>/delete/', views.DeleteWorkout.as_view(), name='delete_workout'),

    path('workout/<int:workout_id>/add-exercise/',
         views.AddExerciseWorkout.as_view(), name='add_workout_exercise'),
    path('workout/<int:workout_id>/edit-exercise/<slug:ex_slug>/',
         views.UpdateExerciseWorkout.as_view(), name='edit_workout_exercise'),
    path('workout/<int:workout_id>/delete-exercise/<slug:ex_slug>/',
         views.DeleteExerciseWorkout.as_view(), name='delete_workout_exercise'),

    path('workout/<int:workout_id>/<slug:ex_slug>/add-set/',
         views.AddSet.as_view(), name='add_set'),
    path('workout/<int:workout_id>/<slug:ex_slug>/edit-set/<int:set_id>/',
         views.UpdateSet.as_view(), name='edit_set'),
    path('workout/<int:workout_id>/<slug:ex_slug>/delete-set/<int:set_id>/',
         views.DeleteSet.as_view(), name='delete_set'),

    path('programs/', views.Programs.as_view(), name='programs'),
    path('user-programs/', views.UserPrograms.as_view(), name='user_programs'),
    path('week-program/<slug:pr_slug>/', views.WeekProgramView.as_view(), name='week_program_view'),
    path('day-program/<slug:pr_slug>/', views.DayProgramView.as_view(), name='day_program_view'),
    path('create-program/', views.CreateProgram.as_view(), name='create_program'),
    path('program/<slug:pr_slug>/edit-program/', views.UpdateProgram.as_view(), name='edit_program'),
    path('add-workout/', views.AddProgramWorkout.as_view(), name='add_workout'),
    path('program-workout/<int:workout_id>/edit/', views.UpdateProgramWorkout.as_view(), name='edit_program_workout'),

    path('add-program-category/', views.AddProgramCategory.as_view(), name='add_program_category')
]


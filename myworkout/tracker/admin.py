from django.contrib import admin
from .models import WorkoutType, Workout, SetWeightTraining, SetCyclingTraining, SetStretching, SetAnotherType

# Register your models here.
admin.site.register(WorkoutType)
admin.site.register(SetWeightTraining)
admin.site.register(SetCyclingTraining)
admin.site.register(SetStretching)
admin.site.register(SetAnotherType)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'date', 'description', 'workout_type')

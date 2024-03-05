from django.contrib import admin
from .models import Workout, SetWeightTraining, SetCyclingTraining, SetStretching, SetAnotherType, Program, ProgramCategory, ProgramPeriod

# Register your models here.
admin.site.register(SetCyclingTraining)
admin.site.register(SetStretching)
admin.site.register(SetAnotherType)
admin.site.register(Program)
admin.site.register(ProgramCategory)


@admin.register(ProgramPeriod)
class ProgramPeriodAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}



@admin.register(SetWeightTraining)
class SetWeightTrainingAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_work', 'weight', 'reps', 'time')
    list_editable = ('is_work',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'date', 'description')

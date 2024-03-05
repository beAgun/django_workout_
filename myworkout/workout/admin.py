from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin
from .models import Exercise, Equipment, ExperienceLevel, TargetMuscle, WorkoutType

# Register your models here.
#admin.site.register(Exercise)


@admin.register(TargetMuscle)
class TargetMuscleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'position', 'parent')
    list_display_links = ('id',)
    list_editable = ('name', 'slug', 'position', 'parent')
    prepopulated_fields = {'slug': ('name',)}


# @admin.register(TargetMuscle)
# class TargetMuscleMPTTModelAdmin(MPTTModelAdmin):
#     list_display = ('name', 'slug', 'position', 'parent')
#     mptt_level_indent = 20
#     prepopulated_fields = {'slug': ('name',)}

@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    #fields = ['id', 'name', 'slug', 'post_image', 'category', 'is_compound']
    list_display = ('id', 'name', 'slug', 'post_image', 'is_compound')
    list_display_links = ('id', 'name')
    list_editable = ('is_compound', 'slug')
    list_per_page = 5
    search_fields = ['name', 'muscle__name']
    list_filter = ['muscle__name', 'is_compound']
    prepopulated_fields = {'slug': ('name', )}
    filter_horizontal = ['muscle']
    save_on_top = True

    @admin.display(description="Изображение")
    def post_image(self, ex: Exercise):
        if ex.image:
            return mark_safe(f"<img src='{ex.image.url}' width=50>")
        return "Без фото"


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ExperienceLevel)
class ExperienceLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


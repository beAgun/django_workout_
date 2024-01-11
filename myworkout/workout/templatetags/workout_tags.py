from django import template
from workout.models import TargetMuscle, Equipment, ExperienceLevel

register = template.Library()


# @register.simple_tag()
# def get_categories():
#     categories = Category.objects.all()
#     return categories
#
#
@register.inclusion_tag('workout/includes/categories_by_equipment.html')
def show_categories_by_equipment(cat_selected=0):
    categories = Equipment.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected}


@register.inclusion_tag('workout/includes/categories_by_experience_level.html')
def show_categories_by_experience_level(cat_selected=0):
    categories = ExperienceLevel.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected}

# @register.inclusion_tag('workout/includes/list_muscles.html')
# def show_muscles(muscle_selected=0):
#     muscles = Muscle.objects.all()
#     return {'muscles': muscles, 'muscle_selected': muscle_selected}


@register.inclusion_tag('workout/includes/list_muscles2.html')
def show_muscles(muscle_selected=0):
    muscles = TargetMuscle.objects.all()
    return {'nodes': muscles, 'muscle_selected': muscle_selected}
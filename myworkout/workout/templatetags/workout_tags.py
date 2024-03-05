from django import template
from django.urls import reverse
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


# @register.inclusion_tag('workout/includes/list_muscles2.html')
# def show_muscles(muscle_selected=0):
#     muscles = TargetMuscle.objects.all()
#     return {'nodes': muscles, 'muscle_selected': muscle_selected}


@register.inclusion_tag('workout/menu_root.html', takes_context=True)
def show_muscles(context, muscle_selected):
    # path_lst = ['']
    # path = 'path' #'menu_item_path_selected'
    # if path in context:
    #     path_lst = context[path].split('/')
    # path_lst.pop()
    muscles = TargetMuscle.objects.all()

    tree = {}
    roots = []
    for i in muscles:
        tree[i.id] = {'id': i.id, 'name': i.name, 'slug': i.slug, 'children': []}

        if i.parent_id is None:
            roots += [i.id]
        else:
            tree[i.parent_id]['children'] += [i.id]

    def rec(node, tree):
        if node in roots:
            tree[node]['path'] = reverse('muscle',
                                         kwargs={'muscle_path': tree[node]['slug']})

        for child in tree[node]['children']:
            tree[child]['path'] = tree[node]['path'] + tree[child]['slug'] + '/'
            tree = rec(child, tree)

        return tree

    for root in roots:
        tree = rec(root, tree)

    if roots == []:
        return {}

    return {'roots': roots, 'tree': tree, 'muscle_selected': muscle_selected}
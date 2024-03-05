from django import template
from django.urls import reverse
from workout.models import TargetMuscle, Equipment, ExperienceLevel

register = template.Library()


@register.inclusion_tag('tracker/sets_table.html', takes_context=True)
def show_sets_table(context, object, type, workout, exercise):
    weight, reps, time, distance = False, False, False, False
    type = context['type']
    sets = []
    cols = len(object)

    for s in object:
        sets += [{'id': s.id, 'weight': None, 'reps': None, 'time': None, 'distance': None, 'is_work': None}]

        if type == 1:
            if s.weight:
                weight = True
                sets[-1]['weight'] = s.weight
            if s.reps:
                reps = True
                sets[-1]['reps'] = s.reps
            sets[-1]['is_work'] = s.is_work

        if s.time:
            time = True
            sets[-1]['time'] = s.time

        if type == 2:
                if s.distance:
                    distance = True
                    sets[-1]['distance'] = s.distance

    return {'weight': weight, 'reps': reps, 'time': time, 'distance': distance,
                'context': context, 'cols_range': range(cols), 'sets': sets,
                'workout': workout, 'exercise': exercise, }
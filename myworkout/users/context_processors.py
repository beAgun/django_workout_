from workout.utils import menu


def get_workout_context(req):
    #menu = menu + [{'name': 'Profile', 'url': 'users:login'}]
    return {'menu': menu}
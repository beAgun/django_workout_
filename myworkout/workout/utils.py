#from myworkout.workout.forms import CatalogueFilteredForm

menu = [
    {'name': 'Главная', 'url': 'home'},
    {'name': 'Каталог упражнений', 'url': 'catalogue'},
    {'name': 'Программы тренировок', 'url': 'tracker:programs'},
    #{'name': 'Блог', 'url': 'home'},
]


class DataMixin:
    paginate_by = 6
    title_page = None
    extra_context = {}
    cat_selected = None

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        #context['form'] = CatalogueFilteredForm
        context.update(kwargs)
        return context

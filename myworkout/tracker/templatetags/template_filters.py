from django import template

register = template.Library()


@register.filter()
def reverse(list):
    return reversed(list)

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = (total_seconds % 3600) % 60
    res = ''
    if hours:
        res += f'{hours} ч '
    if minutes:
        res += f'{minutes} мин '
    if seconds:
        res += f'{seconds} сек '
    return res


@register.filter()
def normalize(num):
    return num.normalize()

@register.filter()
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter()
def get_lst_el(lst, ind):
    return lst[ind]
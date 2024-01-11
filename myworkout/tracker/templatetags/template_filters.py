from django import template

register = template.Library()


@register.filter()
def reverse(list):
    return reversed(list)
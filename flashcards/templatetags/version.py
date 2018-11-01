from django import template

register = template.Library()

@register.filter()
def to_int(value):
    value = value[:-1]
    return int(value)
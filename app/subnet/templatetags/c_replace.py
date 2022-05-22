from django import template

register = template.Library()

@register.filter
def c_replace(value):
    return value.replace(";"," ")
from django import template

register = template.Library()
@register.filter
def ktoc(value):
    return float(value)-273.15

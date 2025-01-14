from django import template

register = template.Library()

@register.filter

def tenge(price):
    return f'${price}'
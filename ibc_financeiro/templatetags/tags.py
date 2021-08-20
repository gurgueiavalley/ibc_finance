from django import template

register = template.Library()

@register.filter(name = 'class')
def className(target): return target.__class__.__name__
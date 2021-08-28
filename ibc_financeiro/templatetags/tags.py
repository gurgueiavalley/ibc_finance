from django import template

register = template.Library()

@register.filter(name = 'class')
def className(target): return target.__class__.__name__

@register.filter()
def column(data): return data[:2].replace(' ', '')

@register.filter()
def icon(data): return data[2:].replace(' ', '').lower()
from django import template

register = template.Library()

@register.filter
def slice4(value):
    return str(value)[:4]
# templatetags/custom_filters.py

from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='custom_date')
def custom_date(value):
    return value.strftime('%d.%m.%Y')
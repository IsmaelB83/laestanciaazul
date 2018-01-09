from django import template
import calendar
import locale

register = template.Library()

@register.filter
def month_name(month_number):
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    return calendar.month_name[month_number]

@register.filter
def month_inverse(month_number):
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    return calendar.month_name[14-month_number]

@register.filter
def month_n_inverse(month_number):
    return int(14-month_number)


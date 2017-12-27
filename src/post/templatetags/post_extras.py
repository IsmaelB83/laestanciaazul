from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

@register.filter
def month_inverse(month_number):
    return calendar.month_name[14-month_number]

@register.filter
def month_n_inverse(month_number):
    return int(14-month_number)


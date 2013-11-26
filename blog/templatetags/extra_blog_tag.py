from django import template
from django.template.defaultfilters import stringfilter

register=template.Library()

@register.filter
@stringfilter
def parse_year(value):
    return int(value.split('/')[0])

@register.filter
@stringfilter
def parse_month(value):
    return int(value.split('/')[1])

@register.filter
def ToString(value):
    return str(value)

##
##register.filter('parse_year', parse_year)
##register.filter('parse_month', parse_month)
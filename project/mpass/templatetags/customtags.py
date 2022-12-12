from django.template import Library

register = Library()


@register.filter
def total_sum(values):
    return sum(values)
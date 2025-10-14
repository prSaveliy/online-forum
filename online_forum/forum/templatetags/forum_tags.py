from django import template

register = template.Library()


@register.filter(name='error_char')
def count_error_char(errors):
    ls = list(errors)
    if not len(ls):
        return None
    return len(ls[0]) > 50
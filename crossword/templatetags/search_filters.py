from django import template
from ..constants import *

register = template.Library()


@register.filter
def language(a, b):
    languages = {'ua': 'Українська', 'en': 'Англійська', 'it': 'Італійська', 'fr': 'Французька', 'pl': 'Польська'}
    return languages[a]

@register.filter
def status(a, b):
    statuses = {'0': 'Відкритий', '1': 'Захищений', '2': 'Приватний'}
    return statuses[a]

@register.filter
def to_cut(a, b):
    if (len(a) > max_crosswords_name_symbols):
        return a[0:max_crosswords_name_symbols - 1] + '...'
    else:
        return a
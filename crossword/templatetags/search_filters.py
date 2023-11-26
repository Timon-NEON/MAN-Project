from django import template

register = template.Library()


@register.filter
def language(a, b):
    languages = {'ua': 'Українська', 'en': 'Англійська', 'it': 'Італійська', 'fr': 'Французька', 'pl': 'Польська'}
    return languages[a]

@register.filter
def status(a, b):
    statuses = {'0': 'Відкритий', '1': 'Захищений', '2': 'Приватний'}
    return statuses[a]
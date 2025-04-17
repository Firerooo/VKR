from django import template

register = template.Library()

@register.filter
def abbr(value):
    mapping = {
        'Рубль': '₽',
        'Доллар США': '$',
        'Евро': '€',
        'Сутки': 'сут.',
        'Месяц': 'мес.',
    }
    if not value:
        return ""
    result = mapping.get(value, value)
    return result.lower()
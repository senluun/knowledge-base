from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Разделяет строку по разделителю"""
    if not value:
        return []
    return value.split(delimiter)

@register.filter
def strip(value):
    """Убирает пробелы в начале и конце строки"""
    if not value:
        return value
    return value.strip()




register = template.Library()

@register.filter
def split(value, delimiter):
    """Разделяет строку по разделителю"""
    if not value:
        return []
    return value.split(delimiter)

@register.filter
def strip(value):
    """Убирает пробелы в начале и конце строки"""
    if not value:
        return value
    return value.strip()


















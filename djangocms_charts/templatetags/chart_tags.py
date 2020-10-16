from django import template

register = template.Library()

@register.filter(is_safe=True)
def clean_json(value):
    return value.replace('"FUNC_START:', '').replace(':FUNC_END"', '')

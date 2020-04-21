from django import template

register = template.Library()


@register.filter
def remove_newlines(cmux: str) -> str:
    return cmux.replace('\n', ' ')

from urllib.parse import urlencode
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, next_page):
    query = context['request'].GET.copy().urlencode()

    if query.startswith('page') or not len(query):
        new_url = f'page={next_page}'
    elif '&page=' in query:
        get_params = query.rpartition('&page=')[0]
        new_url = f'{get_params}&page={next_page}'
    else:
        new_url = f'{query}&page={next_page}'
    return new_url

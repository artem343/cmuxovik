from django import template
import re

register = template.Library()


@register.filter
def shorten_naturaltime(naturaltime):
    try:
        naturaltime = re.sub(r',\s\d+\s\w+', '', naturaltime)
    except TypeError:
        pass
    return naturaltime

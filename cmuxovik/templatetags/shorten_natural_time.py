from django import template
import re

register = template.Library()


@register.filter
def shorten_naturaltime(naturaltime):
    print(naturaltime)
    naturaltime = re.sub(r',\s\d+\s\w+', '', naturaltime)
    return naturaltime

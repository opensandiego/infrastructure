
from infrastructure.cip.models import *
from django import template
from django.core.urlresolvers import *
import urllib

register = template.Library()
@register.inclusion_tag('shortcuts.haml')
def show_shortcuts():
    """docstring for generate_shortcuts"""
    shortcuts = []
    phase_links = { 'links' : [], 'title': 'Current Projects by phase' }
    for (key, value) in PROJECT_PHASES:
        link = {}
        link['url'] = reverse("projects_filter_list",kwargs={'filter':"phase", 'value':urllib.unquote(value)})
        link['name'] = value
        link['key'] = key
        phase_links['links'].append(link)
    shortcuts.append(phase_links)
    return {'shortcuts': shortcuts}

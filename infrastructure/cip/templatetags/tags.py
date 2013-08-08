
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
        phase_links['links'].append(generate_link('phase',key,value))
    shortcuts.append(phase_links)
    asset_group_links = { 'links' : [], 'title': 'Current Projects by asset type group' }
    for (key, value) in ASSET_TYPE_GROUPS:
        asset_group_links['links'].append(generate_link('asset_group',key,value))
    shortcuts.append(asset_group_links)
    client_departement_links = { 'links' : [], 'title': 'Current Projects by asset type group' }
    for (key, value) in CLIENT_DEPARTMENTS:
        client_departement_links['links'].append(generate_link('client_departement',key,value))
    shortcuts.append(client_departement_links)

    return {'shortcuts': shortcuts}

def generate_link(type,key,value):
    """docstring for generate_link"""
    link = {}
    link['url'] = reverse("projects_filter_list",kwargs={'filter':type, 'value':iri_to_uri(re.sub(r"[\(\)-]"," ",value))})
    link['name'] = value
    link['key'] = key
    return link

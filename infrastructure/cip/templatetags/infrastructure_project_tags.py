
from infrastructure.cip.models import *
from django import template
from django.core.urlresolvers import *
import urllib

register = template.Library()
phase = {
        'Design' : 'design',
        'Construction' : 'construction',
        'Post Construction' : 'post-construction',
        'Planning' : 'planning',
        'Bid and Award' : 'bid',
        'Complete' : 'complete'
        }
asset_type = {
        'Buildings': 'commercial',
        'Airports' : 'airport',
        'Storm Water Drainage' : 'telephone',
        'Parks' : 'park2',
        'Transportation' : 'bus',
        'Sewer' : 'wetland',
        'Water' : 'water',
        }
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

@register.inclusion_tag('project_list_item.haml')
def project_list_item(project):
    """docstring for project_list_item"""
    project_link_path = reverse('project_detail', args=[project.id] )
    asset_type_image = "images/icons/%s-18.png" % asset_type[project.SP_ASSET_TYPE_GROUP] 
    return { 'project' : project, 'link': project_link_path, 'phase': phase[project.SP_PROJECT_PHASE], 'asset_type_image': asset_type_image }

@register.inclusion_tag('pagination.haml',takes_context=True)
def pagination(context):
    """docstring for pagination"""
    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj']
        }
@register.inclusion_tag('pagination_count.haml', takes_context=True)
def pagination_count(context):
    """docstring for pagination_count"""
    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj']
        }

@register.inclusion_tag('filter_text.haml', takes_context=True)
def filter_text(context):
    """docstring for filter_text"""
    filter =  context["filter"]
    filter_text = ""
    if filter.has_key("asset_type"):
        filter_text = filter_text + " {0}".format(filter['asset_type'])
    filter_text = filter_text + " Projects"
    if filter.has_key("phase"):
        filter_text = filter_text + " in {0} Phase".format(filter['phase'])
    
    filter_text = filter_text + " ordered by {0}".format(filter['order'])
    return {'filter_text': filter_text}

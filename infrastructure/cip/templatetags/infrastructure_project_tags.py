
from infrastructure.cip.models import *
from django import template
from django.core.urlresolvers import *
import urllib
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter    
def subtract(value, arg):
    return value - arg
phase_class = {
        'Design' : 'design',
        'Construction' : 'construction',
        'Post Construction' : 'post-construction',
        'Planning' : 'planning',
        'Bid and Award' : 'bid',
        'Complete' : 'completed'
        }
phase_images = {
        'Design' : '234_brush',
        'Construction' : '430_construction_cone',
        'Post Construction' : '331_dashboard',
        'Planning' : '335_pushpin',
        'Bid and Award' : '458_money',
        'Complete' : '206_ok_2'
        }
asset_type_class = {
        'Buildings': 'buildings',
        'Airports' : 'airport',
        'Storm Water Drainage' : 'storm-water-drainage ',
        'Parks' : 'parks',
        'Transportation' : 'transportation',
        'Sewer' : 'sewer',
        'Water' : 'water'
        }

asset_type_images = {
        'Buildings': 'commercial',
        'Airports' : 'airport',
        'Storm Water Drainage' : 'telephone',
        'Parks' : 'park2',
        'Transportation' : 'bus',
        'Sewer' : 'wetland',
        'Water' : 'water'
        }
@register.filter(needs_autoescape=True)
def intword_span(value,autoescape=None):
    """docstring for intword_span"""
    if value < 1000000:
        return value
    intword = value.split(" ")
    money = intword[0]
    money_type = intword[1]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    money_string = "{0} <span>{1}</span>".format(esc(money),esc(money_type))
    return mark_safe(money_string)
    
@register.inclusion_tag('shortcuts.haml')
def show_shortcuts():
    """docstring for generate_shortcuts"""
    shortcuts = []
    phase_links = { 'links' : [], 'title': 'Phase' }
    for (key, value) in PHASE_URLS:
        phase_links['links'].append(generate_link('phase',key,value,phase_class[value]))
    shortcuts.append(phase_links)
    asset_group_links = { 'links' : [], 'title': 'Asset Type' }
    for (key, value) in ASSET_TYPE_URLS:
        asset_group_links['links'].append(generate_link('asset_type',key,value, asset_type_class[value]))
    shortcuts.append(asset_group_links)
    district_links = { 'links' : [], 'title': 'Disricts' }
    for district_nr in range(1,10):
        district_links['links'].append(generate_link('district',district_nr,'District {0}'.format(district_nr),''))
    shortcuts.append(district_links)
    #client_departement_links = { 'links' : [], 'title': 'Current Projects by asset type group' }

    return {'shortcuts': shortcuts}

def generate_link(type,key,value,image_class):
    """docstring for generate_link"""
    link = {}
    link['url'] = reverse("{0}_projects".format(type),kwargs={type: key})
    link['name'] = value
    link['key'] = key
    link['image_class'] = image_class
    return link

@register.inclusion_tag('project_list_item.haml')
def project_list_item(project):
    """docstring for project_list_item"""
    project_link_path = reverse('project_detail', args=[project.id] )
    asset_type_image = "images/icons/%s-18.png" % asset_type_images[project.SP_ASSET_TYPE_GROUP] 
    return { 'project' : project, 'link': project_link_path, 'phase': phase_class[project.SP_PROJECT_PHASE], 'asset_type_image': asset_type_image }

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

@register.inclusion_tag('widgets.haml', takes_context=True)
def widgets(context):
    """docstring for widgets"""
    return context

@register.inclusion_tag('no_results.haml')
def no_results():
    """docstring for no_results"""
    return

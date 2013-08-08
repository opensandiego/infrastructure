# Create your views here.
import datetime
from django.shortcuts import render_to_response, render
from django.db.models import Q
from infrastructure.cip.models import *
from django import forms
from django_select2 import *
from django.core.urlresolvers import *
import inspect
from django.views.generic import ListView, DetailView

def index(request):
    """docstring for projects"""
    projects = Project.objects.all()
    department_needs = DepartmentNeed.objects.all()
    return render_to_response('index.haml', {'projects': projects, 'department_needs': department_needs})

def projects():
    """docstring for projects"""
    
def filter_projects(request):
    """docstring for filter_projects"""
    if request.POST:
        form = ProjectFilterForm(request.POST)
        form.is_valid()
        projects = ProjectFilter(form).filter()
    else:
        form = ProjectFilterForm()
    return render(request, 'projects.haml', {'projects': projects, 'form': form })
    
def show_project(request, p_id):
    """docstring for show_project"""
    project = Project.objects.get(id= p_id)
    
    return render_to_response('project.haml', {'project': project})

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project.haml'
    context_object_name = 'project'
    
class ProjectList(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects.haml'
    #paginate_by = 10

    def timephase(self):
        """docstring for timephase"""
        if self.kwargs.has_key('show'):
            if self.kwargs['show'] == "all":
                return Project.objects.all()
            elif self.kwargs['show'] == "current":
                return Project.objects.current()
            else:
                return Project.objects.all()
        else:
            return Project.objects.current()
    def post(self, request, *args, **kwargs):
        form = ProjectFilterForm(self.request.POST)
        form.is_valid()
        projects =  ProjectFilter(form).filter()
        kwargs['object_list'] = projects
        context = super(ProjectList, self).get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)
        
    def get_queryset(self):
        """docstring for get_queryset"""
        if self.kwargs.has_key('filter') and self.kwargs.has_key('value'):
            self.filter = self.kwargs['filter']
            self.filter_value = self.kwargs['value']
            projects = self.timephase() 
            return getattr(projects, 'by_{format}'.format(format=self.filter))(self.filter_value)
        else:
            return self.timephase() 

        
    def get_context_data(self, **kwargs):
        """docstring for get_contxt_data"""
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['form'] = ProjectFilterForm()
        return context

class ProjectFilter:
    def __init__(self, form):
        self.form = form
        if self.form.cleaned_data['dataset'] == 'current':
            self.projects = Project.objects.current()
        else:
            self.projects = Project.objects.all()
        self.order =  self.form.cleaned_data['order'] 
    def filter(self):
        """docstring for  filter_data"""
        if self.form.cleaned_data.has_key('phases') and self.form.cleaned_data['phases']:
            self.phases()
        if self.form.cleaned_data.has_key('asset_types') and self.form.cleaned_data['asset_types']:
            self.asset_types()
        if self.form.cleaned_data.has_key('type_choices') and self.form.cleaned_data['type_choices']:
            self.asset_groups()
        if self.form.cleaned_data.has_key('delivery_methods') and self.form.cleaned_data['delivery_methods']:
            self.delivery_methods()
        if self.form.cleaned_data.has_key('client_departements') and self.form.cleaned_data['client_departements']:
            self.client_departements()
        return self.projects

    def phases(self):
        """docstring for phases"""
        phase = self.form.cleaned_data['phases']
        phases = dict(PROJECT_PHASES)
        self.projects = self.projects.by_phase(phases[phase]).order_by(self.order)
    def asset_types(self):
        """docstring for asset_types"""
        asset_type = self.form.cleaned_data['asset_types']
        asset_types = dict(ASSET_TYPE_GROUPS)
        self.projects = self.projects.by_asset_group(asset_types[asset_type]).order_by(self.order)
    def asset_groups(self):
        """docstring for asset_types"""
        asset_group = self.form.cleaned_data['type_choices']
        asset_groups = dict(ASSET_TYPE_CHOICES)
        self.projects = self.projects.by_asset_group(asset_groups[asset_group]).order_by(self.order)
    def delivery_methods(self):
        """docstring for asset_types"""
        delivery_method = self.form.cleaned_data['delivery_methods']
        delivery_methods = dict(DELIVERY_METHODS)
        self.projects = self.projects.by_delivery_method(delivery_methods[delivery_method]).order_by(self.order)
    def client_departements(self):
        """docstring for asset_types"""
        client_departement = self.form.cleaned_data['client_departements']
        client_departements = dict(CLIENT_DEPARTMENTS)
        self.projects = self.projects.by_client_departement(client_departements[client_departement]).order_by(self.order)

class ProjectFilterForm(forms.Form):
    default = [(u'', 'All')]
    choice_phases = tuple(default + list(PROJECT_PHASES))
    choice_assets = tuple(default + list(ASSET_TYPE_GROUPS))
    choice_type_choices = tuple(default + list(ASSET_TYPE_CHOICES))
    choice_delivery_methods = tuple(default + list(DELIVERY_METHODS))
    choice_client_departements = tuple(default + list(CLIENT_DEPARTMENTS))

    dataset = Select2ChoiceField(initial=2,
        choices=(('all','All'),('current','Active')),required=False)
    order = Select2ChoiceField(initial=2,
        choices=(('SP_AWARD_START_DT', 'Award Start'),('SP_CONSTR_FINISH_DT','construction finish'),('SP_TOTAL_PROJECT_COST','construction cost')),required=False)
    phases = Select2ChoiceField(initial=2,
        choices=choice_phases,required=False)
    asset_types = Select2ChoiceField(initial=2,
        choices=choice_assets,required=False)
    type_choices = Select2ChoiceField(initial=2,
        choices=choice_type_choices,required=False)
    client_departements = Select2ChoiceField(initial=2,
        choices=choice_client_departements,required=False)
    delivery_methods = Select2ChoiceField(initial=2,
        choices=choice_delivery_methods,required=False)


import datetime
from django.shortcuts import render_to_response, render
from django.db.models import Q
from infrastructure.cip.models import *
from django import forms
from django_select2 import *
from django.core.urlresolvers import *
import inspect
from django.views.generic import ListView, DetailView, TemplateView
import json
import django.http
from django.db.models import Count, Min, Sum, Avg
from django.contrib.humanize.templatetags.humanize import intword
from infrastructure.cip.templatetags.infrastructure_project_tags import intword_span

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

class DashboardWidget():
    headline = ''
    value = ''
    widget_class = ''
    def __init__(self,headline):
        """docstring for __init__"""
        self.headline = headline
    def set_value(self,value):
        """docstring for set_value"""
        self.value = value

class DashboardMixin(object):
    projects = Project.objects.all().aggregate(overall_project_cost=Sum('SP_TOTAL_PROJECT_COST'),overall_construction_cost=Sum('SP_TOTAL_CONSTRUCTION_COST'),projects_count=Count('pk'))
    current_projects = Project.objects.current()
    this_years_projects = Project.objects.by_year()
    widgets = []
    def __init__(self):
        """docstring for init"""
        self.this_year = datetime.date.today().year
        self.widgets = []
        self.active_project_count = self.current_projects.count()
        self.project_cost = self.projects['overall_project_cost']
        self.construction_cost = self.projects['overall_construction_cost']
        self.finished_this_year = self.this_years_projects.by_finished_date(datetime.date(self.this_year,12,31))
    def get_widgets(self):
        """docstring for get_widgets"""
        project_count = DashboardWidget('projects')
        project_count.value = self.projects['projects_count']

        active_project_count = DashboardWidget('active projects')
        active_project_count.value = self.active_project_count

        project_cost = DashboardWidget('$$$')
        project_cost.value = intword_span(intword(self.project_cost))

        construction_cost = DashboardWidget('construction \n $$$')
        construction_cost.value = intword_span(intword(self.construction_cost))

        years_project = DashboardWidget('projects started in {0}'.format(self.this_year))
        years_project.value = self.this_years_projects.count()

        years_finished = DashboardWidget('projects finished in {0}'.format(self.this_year))
        years_finished.value = self.finished_this_year.count()
        row_widgets = []
        row_widgets.append(project_count)
        row_widgets.append(active_project_count)
        row_widgets.append(project_cost)
        row_widgets.append(construction_cost)
        row_widgets.append(years_project)
        row_widgets.append(years_finished)
        self.widgets.append({'title': '', 'row': row_widgets})
        row_widgets = []
        for (phase_class,phase) in PHASE_URLS:
            phase_widget = DashboardWidget(phase)
            phase_widget.value = Project.objects.all().by_phase(phase).count()
            phase_widget.widget_class = phase_class
            row_widgets.append(phase_widget)
        self.widgets.append({'title': 'Projects by Phase:', 'row': row_widgets})
        row_widgets = []
        for (asset_type_class,asset_type) in ASSET_TYPE_URLS:
            asset_widget = DashboardWidget(asset_type)
            asset_widget.value = Project.objects.all().by_asset_group(asset_type).count()
            row_widgets.append(asset_widget)

        self.widgets.append({'title': 'Projects by Asset Type:', 'row': row_widgets})
        return self.widgets
    def get_context_data(self, **kwargs):
        context = super(DashboardMixin, self).get_context_data(**kwargs)
        context['widgets'] = self.get_widgets()
        return context

class DashboardView(DashboardMixin,TemplateView):
    template_name = 'dashboard.haml'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project.haml'
    context_object_name = 'project'

class ProjectList(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects.haml'
    paginate_by = 20

    def timephase(self):
        """docstring for timephase"""
        self.show = {'current': 'active', 'all': ''}
        projects = Project.objects.all()
        if self.kwargs.has_key('show'):
            if self.kwargs['show'] == "current":
                self.show['current'] = 'active'
                self.show['all'] = ''
                projects = Project.objects.current()
            elif self.kwargs['show'] == 'all':
                self.show['current'] = ''
                self.show['all'] = 'active'
                projects = Project.objects.all()
        return projects.order_by('SP_PRELIM_ENGR_START_DT').exclude(SP_PRELIM_ENGR_START_DT=None)
    def get_queryset(self):
        """docstring for get_queryset"""
        if self.kwargs.has_key('phase'):
            self.show = {'current': '', 'all': 'active'}
            projects = self.timephase().order_by(PHASE_ORDERS[self.kwargs['phase']])
            return projects.by_phase(dict(PHASE_URLS)[self.kwargs['phase']])
        if self.kwargs.has_key('asset_type'):
            self.show = {'current': '', 'all': 'active'}
            projects = self.timephase().order_by('SP_CONSTR_FINISH_DT')
            return projects.by_asset_group(dict(ASSET_TYPE_URLS)[self.kwargs['asset_type']])

        if self.kwargs.has_key('filter') and self.kwargs.has_key('value'):
            self.filter = self.kwargs['filter']
            self.filter_value = self.kwargs['value']
            projects = self.timephase().order_by('SP_CONSTR_FINISH_DT')
            return getattr(projects, 'by_{format}'.format(format=self.filter))(self.filter_value)
        else:
            return self.timephase() 

    def get_context_data(self, **kwargs):
        """docstring for get_contxt_data"""
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['form'] = ProjectFilterForm()
        context['show'] = self.show
        return context

class ProjectsListListView(ProjectList):
    template_name = 'project_list.haml'
    paginate_by = 10
    def get(self, request, *args, **kwargs):  
        form = ProjectFilterForm(self.request.GET)
        if form.is_valid():
            pf = ProjectFilter(form)
            projects =  pf.filter()
        kwargs['object_list'] = projects
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['filter'] = pf.filter_set
        return render(request, self.template_name, context)
 
class ProjectFilter:
    def __init__(self, form):
        self.form = form
        if self.form.cleaned_data['dataset'] == 'current':
            self.projects = Project.objects.current()
        else:
            self.projects = Project.objects.all()
        self.order =  self.form.cleaned_data['order'] 
        self.filter_set = { 'order': dict(ORDER)[self.order] }
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
        if self.form.cleaned_data.has_key('project_cost') and self.form.cleaned_data['project_cost']:
            self.project_cost()
        return self.projects.order_by(self.order).exclude(**{self.order.replace('-',''): None})

    def phases(self):
        """docstring for phases"""
        phase = self.form.cleaned_data['phases']
        phases = dict(PROJECT_PHASES)
        self.filter_set['phase'] = phases[phase]
        self.projects = self.projects.by_phase(phases[phase])
    def asset_types(self):
        """docstring for asset_types"""
        asset_type = self.form.cleaned_data['asset_types']
        asset_types = dict(ASSET_TYPE_GROUPS)
        self.filter_set['asset_type'] = asset_types[asset_type]
        self.projects = self.projects.by_asset_group(asset_types[asset_type])
    def asset_groups(self):
        """docstring for asset_types"""
        asset_group = self.form.cleaned_data['type_choices']
        asset_groups = dict(ASSET_TYPE_CHOICES)
        self.projects = self.projects.by_asset_group(asset_groups[asset_group])
    def delivery_methods(self):
        """docstring for asset_types"""
        delivery_method = self.form.cleaned_data['delivery_methods']
        delivery_methods = dict(DELIVERY_METHODS)
        self.projects = self.projects.by_delivery_method(delivery_methods[delivery_method])
    def client_departements(self):
        """docstring for asset_types"""
        client_departement = self.form.cleaned_data['client_departements']
        client_departements = dict(CLIENT_DEPARTMENTS)
        self.projects = self.projects.by_client_departement(client_departements[client_departement])
    def project_cost(self):
        """docstring for project_cost"""
        project_cost = self.form.cleaned_data['project_cost']
        self.projects = self.projects.by_project_cost(ProjectCosts().get_value(int(project_cost)))

class ProjectFilterForm(forms.Form):
    default = [(u'', 'All')]
    choice_phases = tuple(default + list(PROJECT_PHASES))
    choice_assets = tuple(default + list(ASSET_TYPE_GROUPS))
    choice_type_choices = tuple(default + list(ASSET_TYPE_CHOICES))
    choice_delivery_methods = tuple(default + list(DELIVERY_METHODS))
    choice_client_departements = tuple(default + list(CLIENT_DEPARTMENTS))
    project_costs = tuple(default + ProjectCosts().get_touples())

    dataset = Select2ChoiceField(initial=2,
        choices=(('all','All'),('current','Active')),required=False)
    order = Select2ChoiceField(initial=2,
        choices=(ORDER),required=False)
    project_cost = Select2ChoiceField(
        choices=project_costs, required=False)
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

class JSONTimetableMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return django.http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        project = context["project"]
        json_response = {
                "timeline": {
                "headline":"Project Timeline",
                "type":"default",
                "text":"<p></p>",
                "date": []
                }
            }
        if project.SP_PRELIM_ENGR_START_DT and project.SP_PRELIM_ENGR_FINISH_DT:
            json_response["timeline"]["date"].append({
                        "startDate":project.SP_PRELIM_ENGR_START_DT.strftime("%Y,%m,%d"),
                        "endDate":project.SP_PRELIM_ENGR_FINISH_DT.strftime("%Y,%m,%d"),
                        "headline":"Planning Phase",
                    })
        if project.SP_DESIGN_INITIATION_START_DT and project.SP_DESIGN_FINISH_DT:
            json_response["timeline"]["date"].append({
                        "startDate":project.SP_DESIGN_INITIATION_START_DT.strftime("%Y,%m,%d"),
                        "endDate":project.SP_DESIGN_FINISH_DT.strftime("%Y,%m,%d"),
                        "headline":"Design Phase",
                    })
        if project.SP_BID_START_DT and project.SP_BID_FINISH_DT:
            json_response["timeline"]["date"].append({
                        "startDate":project.SP_BID_START_DT.strftime("%Y,%m,%d"),
                        "endDate":project.SP_BID_FINISH_DT.strftime("%Y,%m,%d"),
                        "headline":"Bid Phase",
                    })
        if project.SP_AWARD_START_DT and project.SP_AWARD_FINISH_DT:
            json_response["timeline"]["date"].append({
                        "startDate":project.SP_AWARD_START_DT.strftime("%Y,%m,%d"),
                        "endDate":project.SP_AWARD_FINISH_DT.strftime("%Y,%m,%d"),
                        "headline":"Award Phase",
                    })
        if project.SP_CONSTRUCTION_START_DT and project.SP_CONSTR_FINISH_DT:
            json_response["timeline"]["date"].append({
                        "startDate":project.SP_CONSTRUCTION_START_DT.strftime("%Y,%m,%d"),
                        "endDate":project.SP_CONSTR_FINISH_DT.strftime("%Y,%m,%d"),
                        "headline":"Construction Phase",
                    })
        if project.SP_CONSTR_FINISH_DT and project.SP_NOC_DT:
            json_response["timeline"]["date"].append({
                        "startDate":project.SP_CONSTR_FINISH_DT.strftime("%Y,%m,%d"),
                        "endDate":project.SP_NOC_DT.strftime("%Y,%m,%d"),
                        "headline":"Post-Construction Phase",
                    })
        return json.dumps(json_response)
class ProjectDetailJSONView(JSONTimetableMixin, ProjectDetailView):
    pass

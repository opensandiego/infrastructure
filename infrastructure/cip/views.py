# Create your views here.
import datetime
from django.shortcuts import render_to_response
from django.db.models import Q
from infrastructure.cip.models import Project, DepartmentNeed
def index(request):
    """docstring for projects"""
    projects = Project.objects.all()
    department_needs = DepartmentNeed.objects.all()
    return render_to_response('index.haml', {'projects': projects, 'department_needs': department_needs})

def projects(request,filter ='', value= ''):
    """docstring for projects"""
    if filter != "":
        if filter == "phase":
            filter_q = Q(SP_PROJECT_PHASE__icontains=value)
            projects = Project.objects.filter(filter_q & current_project_q()).order_by('SP_CONSTR_FINISH_DT')
        elif filter == "asset_group":
            filter_q = Q(SP_ASSET_TYPE_GROUP=value)
            projects = Project.objects.filter(filter_q & current_project_q()).order_by('SP_CONSTR_FINISH_DT')
    else:
        projects = Project.objects.filter(current_project_q()).order_by('SP_CONSTR_FINISH_DT')
    return render_to_response('projects.haml', {'projects': projects})

def current_project_q():
    return Q(SP_CONSTR_FINISH_DT__gt=datetime.date(2013, 8, 1), SP_AWARD_START_DT__lt=datetime.date(2013, 8, 1))
def show_project(request, p_id):
    """docstring for show_project"""
    project = Project.objects.get(id= p_id)
    
    return render_to_response('project.haml', {'project': project})

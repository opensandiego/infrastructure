# Create your views here.
from django.shortcuts import render_to_response
from infrastructure.cip.models import Project, DepartmentNeed
def index(request):
    """docstring for projects"""
    projects = Project.objects.all()
    department_needs = DepartmentNeed.objects.all()
    return render_to_response('index.haml', {'projects': projects, 'department_needs': department_needs})

def projects(request):
    """docstring for projects"""
    projects = Project.objects.all()
    return render_to_response('projects.haml', {'projects': projects})

def show_project(request, p_id):
    """docstring for show_project"""
    project = Project.objects.get(id= p_id)
    
    return render_to_response('project.haml', {'project': project})

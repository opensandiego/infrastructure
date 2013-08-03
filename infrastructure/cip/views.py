# Create your views here.
import datetime
from django.shortcuts import render_to_response, render
from django.db.models import Q
from infrastructure.cip.models import *
from django import forms
from django_select2 import *

def index(request):
    """docstring for projects"""
    projects = Project.objects.all()
    department_needs = DepartmentNeed.objects.all()
    return render_to_response('index.haml', {'projects': projects, 'department_needs': department_needs})

def projects(request,filter ='', value= '',show= 'current'):
    """docstring for projects"""
    if show == "all":
        projects = Project.objects.all
    else:
        projects = Project.objects.current()
    if filter != "":
        if filter == "phase":
            if value == "planning":
                projects = Project.objects.future()
            projects = projects.by_phase(value)
        elif filter == "asset_group":
            project = projects.by_asset_group(value)
    if request.POST:
        form = InitialValueForm(request.POST)
        form.is_valid()
    else:
        form = InitialValueForm()
    return render(request, 'projects.haml', {'projects': projects, 'form': form })

def show_project(request, p_id):
    """docstring for show_project"""
    project = Project.objects.get(id= p_id)
    
    return render_to_response('project.haml', {'project': project})

class InitialValueForm(forms.Form):
    departments = Select2ChoiceField(initial=2,
        choices=PROJECT_PHASES)

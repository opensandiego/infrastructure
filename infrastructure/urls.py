from django.conf.urls import patterns, include, url
from infrastructure.cip.views import *
from django.contrib import admin
from django.http import HttpResponseRedirect
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'infrastructure.views.home', name='home'),
    # url(r'^infrastructure/', include('infrastructure.foo.urls')),
    url(r'^$',ProjectList.as_view()), 
    url(r'^projects$',ProjectList.as_view(), name='projects_list'),
    url(r'^projects/(?P<filter>\w+([\w_])*)/(?P<value>\w+([\/\w \.-?%?&]*))$', ProjectList.as_view(), name='projects_filter_list'),
    url(r'^projects/(?P<filter>\w+)/(?P<value>\w+(\s+\w+)*)/(?P<show>(all|current))$', ProjectList.as_view(), name='projects_list'),
    url(r'^projects/filter$', ProjectList.as_view(), name='filter_projects'),
    url(r'^projects_list$', ProjectsListListView.as_view(), name='projects_list'),

    url(r'^project/(?P<pk>\d+)$', ProjectDetailView.as_view(),name='project_detail'),
    url(r'^admin/', include(admin.site.urls)),
)

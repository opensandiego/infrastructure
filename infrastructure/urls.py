from django.conf.urls import patterns, include, url
from infrastructure.cip.views import ProjectList
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('infrastructure.cip.views',
    # Examples:
    # url(r'^$', 'infrastructure.views.home', name='home'),
    # url(r'^infrastructure/', include('infrastructure.foo.urls')),
    url(r'^$', 'index'),
    url(r'^projects$',ProjectList.as_view()),
    url(r'^projects/(?P<filter>\w+)/(?P<value>\w+(\s+\w+)*)$', ProjectList.as_view(), name='projects_list'),
    url(r'^projects/(?P<filter>\w+)/(?P<value>\w+(\s+\w+)*)/(?P<show>(all|current))$', 'projects'),
    url(r'^projects/filter$', 'filter_projects'),

    url(r'^project/(\d+)/$','show_project', name='show_project'),
    url(r'^admin/', include(admin.site.urls)),
)

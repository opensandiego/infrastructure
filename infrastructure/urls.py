from django.conf.urls import patterns, include, url

from infrastructure.cip.views import index, projects, show_project
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'infrastructure.views.home', name='home'),
    # url(r'^infrastructure/', include('infrastructure.foo.urls')),
    url(r'^$', index),
    url(r'^projects$', projects),
    url(r'^project/(\d+)/$',show_project),
    url(r'^admin/', include(admin.site.urls)),
)

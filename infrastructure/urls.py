from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('infrastructure.cip.views',
    # Examples:
    # url(r'^$', 'infrastructure.views.home', name='home'),
    # url(r'^infrastructure/', include('infrastructure.foo.urls')),
    url(r'^$', 'index'),
    url(r'^projects$', 'projects'),
    url(r'^projects/(?P<filter>\w+)/(?P<value>\w+(\s+\w+)*)$', 'projects'),

    url(r'^project/(\d+)/$','show_project'),
    url(r'^admin/', include(admin.site.urls)),
)

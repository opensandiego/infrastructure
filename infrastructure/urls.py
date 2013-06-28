from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'infrastructure.views.home', name='home'),
    # url(r'^infrastructure/', include('infrastructure.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

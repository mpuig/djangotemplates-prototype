from django.conf.urls.defaults import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Forward all URLs to django-prototyping
    url(r'^([^/]*)$', 'prototyping.views.process', kwargs=dict(
            title=u'Django prototype templates',
            extra_context={'website_name': 'Testing'}
    ))
)

urlpatterns += staticfiles_urlpatterns()
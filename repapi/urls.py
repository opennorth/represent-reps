from django.conf.urls.defaults import patterns, include, url

from repapi.views import *

urlpatterns = patterns('',
    url('^representative/$', RepresentativeListView.as_view()),
    url('^(?P<district>boundary/[\w_-]+/[\w_-]+/)representatives/', RepresentativeListView.as_view()),
)

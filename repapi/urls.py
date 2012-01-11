from django.conf.urls.defaults import patterns, include, url

from repapi.views import *

urlpatterns = patterns('',
    url('^representatives/$', RepresentativeListView.as_view()),
    url('^(?P<district>boundaries/[\w_-]+/[\w_-]+/)representatives/', RepresentativeListView.as_view()),
)

from django.conf.urls.defaults import patterns, include, url

from representatives.views import *

urlpatterns = patterns('',
    url(r'^representatives/$', RepresentativeListView.as_view()),
    url(r'^representatives/(?P<set_slug>[\w_-]+)/$', RepresentativeListView.as_view(), name='representatives_representative_list'),
    url(r'^boundaries/(?P<district>[\w_-]+/[\w_-]+)/representatives/', RepresentativeListView.as_view()),
    url(r'^representative-sets/$', RepresentativeSetListView.as_view()),
    url(r'^representative-sets/(?P<slug>[\w_-]+)/$', RepresentativeSetDetailView.as_view(),
        name='representatives_representative_set_detail'),
)

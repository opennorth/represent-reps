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

urlpatterns += patterns('',
    url(r'^candidates/$', CandidateListView.as_view()),
    url(r'^candidates/(?P<set_slug>[\w_-]+)/$', CandidateListView.as_view(), name='representatives_candidate_list'),
    url(r'^boundaries/(?P<district>[\w_-]+/[\w_-]+)/candidates/$', CandidateListView.as_view()),
    url(r'^candidate-sets/$', CandidateSetListView.as_view()),
    url(r'^candidate-sets/(?P<slug>[\w_-]+)/$', CandidateSetDetailView.as_view(),
        name='representatives_candidate_set_detail'),
)

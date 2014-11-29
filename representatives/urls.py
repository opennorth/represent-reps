from django.conf.urls import patterns, url

from representatives.models import app_settings
from representatives.views import (
    RepresentativeSetListView, RepresentativeSetDetailView, RepresentativeListView,
    ElectionListView, ElectionDetailView, CandidateListView)

urlpatterns = patterns('',
    url(r'^representatives/$', RepresentativeListView.as_view()),
    url(r'^representatives/(?P<set_slug>[\w_-]+)/$', RepresentativeListView.as_view(), name='representatives_representative_list'),
    url(r'^boundaries/(?P<slug>[\w_-]+/[\w_-]+)/representatives/', RepresentativeListView.as_view()),
    url(r'^representative-sets/$', RepresentativeSetListView.as_view()),
    url(r'^representative-sets/(?P<slug>[\w_-]+)/$', RepresentativeSetDetailView.as_view(),
        name='representatives_representative_set_detail'),
)

if app_settings.ENABLE_CANDIDATES:
    urlpatterns += patterns('',
        url(r'^candidates/$', CandidateListView.as_view()),
        url(r'^candidates/(?P<set_slug>[\w_-]+)/$', CandidateListView.as_view(), name='representatives_candidate_list'),
        url(r'^boundaries/(?P<slug>[\w_-]+/[\w_-]+)/candidates/$', CandidateListView.as_view()),
        url(r'^elections/$', ElectionListView.as_view()),
        url(r'^elections/(?P<slug>[\w_-]+)/$', ElectionDetailView.as_view(),
            name='representatives_election_detail'),
    )

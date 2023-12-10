from django.urls import path, re_path

from representatives.models import app_settings
from representatives.views import (
    RepresentativeSetListView, RepresentativeSetDetailView, RepresentativeListView,
    ElectionListView, ElectionDetailView, CandidateListView)

urlpatterns = [
    path('representatives/', RepresentativeListView.as_view()),
    re_path(r'^representatives/(?P<set_slug>[\w_-]+)/$', RepresentativeListView.as_view(), name='representatives_representative_list'),
    re_path(r'^boundaries/(?P<slug>[\w_-]+/[\w_-]+)/representatives/', RepresentativeListView.as_view()),
    path('representative-sets/', RepresentativeSetListView.as_view()),
    re_path(r'^representative-sets/(?P<slug>[\w_-]+)/$', RepresentativeSetDetailView.as_view(),
        name='representatives_representative_set_detail'),
]

if app_settings.ENABLE_CANDIDATES:
    urlpatterns += [
        path('candidates/', CandidateListView.as_view()),
        re_path(r'^candidates/(?P<set_slug>[\w_-]+)/$', CandidateListView.as_view(), name='representatives_candidate_list'),
        re_path(r'^boundaries/(?P<slug>[\w_-]+/[\w_-]+)/candidates/$', CandidateListView.as_view()),
        path('elections/', ElectionListView.as_view()),
        re_path(r'^elections/(?P<slug>[\w_-]+)/$', ElectionDetailView.as_view(),
            name='representatives_election_detail'),
    ]

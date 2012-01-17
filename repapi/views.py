import urllib2, urllib

from django.utils import simplejson as json

from boundaryservice.base_views import ModelListView, ModelDetailView

from repapi.models import Representative, RepresentativeSet, app_settings

class RepresentativeListView(ModelListView):

    model = Representative

    def get_qs(self, request, district=None):
        qs = super(RepresentativeListView, self).get_qs(request)
        if district:
            qs = qs.filter(boundary_url='/' + district)
        return qs

    def filter(self, request, qs):
        qs = super(RepresentativeListView, self).filter(request, qs)

        if 'districts' in request.GET:
            qs = qs.filter(boundary_url__in=['/boundaries/' + d for d in request.GET['districts'].split(',')])

        if 'point' in request.GET:
            # Figure out the boundaries for that point via the boundaryservice API
            request_url = app_settings.BOUNDARYSERVICE_URL \
                        + 'boundaries/?' + urllib.urlencode({'contains': request.GET['point']})
            resp = urllib2.urlopen(request_url)
            data = json.load(resp)
            boundaries = [ o['url'] for o in data['objects'] ]
            qs = qs.filter(boundary_url__in=boundaries)

        return qs

class RepresentativeSetListView(ModelListView):
    pass
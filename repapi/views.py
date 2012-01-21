import urllib2, urllib

from django.utils import simplejson as json

from boundaryservice.base_views import ModelListView, ModelDetailView
from boundaryservice.models import Boundary

from repapi.models import Representative, RepresentativeSet, app_settings

# Oh dear! We're monkey-patching Boundary.as_dict
def boundary_related_decorator(target):
    def inner(self):
        r = target(self)
        r['related']['representatives_url'] = self.get_absolute_url() + 'representatives/'
        return r
    return inner
Boundary.as_dict = boundary_related_decorator(Boundary.as_dict)

class RepresentativeListView(ModelListView):

    model = Representative
    filterable_fields = ('name', 'first_name', 'last_name', 'district_name', 'elected_office', 'party_name')

    def get_qs(self, request, district=None, set_slug=None):
        qs = super(RepresentativeListView, self).get_qs(request)
        if district:
            qs = qs.filter(boundary_url='/' + district)
        elif set_slug:
            qs = qs.filter(representative_set__slug=set_slug)
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

    model = RepresentativeSet

    def get_qs(self, request):
        qs = super(RepresentativeSetListView, self).get_qs(request)
        return qs.select_related('representative_set')

class RepresentativeSetDetailView(ModelDetailView):

    model = RepresentativeSet

    def get_object(self, request, qs, slug):
        return qs.get(slug=slug)
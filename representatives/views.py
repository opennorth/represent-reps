import json
import re
from urllib.parse import urlencode
from urllib.request import urlopen

from boundaries.base_views import BadRequest, ModelDetailView, ModelListView
from boundaries.models import Boundary

from representatives.models import (
    Candidate,
    Election,
    Representative,
    RepresentativeSet,
    app_settings,
)
from representatives.utils import boundary_url_to_name


# Oh dear! We're monkey-patching Boundary.as_dict
def boundary_related_decorator(target):
    def decorate(self):
        boundary = target(self)
        boundary['related']['representatives_url'] = self.get_absolute_url() + 'representatives/'
        return boundary

    return decorate


Boundary.as_dict = boundary_related_decorator(Boundary.as_dict)


class RepresentativeListView(ModelListView):
    model = Representative
    filterable_fields = ('name', 'first_name', 'last_name', 'gender', 'district_name', 'elected_office', 'party_name')

    def get_qs(self, request, slug=None, set_slug=None):
        qs = super().get_qs(request)
        if slug:
            qs = qs.filter(boundary=slug)
        elif set_slug:
            qs = qs.filter(**{self.model.set_name + '__slug': set_slug})
        return qs.select_related(self.model.set_name)

    def filter(self, request, qs):
        qs = super().filter(request, qs)

        if 'districts' in request.GET:
            qs = qs.filter(boundary__in=request.GET['districts'].split(','))

        if 'point' in request.GET:
            if app_settings.RESOLVE_POINT_REQUESTS_OVER_HTTP:
                url = app_settings.BOUNDARYSERVICE_URL + 'boundaries/?' + urlencode({'contains': request.GET['point']})
                boundaries = [boundary_url_to_name(boundary['url']) for boundary in json.loads(urlopen(url).read().decode())['objects']]
            else:
                try:
                    latitude, longitude = re.sub(r'[^\d.,-]', '', request.GET['point']).split(',')
                    wkt = 'POINT({} {})'.format(longitude, latitude)
                    boundaries = Boundary.objects.filter(shape__contains=wkt).values_list('set_id', 'slug')
                except ValueError:
                    raise BadRequest("Invalid latitude,longitude '%s' provided." % request.GET['point'])
                boundaries = ['/'.join(boundary) for boundary in boundaries]
            qs = qs.filter(boundary__in=boundaries)

        return qs


class RepresentativeSetListView(ModelListView):
    model = RepresentativeSet

    def get_qs(self, request):
        qs = super().get_qs(request)
        return qs.filter(enabled=True)


class RepresentativeSetDetailView(ModelDetailView):
    model = RepresentativeSet

    def get_object(self, request, qs, slug):
        return qs.get(slug=slug)


class CandidateListView(RepresentativeListView):
    model = Candidate
    filterable_fields = RepresentativeListView.filterable_fields + ('incumbent',)


class ElectionListView(RepresentativeSetListView):
    model = Election


class ElectionDetailView(RepresentativeSetDetailView):
    model = Election

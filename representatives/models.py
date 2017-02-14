# coding: utf-8
import datetime
import json
import logging
import re
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import urlopen

from appconf import AppConf
# @see https://docs.djangoproject.com/en/1.10/ref/urlresolvers/ Django 1.10
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.template.defaultfilters import slugify
from jsonfield import JSONField

from representatives.utils import boundary_url_to_name

logger = logging.getLogger(__name__)


class MyAppConf(AppConf):
    BOUNDARYSERVICE_URL = 'https://represent.opennorth.ca/'

    # If False, makes a direct database query on the Boundary model for
    # ?point=lat,lng queries. If True, makes an HTTP request to BOUNDARYSERVICE_URL
    RESOLVE_POINT_REQUESTS_OVER_HTTP = False

    # Set to true (in REPRESENT_ENABLE_CANDIDATES in settings.py) to enable
    # Candidate and Election endpoints.
    ENABLE_CANDIDATES = False
    # If an update is triggered 5 or more days after the election date, disable
    # the Election.
    DISABLE_CANDIDATES_AFTER_ELECTION = 5


app_settings = MyAppConf()


class BaseRepresentativeSet(models.Model):
    name = models.CharField(max_length=300,
        help_text="The name of the political body, e.g. House of Commons",
        unique=True)
    data_url = models.URLField(help_text="URL to a JSON array of individuals within this set")
    data_about_url = models.URLField(blank=True, help_text="URL to information about the scraper used to gather data")
    last_import_time = models.DateTimeField(blank=True, null=True)
    last_import_successful = models.NullBooleanField(blank=True, null=True)
    boundary_set = models.CharField(max_length=300, blank=True,
        help_text="Name of the boundary set on the boundaries API, e.g. federal-electoral-districts")
    slug = models.SlugField(max_length=300, unique=True, db_index=True)
    enabled = models.BooleanField(default=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(BaseRepresentativeSet, self).save(*args, **kwargs)

    @property
    def boundary_set_url(self):
        return '/boundary-sets/%s/' % self.boundary_set if self.boundary_set else ''

    @property
    def boundaries_url(self):
        return '/boundaries/%s/' % self.boundary_set if self.boundary_set else ''

    def as_dict(self):
        return {
            'name': self.name,
            'url': self.get_absolute_url(),
            'data_url': self.data_url,
            'data_about_url': self.data_about_url,
            'related': {
                'boundary_set_url': self.boundary_set_url,
                'boundaries_url': self.boundaries_url,
            }
        }

    @staticmethod
    def get_dicts(sets):
        return [s.as_dict() for s in sets]

    def get_absolute_url(self):
        raise NotImplementedError

    def get_list_of_boundaries(self):
        if not self.boundary_set:
            return {}
        set_url = app_settings.BOUNDARYSERVICE_URL + 'boundaries/' + self.boundary_set + '/?limit=0'
        boundaries = []
        while set_url:
            set_data = json.loads(urlopen(set_url).read().decode())
            boundaries.extend(set_data['objects'])
            if set_data['meta'].get('next'):
                set_url = urljoin(app_settings.BOUNDARYSERVICE_URL, set_data['meta']['next'])
            else:
                return boundaries

    def create_child(self):
        """Should create an unsaved instance of a Candidate or Representative
        object belonging to this set."""
        raise NotImplementedError

    @transaction.atomic
    def update_from_data_source(self):
        data = json.loads(urlopen(self.data_url).read().decode())

        if not (isinstance(data, list) and data):  # No data
            self.last_import_successful = False
            self.save()
            return False

        # Delete existing data
        self.individuals.all().delete()

        boundaries = self.get_list_of_boundaries()
        boundary_names = dict((
            (get_comparison_string(b['name']), b['url']) for b in boundaries
        ))
        boundary_ids = dict((
            (b.get('external_id'), b['url']) for b in boundaries
        ))
        url_to_name = dict((
            (b['url'], b['name']) for b in boundaries
        ))
        url_to_id = dict((
            (b['url'], b.get('external_id')) for b in boundaries
        ))

        for source_rep in data:
            rep = self.create_child()
            for fieldname in ('name', 'district_name', 'elected_office',
                    'source_url', 'first_name', 'last_name', 'party_name',
                    'email', 'url', 'personal_url', 'photo_url', 'district_id',
                    'gender'):
                if source_rep.get(fieldname) is not None:
                    setattr(rep, fieldname, source_rep[fieldname])
            for json_fieldname in ('offices', 'extra'):
                if source_rep.get(json_fieldname):
                    try:
                        setattr(rep, json_fieldname, json.loads(source_rep.get(json_fieldname)))
                    except ValueError:
                        raise Exception("Invalid JSON in %s: %s" % (json_fieldname, source_rep.get(json_fieldname)))
                    if isinstance(getattr(rep, json_fieldname), list):
                        for d in getattr(rep, json_fieldname):
                            if isinstance(d, dict):
                                for k in d.keys():
                                    if not d[k]:
                                        del d[k]

            incumbent = str(source_rep.get('incumbent')).lower()
            if incumbent in ('1', 'true', 'yes', 'y'):
                rep.incumbent = True
            elif incumbent in ('0', 'false', 'no', 'n'):
                rep.incumbent = False

            if not source_rep.get('name'):
                rep.name = ' '.join([component for component in [source_rep.get('first_name'), source_rep.get('last_name')] if component])
            if not source_rep.get('first_name') and not source_rep.get('last_name'):
                (rep.first_name, rep.last_name) = split_name(rep.name)

            boundary_url = None
            # Match boundary based on 'boundary_url', then 'district_id', then 'district_name'
            if source_rep.get('boundary_url') and _check_boundary_validity(source_rep['boundary_url']):
                boundary_url = source_rep['boundary_url']
            elif boundaries:
                if rep.district_id:
                    boundary_url = boundary_ids.get(rep.district_id)
                if not boundary_url:
                    boundary_url = boundary_names.get(get_comparison_string(rep.district_name))

            if not boundary_url:
                logger.warning("Couldn't find district boundary %s in %s" % (rep.district_name, self.boundary_set))
            else:
                rep.boundary = boundary_url_to_name(boundary_url)
                if not rep.district_name:
                    rep.district_name = url_to_name.get(boundary_url, '')
                if not rep.district_id:
                    rep.district_id = url_to_id.get(boundary_url, '')
            rep.save()

        self.last_import_time = datetime.datetime.now()
        self.last_import_successful = True
        self.save()
        return len(data)


class RepresentativeSet(BaseRepresentativeSet):

    def create_child(self):
        return Representative(representative_set=self)

    def get_absolute_url(self):
        return reverse('representatives_representative_set_detail',
            kwargs={'slug': self.slug})

    def as_dict(self):
        r = super(RepresentativeSet, self).as_dict()
        r['related']['representatives_url'] = reverse(
            'representatives_representative_list', kwargs={'set_slug': self.slug})
        return r


class Election(BaseRepresentativeSet):
    election_date = models.DateField()

    def create_child(self):
        return Candidate(election=self)

    def get_absolute_url(self):
        return reverse('representatives_election_detail',
            kwargs={'slug': self.slug})

    def as_dict(self):
        r = super(Election, self).as_dict()
        r['election_date'] = str(self.election_date) if self.election_date else None
        r['related']['candidates_url'] = reverse(
            'representatives_candidate_list', kwargs={'set_slug': self.slug})
        return r

    def update_from_data_source(self):
        # Disable Election if the date has passed
        if (app_settings.DISABLE_CANDIDATES_AFTER_ELECTION and
                self.election_date and
                datetime.date.today() - self.election_date > datetime.timedelta(
                    days=app_settings.DISABLE_CANDIDATES_AFTER_ELECTION)):
            self.enabled = False
            self.save()
            self.individuals.all().delete()
            return False
        return super(Election, self).update_from_data_source()


class BaseRepresentative(models.Model):
    name = models.CharField(max_length=300)
    district_name = models.CharField(max_length=300)
    elected_office = models.CharField(max_length=200)
    source_url = models.URLField(max_length=2048)
    boundary = models.CharField(max_length=300, blank=True, db_index=True,
        help_text="e.g. federal-electoral-districts/outremont")
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    party_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True, max_length=2048)
    personal_url = models.URLField(blank=True, max_length=2048)
    photo_url = models.URLField(blank=True, max_length=2048)
    district_id = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, blank=True, choices=(
        ('F', 'Female'),
        ('M', 'Male')))
    offices = JSONField(default=[])
    extra = JSONField(default={})

    class Meta:
        abstract = True

    def __str__(self):
        return "%s (%s for %s)" % (
            self.name, self.elected_office, self.district_name)

    @property
    def boundary_url(self):
        return '/boundaries/%s/' % self.boundary if self.boundary else ''

    def as_dict(self):
        r = dict(((f, getattr(self, f)) for f in
            ('name', 'district_name', 'elected_office', 'source_url',
            'first_name', 'last_name', 'party_name', 'email', 'url', 'personal_url',
            'photo_url', 'gender', 'offices', 'extra')))
        set_obj = getattr(self, self.set_name)
        r[self.set_name + '_name'] = set_obj.name
        r['related'] = {
            self.set_name + '_url': set_obj.get_absolute_url()
        }
        if self.boundary_url:
            r['related']['boundary_url'] = self.boundary_url
        return r

    @staticmethod
    def get_dicts(reps):
        return [rep.as_dict() for rep in reps]


class Representative(BaseRepresentative):
    representative_set = models.ForeignKey(RepresentativeSet, related_name='individuals')
    set_name = 'representative_set'


class Candidate(BaseRepresentative):
    election = models.ForeignKey(Election, related_name='individuals')
    incumbent = models.NullBooleanField(blank=True)
    set_name = 'election'

    def as_dict(self):
        r = super(Candidate, self).as_dict()
        r['incumbent'] = self.incumbent
        return r


def _check_boundary_validity(boundary_url):
    """Check that a given boundary URL matches a boundary on the web service."""
    if not re.search(r'^/boundaries/[^/\s]+/[^/\s]+/$', boundary_url):
        return False
    try:
        resp = urlopen(urljoin(app_settings.BOUNDARYSERVICE_URL, boundary_url))
        return resp.code == 200
    except HTTPError:
        return False


def get_comparison_string(s):
    """Given a string or unicode, returns a simplified lowercase whitespace-free ASCII string.
    Used to compare slightly different versions of the same thing, which may differ in case,
    spacing, or use of accents."""
    nkfd_form = unicodedata.normalize('NFKD', str(s).lower())
    s = ''.join([c for c in nkfd_form if not unicodedata.combining(c)])
    s = re.sub(r'[^a-zA-Z0-9]', '-', s)
    return re.sub(r'--+', '-', s)


def split_name(name):
    """Given a name, returns (first_name, last_name)."""
    family_names = []
    components = name.split(' ')
    family_names.insert(0, components.pop())
    if components and components[-1] in ('De', 'Del', 'Di', 'Van', 'da', 'de', 'van'):
        family_names.insert(0, components.pop())
    return ' '.join(components), ' '.join(family_names)

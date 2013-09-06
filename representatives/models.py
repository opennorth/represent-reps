# coding: utf-8
import datetime
import json
import re
import urllib, urllib2
from urlparse import urljoin

from django.core import urlresolvers
from django.db import models, transaction
from django.template.defaultfilters import slugify

from appconf import AppConf
import dateutil.parser
from jsonfield import JSONField

from representatives.utils import (get_comparison_string, boundary_url_to_name,
                                   split_name, strip_honorific)

import logging
logger = logging.getLogger(__name__)

class MyAppConf(AppConf):
    SCRAPERWIKI_API_URL = 'https://api.scraperwiki.com/api/1.0/'
    BOUNDARYSERVICE_URL = 'http://represent.opennorth.ca/'

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
        help_text="The name of the political body, e.g. BC Legislature",
        unique=True)
    scraperwiki_name = models.CharField(max_length=100)
    last_scrape_time = models.DateTimeField(blank=True, null=True)
    last_import_time = models.DateTimeField(blank=True, null=True)
    last_scrape_successful = models.NullBooleanField(blank=True, null=True)
    boundary_set = models.CharField(max_length=300, blank=True,
        help_text="Name of the boundary set on the boundaries API, e.g. federal-electoral-districts")
    slug = models.SlugField(max_length=300, unique=True, db_index=True, editable=False)
    enabled = models.BooleanField(default=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(BaseRepresentativeSet, self).save(*args, **kwargs)

    @property
    def boundary_set_url(self):
        return u'/boundary-sets/%s/' % self.boundary_set if self.boundary_set else ''

    @property
    def boundaries_url(self):
        return u'/boundaries/%s/' % self.boundary_set if self.boundary_set else ''

    @property
    def scraperwiki_url(self):
        return u'https://scraperwiki.com/scrapers/%s/' % self.scraperwiki_name

    def as_dict(self):
        return {
            'name': self.name,
            'url': self.get_absolute_url(),
            'scraperwiki_url': self.scraperwiki_url,
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
            set_data = json.load(urllib2.urlopen(set_url))
            boundaries.extend(set_data['objects'])
            if set_data['meta'].get('next'):
                set_url = urljoin(app_settings.BOUNDARYSERVICE_URL, set_data['meta']['next'])
            else:
                return boundaries

    def update_scrape_status(self):
        """Checks from Scraperwiki whether the last scrape was successful."""
        api_url = urljoin(app_settings.SCRAPERWIKI_API_URL,
            'scraper/getruninfo') + '?' + urllib.urlencode({
                'format': 'jsondict',
                'name': self.scraperwiki_name
            })
        data = json.load(urllib2.urlopen(api_url))

        self.last_scrape_time = dateutil.parser.parse(data[0]['run_ended'])
        self.last_scrape_successful = not bool(data[0].get('exception_message'))
        self.save()
        return self.last_scrape_successful

    def create_child(self):
        """Should create an unsaved instance of a Candidate or Representative
        object belonging to this set."""
        raise NotImplementedError

    @transaction.commit_on_success
    def update_from_scraperwiki(self):

        if not self.update_scrape_status():
            # Don't update data if the scraper threw an exception on the last run
            return False

        api_url = urljoin(app_settings.SCRAPERWIKI_API_URL, 'datastore/sqlite') + '?' + urllib.urlencode({
            'format': 'jsondict',
            'name': self.scraperwiki_name,
            'query': 'select * from swdata'
        })
        data = json.load(urllib2.urlopen(api_url))

        if not (isinstance(data, list) and data):
            # No data, don't try an update
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

        _r_whitespace = re.compile(r'[^\S\n]+', flags=re.U)
        # Make all whitespace either newlines or spaces and remove whitespace around newlines.
        def clean_string(s):
            return re.sub(r' *\n *', "\n", _r_whitespace.sub(' ', unicode(s)).strip())

        abbreviations = {
            'British Columbia': 'BC',
            'Alberta': 'AB',
            'Saskatchewan': 'SK',
            'Manitoba': 'MB',
            'Ontario': 'ON',
            u'Québec': 'QC',
            'New Brunswick': 'NB',
            'PEI': 'PE',
            'Prince Edward Island': 'PE',
            'Nova Scotia': 'NS',
            'Newfoundland and Labrador': 'NL',
            'Yukon': 'YT',
            'Northwest Territories': 'NT',
            'Nunavut': 'NU',
        }
        # Abbreviates province name, correct postal codes, and formats last line of address.
        def clean_address(s):
            # The letter "O" instead of the numeral "0" is a common mistake.
            s = re.sub(r'\b[A-Z][O0-9][A-Z]\s?[O0-9][A-Z][O0-9]\b', lambda x: x.group(0).replace('O', '0'), s)
            for k, v in abbreviations.iteritems():
                s = re.sub(r'[,\n ]+\(?' + k + r'\)?(?=(?:[,\n ]+Canada)?(?:[,\n ]+[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9])?\Z)', ' ' + v, s)
            return re.sub(r'[,\n ]+([A-Z]{2})(?:[,\n ]+Canada)?[,\n ]+([A-Z][0-9][A-Z])\s?([0-9][A-Z][0-9])\Z', r' \1  \2 \3', s)

        # @see http://www.noslangues-ourlanguages.gc.ca/bien-well/fra-eng/typographie-typography/telephone-eng.html
        def clean_tel(s):
            digits = re.sub(r'\D', '', s)
            if len(digits) == 10:
                digits = '1' + digits
            if len(digits) == 11 and digits[0] == '1':
                return re.sub(r'\A(\d)(\d{3})(\d{3})(\d{4})\Z', r'\1-\2-\3-\4', digits)
            else:
                return s

        for source_rep in data:
            rep = self.create_child()
            for fieldname in ('name', 'district_name', 'elected_office', 'source_url', 'first_name', 'last_name',
                        'party_name', 'email', 'url', 'personal_url', 'photo_url', 'district_id',
                        'gender'):
                if source_rep.get(fieldname) is not None:
                    setattr(rep, fieldname, clean_string(source_rep[fieldname]))
            for json_fieldname in ('offices', 'extra'):
                if source_rep.get(json_fieldname):
                    try:
                        setattr(rep, json_fieldname, json.loads(source_rep.get(json_fieldname)))
                    except ValueError:
                        raise Exception(u"Invalid JSON in %s: %s" % (json_fieldname, source_rep.get(json_fieldname)))
                    if isinstance(getattr(rep, json_fieldname), list):
                        for d in getattr(rep, json_fieldname):
                            if isinstance(d, dict):
                                for k in d.keys():
                                    if isinstance(d[k], basestring):
                                        if d[k]:
                                            d[k] = clean_string(d[k])
                                            if k == 'postal':
                                                d[k] = clean_address(d[k])
                                            elif k in ['tel', 'alt', 'fax', 'tollfree']:
                                                d[k] = clean_tel(d[k])
                                        else:
                                            del d[k]
                                    elif d[k] is None:
                                        del d[k]

            incumbent = unicode(source_rep.get('incumbent')).lower()
            if incumbent in ('1', 'true', 'yes', 'y'):
                rep.incumbent = True
            elif incumbent in ('0', 'false', 'no', 'n'):
                rep.incumbent = False

            if not source_rep.get('name'):
                rep.name = ' '.join(filter(None, [source_rep.get('first_name'), source_rep.get('last_name')]))
            rep.name = strip_honorific(rep.name)
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
            rep.save()

        self.last_import_time = datetime.datetime.now()
        self.save()
        return len(data)


class RepresentativeSet(BaseRepresentativeSet):

    def create_child(self):
        return Representative(representative_set=self)

    def get_absolute_url(self):
        return urlresolvers.reverse('representatives_representative_set_detail',
            kwargs={'slug': self.slug})

    def as_dict(self):
        r = super(RepresentativeSet, self).as_dict()
        r['related']['representatives_url'] = urlresolvers.reverse(
            'representatives_representative_list', kwargs={'set_slug': self.slug})
        return r


class Election(BaseRepresentativeSet):
    election_date = models.DateField()

    def create_child(self):
        return Candidate(election=self)

    def get_absolute_url(self):
        return urlresolvers.reverse('representatives_election_detail',
            kwargs={'slug': self.slug})

    def as_dict(self):
        r = super(Election, self).as_dict()
        r['election_date'] = unicode(self.election_date) if self.election_date else None
        r['related']['candidates_url'] = urlresolvers.reverse(
            'representatives_candidate_list', kwargs={'set_slug': self.slug})
        return r

    def update_scrape_status(self):
        # Disable Election if the date has passed
        if (app_settings.DISABLE_CANDIDATES_AFTER_ELECTION is not False
                and self.election_date
                and datetime.date.today() - self.election_date > datetime.timedelta(
                    days=app_settings.DISABLE_CANDIDATES_AFTER_ELECTION)):
            self.enabled = False
            self.save()
            self.individuals.all().delete()
            return False
        return super(Election, self).update_scrape_status()

    
class BaseRepresentative(models.Model):
    
    name = models.CharField(max_length=300)
    district_name = models.CharField(max_length=300)
    elected_office = models.CharField(max_length=200)
    source_url = models.URLField()
    
    boundary = models.CharField(max_length=300, blank=True, db_index=True,
        help_text="e.g. federal-electoral-districts/outremont")
    
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    party_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    personal_url = models.URLField(blank=True)
    photo_url = models.URLField(blank=True)
    district_id = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, blank=True, choices = (
        ('F', 'Female'),
        ('M', 'Male')))
    
    offices = JSONField(blank=True)
    extra = JSONField(blank=True)

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return "%s (%s for %s)" % (
            self.name, self.elected_office, self.district_name)

    def save(self, *args, **kwargs):
        if not self.offices:
            self.offices = []
        if not self.extra:
            self.extra = {}
        super(BaseRepresentative, self).save(*args, **kwargs)

    @property
    def boundary_url(self):
        return '/boundaries/%s/' % self.boundary if self.boundary else ''

    def as_dict(self):
        r = dict( ( (f, getattr(self, f)) for f in
            ('name', 'district_name', 'elected_office', 'source_url',
            'first_name', 'last_name', 'party_name', 'email', 'url', 'personal_url',
            'photo_url', 'gender', 'offices', 'extra') ) )
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
        return [ rep.as_dict() for rep in reps ]


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
        resp = urllib2.urlopen(urljoin(app_settings.BOUNDARYSERVICE_URL, boundary_url))
        return resp.code == 200
    except urllib2.HTTPError:
        return False
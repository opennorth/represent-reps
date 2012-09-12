# coding: utf-8
import json
import re
import urllib, urllib2
from urlparse import urljoin

from django.core import urlresolvers
from django.db import models, transaction
from django.template.defaultfilters import slugify

from appconf import AppConf
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

app_settings = MyAppConf()

class RepresentativeSet(models.Model):
    name = models.CharField(max_length=300,
        help_text="The name of the political body, e.g. BC Legislature")
    scraperwiki_name = models.CharField(max_length=100)
    boundary_set = models.CharField(max_length=300, blank=True,
        help_text="Name of the boundary set on the boundaries API, e.g. federal-electoral-districts")
    slug = models.SlugField(max_length=300, unique=True, db_index=True, editable=False)
        
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(RepresentativeSet, self).save(*args, **kwargs)

    @property
    def boundary_set_url(self):
        return u'/boundary-sets/%s/' % self.boundary_set

    @property
    def boundaries_url(self):
        return u'/boundaries/%s/' % self.boundary_set

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
                'representatives_url': urlresolvers.reverse('representatives_representative_list', kwargs={'set_slug': self.slug})
            }
        }

    @staticmethod
    def get_dicts(sets):
        return [s.as_dict() for s in sets]

    @models.permalink
    def get_absolute_url(self):
        return 'representatives_representative_set_detail', [], {'slug': self.slug}

    def get_list_of_boundaries(self):
        if not self.boundary_set:
            return {}
        set_url = app_settings.BOUNDARYSERVICE_URL + 'boundaries/' + self.boundary_set + '/?limit=0'
        set_data = json.load(urllib2.urlopen(set_url))
        return set_data['objects']

    @transaction.commit_on_success
    def update_from_scraperwiki(self):
        api_url = urljoin(app_settings.SCRAPERWIKI_API_URL, 'datastore/sqlite') + '?' + urllib.urlencode({
            'format': 'jsondict',
            'name': self.scraperwiki_name,
            'query': 'select * from swdata'
        })
        data = json.load(urllib2.urlopen(api_url))

        # Delete existing data
        self.representative_set.all().delete()

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
                s = re.sub(r'[,\n ]+' + k + r'(?=(?:[,\n ]+Canada)?(?:[,\n ]+[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9])?\Z)', ' ' + v, s)
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
            rep = Representative(representative_set=self)
            for fieldname in ('name', 'district_name', 'elected_office', 'source_url', 'first_name', 'last_name',
                        'party_name', 'email', 'url', 'personal_url', 'photo_url', 'district_id',
                        'gender'):
                if source_rep.get(fieldname) is not None:
                    setattr(rep, fieldname, clean_string(source_rep[fieldname]))
            for json_fieldname in ('offices', 'extra'):
                if source_rep.get(json_fieldname):
                    setattr(rep, json_fieldname, json.loads(source_rep.get(json_fieldname)))
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

        return len(data)


    
class Representative(models.Model):
    representative_set = models.ForeignKey(RepresentativeSet)
    
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
    
    def __unicode__(self):
        return "%s (%s for %s in %s)" % (
            self.name, self.elected_office, self.district_name, self.representative_set)

    def save(self, *args, **kwargs):
        if not self.offices:
            self.offices = []
        if not self.extra:
            self.extra = {}
        super(Representative, self).save(*args, **kwargs)

    @property
    def representative_set_name(self):
        return self.representative_set.name

    @property
    def boundary_url(self):
        return '/boundaries/%s/' % self.boundary if self.boundary else ''

    def as_dict(self):
        r = dict( ( (f, getattr(self, f)) for f in
            ('name', 'district_name', 'elected_office', 'source_url',
            'first_name', 'last_name', 'party_name', 'email', 'url', 'personal_url',
            'photo_url', 'gender', 'offices', 'extra', 'representative_set_name') ) )
        r['related'] = {
            'representative_set_url': self.representative_set.get_absolute_url()
        }
        if self.boundary_url:
            r['related']['boundary_url'] = self.boundary_url
        return r

    @staticmethod
    def get_dicts(reps):
        return [ rep.as_dict() for rep in reps ]

def _check_boundary_validity(boundary_url):
    """Check that a given boundary URL matches a boundary on the web service."""
    if not re.search(r'^/boundaries/[^/\s]+/[^/\s]+/$', boundary_url):
        return False
    try:
        resp = urllib2.urlopen(urljoin(app_settings.BOUNDARYSERVICE_URL, boundary_url))
        return resp.code == 200
    except urllib2.HTTPError:
        return False
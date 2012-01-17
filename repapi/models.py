import json
import urllib, urllib2
from urlparse import urljoin

from django.core import urlresolvers
from django.db import models, transaction
from django.template.defaultfilters import slugify

from appconf import AppConf
from jsonfield import JSONField

from repapi.utils import slugify

import logging
logger = logging.getLogger(__name__)

class MyAppConf(AppConf):
    SCRAPERWIKI_API_URL = 'https://api.scraperwiki.com/api/1.0/'
    BOUNDARYSERVICE_URL = 'http://boundaries.opennorth.ca/'

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
    def scraperwiki_url(self):
        return u'https://scraperwiki.com/scrapers/%s/' % self.scraperwiki_name

    def as_dict(self):
        return {
            'name': self.name,
            'url': self.get_absolute_url(),
            'scraperwiki_url': self.scraperwiki_url,
            'related': {
                'boundary_set_url': self.boundary_set_url,
                'representatives_url': urlresolvers.reverse('repapi_representative_list', kwargs={'set_slug': self.slug})
            }
        }

    @staticmethod
    def get_dicts(sets):
        return [s.as_dict() for s in sets]

    @models.permalink
    def get_absolute_url(self):
        return 'repapi_representative_set_detail', [], {'slug': self.slug}

    def get_list_of_boundaries(self):
        if not self.boundary_set:
            return {}
        set_url = app_settings.BOUNDARYSERVICE_URL + 'boundaries/' + self.boundary_set + '/?limit=500'
        set_data = json.load(urllib2.urlopen(set_url))

        boundary_dict = dict(( (slugify(b['name']), b['url']) for b in set_data['objects']))

        return boundary_dict

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

        for source_rep in data:
            rep = Representative(representative_set=self)
            for fieldname in ('name', 'district_name', 'elected_office', 'source_url', 'first_name', 'last_name',
                        'party_name', 'email', 'url', 'personal_url', 'photo_url', 'district_id',
                        'gender', 'offices', 'extra'):
                if source_rep.get(fieldname) is not None:
                    setattr(rep, fieldname, source_rep[fieldname])

            district_slug = slugify(rep.district_name)
            if boundaries and district_slug:
                if district_slug not in boundaries:
                    logger.warning("Couldn't find district boundary %s in %s" % (rep.district_name, self.boundary_set))
                rep.boundary_url = boundaries.get(district_slug, '')
            rep.save()

        return len(data)


    
class Representative(models.Model):
    representative_set = models.ForeignKey(RepresentativeSet)
    
    name = models.CharField(max_length=300)
    district_name = models.CharField(max_length=300)
    elected_office = models.CharField(max_length=200)
    source_url = models.URLField()
    
    boundary_url = models.CharField(max_length=300, blank=True, db_index=True)
    
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
            self.offices = {}
        if not self.extra:
            self.extra = {}
        super(Representative, self).save(*args, **kwargs)

    @property
    def representative_set_name(self):
        return self.representative_set.name

    def as_dict(self):
        r = dict( ( (f, getattr(self, f)) for f in
            ('name', 'district_name', 'elected_office', 'source_url',
            'first_name', 'last_name', 'party_name', 'email', 'url', 'personal_url',
            'photo_url', 'gender', 'offices', 'extra') ) )
        r['related'] = {
            'representative_set_url': self.representative_set.get_absolute_url()
        }
        if self.boundary_url:
            r['related']['boundary_url'] = self.boundary_url
        return r

    @staticmethod
    def get_dicts(reps):
        return [ rep.as_dict() for rep in reps ]
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'RepresentativeSet', fields ['name']
        db.create_unique(u'representatives_representativeset', ['name'])

        # Adding unique constraint on 'Election', fields ['name']
        db.create_unique(u'representatives_election', ['name'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Election', fields ['name']
        db.delete_unique(u'representatives_election', ['name'])

        # Removing unique constraint on 'RepresentativeSet', fields ['name']
        db.delete_unique(u'representatives_representativeset', ['name'])


    models = {
        u'representatives.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'boundary': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'elected_office': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'individuals'", 'to': u"orm['representatives.Election']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'extra': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incumbent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'offices': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'representatives.election': {
            'Meta': {'object_name': 'Election'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'election_date': ('django.db.models.fields.DateField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_import_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'scraperwiki_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'})
        },
        u'representatives.representative': {
            'Meta': {'object_name': 'Representative'},
            'boundary': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'elected_office': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'extra': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'offices': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'representative_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'individuals'", 'to': u"orm['representatives.RepresentativeSet']"}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'representatives.representativeset': {
            'Meta': {'object_name': 'RepresentativeSet'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_import_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'scraperwiki_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'})
        }
    }

    complete_apps = ['representatives']

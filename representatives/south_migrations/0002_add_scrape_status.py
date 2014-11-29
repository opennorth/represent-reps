# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RepresentativeSet.last_scrape_time'
        db.add_column('representatives_representativeset', 'last_scrape_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'RepresentativeSet.last_scrape_successful'
        db.add_column('representatives_representativeset', 'last_scrape_successful', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RepresentativeSet.last_scrape_time'
        db.delete_column('representatives_representativeset', 'last_scrape_time')

        # Deleting field 'RepresentativeSet.last_scrape_successful'
        db.delete_column('representatives_representativeset', 'last_scrape_successful')


    models = {
        'representatives.representative': {
            'Meta': {'object_name': 'Representative'},
            'boundary': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'elected_office': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'extra': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'offices': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'representative_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['representatives.RepresentativeSet']"}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'representatives.representativeset': {
            'Meta': {'object_name': 'RepresentativeSet'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrape_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'scraperwiki_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'})
        }
    }

    complete_apps = ['representatives']

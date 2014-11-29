# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Election'
        db.create_table('representatives_election', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('scraperwiki_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_scrape_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_scrape_successful', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('boundary_set', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=300, db_index=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('election_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('representatives', ['Election'])

        # Adding model 'Candidate'
        db.create_table('representatives_candidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('district_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('elected_office', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('boundary', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=300, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('party_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('personal_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('photo_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('district_id', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('offices', self.gf('jsonfield.fields.JSONField')(blank=True)),
            ('extra', self.gf('jsonfield.fields.JSONField')(blank=True)),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(related_name='individuals', to=orm['representatives.Election'])),
            ('incumbent', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('representatives', ['Candidate'])

        # Adding field 'RepresentativeSet.enabled'
        db.add_column('representatives_representativeset', 'enabled', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Election'
        db.delete_table('representatives_election')

        # Deleting model 'Candidate'
        db.delete_table('representatives_candidate')

        # Deleting field 'RepresentativeSet.enabled'
        db.delete_column('representatives_representativeset', 'enabled')


    models = {
        'representatives.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'boundary': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'elected_office': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'individuals'", 'to': "orm['representatives.Election']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'extra': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'representatives.election': {
            'Meta': {'object_name': 'Election'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'election_date': ('django.db.models.fields.DateField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrape_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'scraperwiki_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'})
        },
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
            'representative_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'individuals'", 'to': "orm['representatives.RepresentativeSet']"}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'representatives.representativeset': {
            'Meta': {'object_name': 'RepresentativeSet'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrape_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_scrape_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'scraperwiki_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'})
        }
    }

    complete_apps = ['representatives']

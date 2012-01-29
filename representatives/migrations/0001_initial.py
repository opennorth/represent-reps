# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RepresentativeSet'
        db.create_table('representatives_representativeset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('scraperwiki_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('boundary_set', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=300, db_index=True)),
        ))
        db.send_create_signal('representatives', ['RepresentativeSet'])

        # Adding model 'Representative'
        db.create_table('representatives_representative', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('representative_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['representatives.RepresentativeSet'])),
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
        ))
        db.send_create_signal('representatives', ['Representative'])


    def backwards(self, orm):
        
        # Deleting model 'RepresentativeSet'
        db.delete_table('representatives_representativeset')

        # Deleting model 'Representative'
        db.delete_table('representatives_representative')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'scraperwiki_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300', 'db_index': 'True'})
        }
    }

    complete_apps = ['representatives']

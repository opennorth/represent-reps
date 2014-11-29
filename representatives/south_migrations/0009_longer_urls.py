# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Candidate.url'
        db.alter_column(u'representatives_candidate', 'url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Candidate.source_url'
        db.alter_column(u'representatives_candidate', 'source_url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Candidate.personal_url'
        db.alter_column(u'representatives_candidate', 'personal_url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Candidate.photo_url'
        db.alter_column(u'representatives_candidate', 'photo_url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Representative.url'
        db.alter_column(u'representatives_representative', 'url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Representative.source_url'
        db.alter_column(u'representatives_representative', 'source_url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Representative.personal_url'
        db.alter_column(u'representatives_representative', 'personal_url', self.gf('django.db.models.fields.URLField')(max_length=2048))

        # Changing field 'Representative.photo_url'
        db.alter_column(u'representatives_representative', 'photo_url', self.gf('django.db.models.fields.URLField')(max_length=2048))

    def backwards(self, orm):

        # Changing field 'Candidate.url'
        db.alter_column(u'representatives_candidate', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Candidate.source_url'
        db.alter_column(u'representatives_candidate', 'source_url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Candidate.personal_url'
        db.alter_column(u'representatives_candidate', 'personal_url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Candidate.photo_url'
        db.alter_column(u'representatives_candidate', 'photo_url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Representative.url'
        db.alter_column(u'representatives_representative', 'url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Representative.source_url'
        db.alter_column(u'representatives_representative', 'source_url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Representative.personal_url'
        db.alter_column(u'representatives_representative', 'personal_url', self.gf('django.db.models.fields.URLField')(max_length=200))

        # Changing field 'Representative.photo_url'
        db.alter_column(u'representatives_representative', 'photo_url', self.gf('django.db.models.fields.URLField')(max_length=200))

    models = {
        u'representatives.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'boundary': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'elected_office': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'individuals'", 'to': u"orm['representatives.Election']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'extra': ('jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incumbent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'offices': ('jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '2048'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'})
        },
        u'representatives.election': {
            'Meta': {'object_name': 'Election'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'data_about_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'data_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'election_date': ('django.db.models.fields.DateField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_import_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_import_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300'})
        },
        u'representatives.representative': {
            'Meta': {'object_name': 'Representative'},
            'boundary': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '300', 'blank': 'True'}),
            'district_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'elected_office': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'extra': ('jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'offices': ('jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'personal_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'}),
            'photo_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'}),
            'representative_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'individuals'", 'to': u"orm['representatives.RepresentativeSet']"}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '2048'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'})
        },
        u'representatives.representativeset': {
            'Meta': {'object_name': 'RepresentativeSet'},
            'boundary_set': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'data_about_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'data_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_import_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'last_import_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '300'})
        }
    }

    complete_apps = ['representatives']
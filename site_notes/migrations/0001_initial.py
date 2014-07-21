# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteNotes'
        db.create_table(u'site_notes_sitenotes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.OneToOneField')(related_name='extra_fields', unique=True, to=orm['sites.Site'])),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'site_notes', ['SiteNotes'])

        # Adding model 'RedirectNotes'
        db.create_table(u'site_notes_redirectnotes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.OneToOneField')(related_name='extra_fields', unique=True, to=orm['redirects.Redirect'])),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'site_notes', ['RedirectNotes'])


    def backwards(self, orm):
        # Deleting model 'SiteNotes'
        db.delete_table(u'site_notes_sitenotes')

        # Deleting model 'RedirectNotes'
        db.delete_table(u'site_notes_redirectnotes')


    models = {
        u'redirects.redirect': {
            'Meta': {'ordering': "('old_path',)", 'unique_together': "(('site', 'old_path'),)", 'object_name': 'Redirect', 'db_table': "'django_redirect'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'old_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"})
        },
        u'site_notes.redirectnotes': {
            'Meta': {'object_name': 'RedirectNotes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'extra_fields'", 'unique': 'True', 'to': u"orm['redirects.Redirect']"})
        },
        u'site_notes.sitenotes': {
            'Meta': {'object_name': 'SiteNotes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'extra_fields'", 'unique': 'True', 'to': u"orm['sites.Site']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['site_notes']
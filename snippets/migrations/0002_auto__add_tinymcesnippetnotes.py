# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TinyMCESnippetNotes'
        db.create_table(u'snippets_tinymcesnippetnotes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.OneToOneField')(related_name='extra_fields', unique=True, to=orm['snippets.TinyMCESnippet'])),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('notes_zh_cn', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'snippets', ['TinyMCESnippetNotes'])


    def backwards(self, orm):
        # Deleting model 'TinyMCESnippetNotes'
        db.delete_table(u'snippets_tinymcesnippetnotes')


    models = {
        u'snippets.tinymcesnippet': {
            'Meta': {'object_name': 'TinyMCESnippet'},
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'snippets.tinymcesnippetnotes': {
            'Meta': {'object_name': 'TinyMCESnippetNotes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'notes_zh_cn': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'page': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'extra_fields'", 'unique': 'True', 'to': u"orm['snippets.TinyMCESnippet']"})
        }
    }

    complete_apps = ['snippets']
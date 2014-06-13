# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.legal_entity'
        db.add_column(u'registration_salesforce_profile', 'legal_entity',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'Profile.company_zip_code'
        db.add_column(u'registration_salesforce_profile', 'company_zip_code',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)

        # Adding field 'Profile.website'
        db.add_column(u'registration_salesforce_profile', 'website',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'Profile.street'
        db.add_column(u'registration_salesforce_profile', 'street',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'Profile.zip_code'
        db.add_column(u'registration_salesforce_profile', 'zip_code',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'Profile.language_preference'
        db.add_column(u'registration_salesforce_profile', 'language_preference',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.legal_entity'
        db.delete_column(u'registration_salesforce_profile', 'legal_entity')

        # Deleting field 'Profile.company_zip_code'
        db.delete_column(u'registration_salesforce_profile', 'company_zip_code')

        # Deleting field 'Profile.website'
        db.delete_column(u'registration_salesforce_profile', 'website')

        # Deleting field 'Profile.street'
        db.delete_column(u'registration_salesforce_profile', 'street')

        # Deleting field 'Profile.zip_code'
        db.delete_column(u'registration_salesforce_profile', 'zip_code')

        # Deleting field 'Profile.language_preference'
        db.delete_column(u'registration_salesforce_profile', 'language_preference')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registration_salesforce.profile': {
            'Meta': {'object_name': 'Profile'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'company_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'language_preference': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'last_salesforce_sync': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'legal_entity': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'mobile_product_interest': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'salesforce_id': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'salesforce_sync': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'type_of_device': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['registration_salesforce']
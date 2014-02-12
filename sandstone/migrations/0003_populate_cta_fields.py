# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        # Page model not accessible via the suggested orm method
        from mezzanine.pages.models import Page
        Page.objects.all().update(cta_title=models.F('subtitle'),cta_body=models.F('closing'))

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {

    }

    complete_apps = ['sandstone']
    symmetrical = True

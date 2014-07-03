from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.query import QuerySet

from concurrency.api import disable_concurrency

from mezzanine.core.models import SiteRelated
from mezzanine.forms.models import Form, Field


def get_site_for_language(language_code):
    """Get site for the given language code."""
    if language_code == settings.LANGUAGE_CODE:
        site = Site.objects.get_current()
    else:
        try:
            site = Site.objects.get(name=language_code)
        except Site.DoesNotExist:
            site = None
    return site


def build_site_for_language(language_code, copy_content=False):
    """Create a site for a given language."""
    site = get_site_for_language(language_code)
    if site is None:
        default = Site.objects.get_current()
        site = Site.objects.create(
            name=language_code,
            domain='%s.%s' % (language_code, default.domain)
        )
        if copy_content:
            build_site_content(site, base_site=default)
    else:
        # TODO: How to handle existing sites
        pass
    return site


def _get_site_models():
    """Get all model classes which subclass SiteRelated."""
    return filter(lambda m: issubclass(m, SiteRelated), models.get_models())


def build_site_content(site, base_site=None):
    """Build new site content by copying content from one site to another."""
    # Get all site related models
    models_to_copy = _get_site_models()
    base_site = base_site or Site.objects.get_current()
    for model_cls in models_to_copy:
        copies = []
        # Use a QuerySet rather than the default manager because the
        # CurrentSiteManager forces the site equal to the current SITE_ID
        for instance in QuerySet(model_cls).filter(site=base_site):
            instance._original_id = instance.id
            instance.id = None
            instance.site = site
            copies.append(instance)
        if copies:
            if not model_cls._meta.parents:
                QuerySet(model_cls).bulk_create(copies)
            else:
                # Multi-table inheritance classes can't be bulk created
                new_ids = []
                for c in copies:
                    for _, field in model_cls._meta.parents.items():
                        parent = getattr(c, field.name)
                        parent.id = None
                        setattr(c, field.name, parent)
                    if hasattr(c, '_concurrencymeta'):
                        with disable_concurrency(c):
                            c.save(force_insert=True)
                    else:
                        c.save(force_insert=True)
                    new_ids.append(c.id)
                    # Copy form fields
                    if model_cls == Form:
                        # Copy fields as well
                        fields = []
                        for field in Field.objects.filter(form=instance._original_id):
                            field.id = None
                            field.form = c
                            fields.append(field)
                        Field.objects.bulk_create(fields)
                # SiteRelated.save will force this to the "current" site
                # so these need to be updated with the site we actually want
                QuerySet(model_cls).filter(id__in=new_ids).update(site=site)

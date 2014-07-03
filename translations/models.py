from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models


def get_site_for_language(language_code):
    """Get site for the given language code."""
    if language == settings.LANGUAGE_CODE:
        site = Site.objects.get_current()
    else:
        try:
            site = Site.objects.get(name=language)
        except Site.DoesNotExist:
            site = None
    return site


def build_site_for_language(language_code):
    """Create a site for a given language."""
    default = Site.objects.get_current()
    site = get_site_for_language(language_code)
    if site is None:
        site = Site.objects.create(
            name=language_code,
            domain='%s.%s' % (language_code, default.domain)
        )
        # TODO: Copy the current pages over

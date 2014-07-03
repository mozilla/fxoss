from django.conf import settings
from django.contrib.sites.models import Site


class LocaleSiteMiddleware(object):
    """Middleware to dynamically change the current request site based on the
    user's locale. This relies on the request.LANGUAGE_CODE set by
    the `django.middleware.locale.LocaleMiddleware` and must come after it
    in the middleware stack."""

    def process_request(self, request):
        """Site records should have name equal to the language code."""
        site_id = getattr(request, 'site_id', None)
        language = getattr(request, 'LANGUAGE_CODE', None)
        if site_id is None and language is not None:
            if language == settings.LANGUAGE_CODE:
                # This is the default language
                # Clear any explicit site in the session
                if 'site_id' in request.session:
                    del request.session['site_id']
            else:
                try:
                    site_id = Site.objects.get(name=language).pk
                except Site.DoesNotExist:
                    site_id = None
        if site_id is not None:
            request.session['site_id'] = site_id
            request.site_id = site_id

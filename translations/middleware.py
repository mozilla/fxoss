from django.conf import settings

from .utils import get_site_for_language


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
            site = get_site_for_language(language)
            if site is None or site.pk == settings.SITE_ID:
                # Use the default site
                # Clear any explicit site in the session
                if 'site_id' in request.session:
                    del request.session['site_id']
            else:
                request.session['site_id'] = site.pk
                request.site_id = site.pk

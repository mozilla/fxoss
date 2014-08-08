import contextlib

import mezzanine.core.request

from django.conf import settings
from django.http import HttpRequest


@contextlib.contextmanager
def override_current_site(site_id=None):
    """Temporarily change the current Mezzanine site."""
    site_id = site_id or settings.SITE_ID
    current = mezzanine.core.request.current_request()
    fake = HttpRequest()
    fake.site_id = site_id
    mezzanine.core.request._thread_local.request = fake
    try:
        yield
    finally:
        mezzanine.core.request._thread_local.request = current

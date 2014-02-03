from __future__ import unicode_literals

from django.conf.urls import patterns, url

from mezzanine.conf import settings


ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/account/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL",
                     "/%s/signup/" % ACCOUNT_URL.strip("/"))

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = patterns("project.fxoss.views",
    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash),
        "signup", name="signup"),
)

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from mezzanine.conf import settings


ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL",
                     "/%s/signup/" % ACCOUNT_URL.strip("/"))

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = patterns("registration_salesforce.views",
    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash),
        "signup", name="signup"),
)


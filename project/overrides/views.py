from __future__ import unicode_literals

import requests

from django.contrib.auth import login as auth_login
from django.contrib.messages import info
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url
from mezzanine.utils.views import render


SALESFORCE_FIELD_MAPPINGS = {
    'type_of_device': '00NU0000003WwlV',
    'mobile_product_interest': '00NU0000003WwlQ'
}

def signup(request, template="accounts/account_signup.html"):
    """
    Signup form.
    """
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        new_user = form.save()

        # Generate Salesforce Lead
        data = form.cleaned_data.copy()
        # Pop non-Salesforce Fields
        for field in ['password1', 'password2']:
            data.pop(field)
        for k, v in SALESFORCE_FIELD_MAPPINGS.items():
            data[v] = data.pop(k)
        data['oid'] = '00DU0000000IrgO'
        # As we're doing the Salesforce POST in the background here,
        # `retURL` is never visited/seen by the user. I believe it
        # is required by Salesforce though, so it should hang around
        # as a placeholder (with a valid URL, just in case).
        data['retURL'] = (request.build_absolute_uri())


        #r = requests.post('https://www.salesforce.com/servlet/'
        #                  'servlet.WebToLead?encoding=UTF-8', data)
        # TODO: Check status code for errors and...?

        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                send_approve_mail(request, new_user)
                info(request, _("Thanks for signing up! You'll receive "
                                "an email when your account is activated."))
            else:
                send_verification_mail(request, new_user, "signup_verify")
                info(request, _("A verification email has been sent with "
                                "a link for activating your account."))
            return redirect(next_url(request) or "/")
        else:
            info(request, _("Successfully signed up"))
            auth_login(request, new_user)
            return login_redirect(request)
    context = {"form": form, "title": _("Sign up")}
    return render(request, template, context)


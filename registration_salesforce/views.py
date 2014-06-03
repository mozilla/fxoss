from __future__ import unicode_literals

import requests

from django.contrib.auth import login as auth_login
from django.contrib.messages import info
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url
from mezzanine.utils.views import render

from .forms import UserRegistrationLeadForm


def signup(request, template="accounts/account_signup.html"):
    """
    Signup form.
    """
    profile_form = UserRegistrationLeadForm
    form = profile_form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data.copy()

        # ensure user is not a robot
        honeypot = data.pop('superpriority')
        if honeypot:
            raise PermissionDenied

        # save the user
        new_user = form.save()

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


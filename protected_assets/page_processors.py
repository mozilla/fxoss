from __future__ import unicode_literals

from django.shortcuts import redirect
from django.utils.http import is_safe_url

from mezzanine.conf import settings
from mezzanine.pages.page_processors import processor_for

from .forms import AgreementForm
from .models import Agreement


@processor_for('download-agreement')
def download_agreement(request, page):
    form = AgreementForm()
    if request.method == "POST":
        form = AgreementForm(request.POST)
        if form.is_valid():
            settings.use_editable()
            Agreement.objects.create(
                user=request.user,
                ip=request.META.get('REMOTE_ADDR') or None,
                version=settings.DOWNLOAD_AGREEMENT_VERSION
            )
            redirect_field_name = 'next'
            default_next = '/'
            next_page = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name))
            next_page = next_page or default_next
            if not is_safe_url(url=next_page, host=request.get_host()):
                next_page = default_next
            return redirect(next_page)
    return {"form": form}

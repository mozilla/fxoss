from __future__ import unicode_literals

import os
import urllib

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.views.static import serve

from filebrowser_safe.settings import DIRECTORY as FILEBROWSER_DIRECTORY
from mezzanine.conf import settings

from .models import Agreement


@login_required
def protected_download(request, path):
    """Check for a signed download agreement before delivering the asset."""
    settings.use_editable()
    agreement = Agreement.objects.filter(user=request.user, version=settings.DOWNLOAD_AGREEMENT_VERSION)
    if not agreement.exists():
        params = {'next': request.path}
        previous = request.META.get('HTTP_REFERER', None) or None
        if previous is not None:
            params['next'] = previous
            request.session['waiting_download'] = request.path
        agreement_url = '%s?%s' % (
            reverse('page', kwargs={'slug': 'download-agreement'}),
            urllib.urlencode(params))
        return redirect(agreement_url)
    if settings.DEBUG:
        response = serve(request, path, document_root=os.path.join(settings.MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'protected'))
    else:
        response = HttpResponse()
        response['X-Accel-Redirect'] = '/__protected__/%s' % path
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(path)
    if request.path == request.session.get('waiting_download'):
         del request.session['waiting_download']
    if request.path == request.session.get('ready_download'):
         del request.session['ready_download']
    return response

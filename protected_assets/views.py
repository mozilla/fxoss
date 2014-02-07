from __future__ import unicode_literals

import os

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
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
        agreement_url = '%s?next=%s' % (reverse('page', kwargs={'slug': 'download-agreement'}), request.path)
        return redirect(agreement_url)
    if settings.DEBUG:
        response = serve(request, path, document_root=os.path.join(settings.MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'protected'))
    else:
        response = HttpResponse()
        response['X-Accel-Redirect'] = "/__protected__/%s" % path
    response["Content-Disposition"] = "attachment; filename=%s" % os.path.basename(path)
    return response

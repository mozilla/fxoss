from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.static import serve

from filebrowser_safe.settings import DIRECTORY as FILEBROWSER_DIRECTORY


@login_required
def protected_download(request, path):
    """Check for a signed download agreement before delivering the asset."""
    # TODO: Define what it means to have signed the agreement
    if not request.user.is_staff:
        return redirect('page', kwargs={'slug': 'download-agreement'})
    if settings.DEBUG:
        response = serve(request, path, document_root=os.path.join(settings.MEDIA_ROOT, FILEBROWSER_DIRECTORY, 'protected'))
    else:
        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename=%s" % os.path.basename(path)
        response['X-Accel-Redirect'] = "/protected/%s" % path
    return response
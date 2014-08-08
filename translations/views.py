from __future__ import unicode_literals

from django import http
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _


# Custom admin View On Site view
@staff_member_required
def shortcut(request, content_type_id, object_id):
    """
    Redirect to an object's page based on a content-type ID and an object ID.
    """
    # Look up the object, making sure it's got a get_absolute_url() function.
    try:
        content_type = ContentType.objects.get(pk=content_type_id)
        if not content_type.model_class():
            raise http.Http404(_("Content type %(ct_id)s object has no associated model") %
                               {'ct_id': content_type_id})
        obj = content_type.get_object_for_this_type(pk=object_id)
    except (ObjectDoesNotExist, ValueError):
        raise http.Http404(_("Content type %(ct_id)s object %(obj_id)s doesn't exist") %
                           {'ct_id': content_type_id, 'obj_id': object_id})

    try:
        get_absolute_url = obj.get_absolute_url
    except AttributeError:
        raise http.Http404(_("%(ct_name)s objects don't have a get_absolute_url() method") %
                           {'ct_name': content_type.name})
    # We do not want the object domain as the translation middleware will
    # ensure the viewer is directed to the appropriate place, and cross domain
    # requests (handled in the default version) are not an issue, so just redirect
    # to the object's get_absolute_url value
    return http.HttpResponseRedirect(get_absolute_url())

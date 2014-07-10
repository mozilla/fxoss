from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db.models.query import QuerySet
from django.template.loader import select_template
from django.utils.translation import override

from mezzanine.conf import settings


class TranslatableMixin(object):
    """Fetches the base English version of the current content when making an edit."""

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if change and obj.site_id != settings.SITE_ID:
            # Grab the default language version of the object
            try:
                default = QuerySet(obj.__class__).filter(slug=obj.slug, site=settings.SITE_ID)[0]
            except IndexError:
                default = None
            with override(settings.LANGUAGE_CODE):
                meta = default.__class__._meta
                context['default_language_url'] = reverse(admin_urlname(meta, 'change'), args=(default.id, ))
        response = super(TranslatableMixin, self).render_change_form(request, context,
            add=add, change=change, form_url=form_url, obj=obj)
        if change and obj.site_id != settings.SITE_ID:
            # Hijack the delayed rendering to replace the change form while
            # extending from the original template
            if not response.is_rendered:
                current_template = select_template(response.template_name).name
                response.context_data['base_template'] = current_template
                response.template_name = 'translations/admin/change_form.html'
        return response
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db.models.query import QuerySet
from django.template.loader import select_template
from django.utils.encoding import force_text
from django.utils.translation import override

from mezzanine.conf import settings

from .models import TODOItem
from .utils import get_site_for_language


class TranslatableMixin(object):
    """Fetches the base English version of the current content when making an edit."""

    tranlsated_fields = []

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if change and obj.site_id != settings.SITE_ID:
            # Grab the default language version of the object
            try:
                default = QuerySet(obj.__class__).filter(slug=obj.slug, site=settings.SITE_ID)[0]
            except IndexError:
                context['default_language_url'] = None
            else:
                with override(settings.LANGUAGE_CODE):
                    meta = default.__class__._meta
                    context['default_language_url'] = reverse(
                        admin_urlname(meta, 'change'), args=(default.id, ))
                    context['tranlsated_fields'] = self.tranlsated_fields
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

    def _build_todo_items(self, obj, user, changes=None, delete=False):
        languages = [code for code, name in  settings.LANGUAGES if code != settings.LANGUAGE_CODE]
        for lang in  languages:
            site = get_site_for_language(lang)
            if site is None:
                continue
            current = None
            if delete or changes:
                # Grab the translated version of the object
                try:
                    current = QuerySet(obj.__class__).filter(slug=obj.slug, site=site)[0]
                except IndexError:
                    current = None
            if delete:
                if current is not None:
                    # Translated version should be deleted as well
                    TODOItem.objects.create(
                        title=force_text(title), slug=obj.slug, page=current,
                        action=TODOItem.ACTION_DELETE,
                        description='Delete %s' % obj.__class__._meta.vebose_name,
                        editor=user, site=site)
            elif changes is not None:
                if changes and current is not None:
                    # Translated version should be updated as well
                    TODOItem.objects.create(
                        title=force_text(obj), slug=obj.slug, page=current,
                        action=TODOItem.ACTION_EDIT,
                        description='Update %s' % ', '.join(c for c in changes),
                        editor=user, site=site)
            else:
                # Need to create translated version
                TODOItem.objects.create(
                    title=force_text(obj), slug=obj.slug, page=None,
                    action=TODOItem.ACTION_ADD,
                    description='Create %s' % obj.__class__._meta.vebose_name,
                    editor=user, site=site)

    def save_model(self, request, obj, form, change):
        super(TranslatableMixin, self).save_model(request, obj, form, change)
        # If this is the default language, create TODO items for the other languages
        if obj.site_id == settings.SITE_ID:
            changes = None
            if change:
                changes = [name for name in form.changed_data if name in self.tranlsated_fields]
            self._build_todo_items(obj, request.user, changes=changes, delete=False)

    def delete_model(self, request, obj):
        super(TranslatableMixin, self).delete_model(request, obj)
        # If this is the default language, create TODO items for the other languages
        if obj.site_id == settings.SITE_ID:
            self._build_todo_items(obj, request.user, changes=None, delete=True)


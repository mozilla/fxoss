from __future__ import unicode_literals

from optparse import make_option

from django.conf import settings
from django.core.management.base import LabelCommand

from translations.models import build_site_for_language


class Command(LabelCommand):
    """Creates Site records and copies the initial pages from the default site."""

    args = '<language language ...>'
    label = 'language code'

    option_list = LabelCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all_languages',
            default=False,
            help='Create a site for all languages in the LANGUAGES setting.'
        ),
        make_option('--skip-content',
            action='store_true',
            dest='skip_content',
            default=False,
            help='Don\'t copy the CMS content for the newly created sites.'
        ),
    )

    def handle(self, *labels, **options):
        if options.get('all_languages', False):
            labels = [code for code, name in  settings.LANGUAGES if code != settings.LANGUAGE_CODE]
        return super(Command, self).handle(*labels, **options)

    def handle_label(self, label, **options):
        """Create a new site for the language."""
        build_site_for_language(label, copy_content=not options.get('skip_content', False))
        return 'Created site for %s' % label

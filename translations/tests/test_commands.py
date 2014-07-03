from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase

from mock import patch, call


@patch('translations.management.commands.build_language_sites.build_site_for_language')
class BuildSitesCommandTestCase(SimpleTestCase):
    """Management command to create new language sites."""

    def test_create_single_site(self, mock_build_site):
        """Create a new language site."""
        call_command('build_language_sites', 'zh-cn')
        mock_build_site.assert_called_with('zh-cn')

    def test_create_multiple_sites(self, mock_build_site):
        """Create multiple sites at once."""
        call_command('build_language_sites', 'zh-cn', 'fr')
        mock_build_site.assert_has_calls([call('zh-cn'), call('fr')])

    def test_create_all_sites(self, mock_build_site):
        """Helper to create all defined language sites."""
        languages =(
            ('en', 'English'),
            ('zh-cn', 'Simplified Chinese'),
            ('fr', 'French'),
        )
        default = 'en'
        with self.settings(LANGUAGES=languages, LANGUAGE_CODE=default):
            call_command('build_language_sites', all_languages=True)
            mock_build_site.assert_has_calls([call('zh-cn'), call('fr')])

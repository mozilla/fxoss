import sys

from django.core.management.base import CommandError, NoArgsCommand
from django.utils.log import getLogger

from ...leads import sync_leads_from_profiles


logger = getLogger('management_commands')


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            sync_leads_from_profiles() 
        except Exception as e:
            logger.error('sync_leads Error: ' + e.message,
                         exc_info=sys.exc_info())
            raise CommandError(e)

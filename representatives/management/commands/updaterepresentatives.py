from __future__ import unicode_literals

import logging
import itertools

from django.core.management.base import BaseCommand

from representatives.models import RepresentativeSet, Election

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Updates representatives from sources.'

    def handle(self, *args, **options):
        for representative_set in itertools.chain(RepresentativeSet.objects.filter(enabled=True), Election.objects.filter(enabled=True)):
            try:
                representative_set.update_from_data_source()
            except Exception:
                log.error("Couldn't update representatives in %s." % representative_set)
                representative_set.__class__.objects.filter(pk=representative_set.pk).update(last_import_successful=False)

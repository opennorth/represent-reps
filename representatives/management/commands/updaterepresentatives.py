import logging
import itertools

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pulls new data for all RepresentativeSets from ScraperWiki'

    def handle(self, *args, **options):
        from representatives.models import RepresentativeSet, Election

        for rs in itertools.chain(
                RepresentativeSet.objects.filter(enabled=True), Election.objects.filter(enabled=True)):
            try:
                rs.update_from_data_source()
            except Exception as e:
                logger.exception("Failure updating %r" % rs)
                rs.__class__.objects.filter(pk=rs.pk).update(last_import_successful=False)

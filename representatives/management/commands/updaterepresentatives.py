import logging
import itertools

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pulls new data for all RepresentativeSets from ScraperWiki'

    def handle(self, *args, **options):
        from representatives.models import RepresentativeSet, CandidateSet

        for rs in itertools.chain(
                RepresentativeSet.objects.all(), CandidateSet.objects.all()):
            rs.update_from_scraperwiki()

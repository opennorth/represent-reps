import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Pulls new data for all RepresentativeSets from ScraperWiki'

    def handle(self, *args, **options):
        from representatives.models import RepresentativeSet

        for rs in RepresentativeSet.objects.all():
            rs.update_from_scraperwiki()
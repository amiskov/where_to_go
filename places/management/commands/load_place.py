import logging

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from urllib.parse import unquote

from ._place_loader import create_place

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class Command(BaseCommand):
    help = 'Import places from URL (in JSON).'

    def handle(self, *args, **options):
        for url in options['urls']:
            try:
                create_place(url)
            except IntegrityError as err:
                filename = unquote(url.split('/')[-1])
                logging.error(f'Place from {filename} already exists with different data.')

    def add_arguments(self, parser):
        parser.add_argument(dest='urls', nargs='+',
                            help='A URL of a place JSON to import.')

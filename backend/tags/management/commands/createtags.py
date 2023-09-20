import csv

from django.core.management.base import BaseCommand

from tags.models import Tag


class Command(BaseCommand):
    help = 'Create tags for app'

    def handle(self, *args, **options):
        tags = (
            {'name': 'Завтрак', 'color': '#2ECC71', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#F39C12', 'slug': 'launch'},
            {'name': 'Ужин', 'color': '#9B59B6', 'slug': 'dinner'}
        )
        Tag.objects.bulk_create(
            [Tag(**kwargs) for kwargs in tags]
        )
        self.stdout.write(self.style.SUCCESS('All tags created!'))

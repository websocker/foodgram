import csv

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Create ingredients for app'

    def handle(self, *args, **options):
        file_path = './data/ingredients.csv'
        with open(file_path, 'r', encoding='utf-8') as ingredients_csv:
            ingredients = [
                kwargs for kwargs in
                csv.DictReader(ingredients_csv,
                               fieldnames=('name', 'measurement_unit'),
                               delimiter=',')
            ]
            Ingredient.objects.bulk_create(
                [Ingredient(**kwargs) for kwargs in ingredients]
            )
        self.stdout.write(self.style.SUCCESS('All ingredients created!'))

from django.core.management.base import BaseCommand
from recommender import train_model

class Command(BaseCommand):
    help = 'Train the LightFM recommendation model'

    def handle(self, *args, **kwargs):
        train_model()
        self.stdout.write(self.style.SUCCESS('Модель рекомендаций обучена и сохранена.'))

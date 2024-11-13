
from django.core.management.base import BaseCommand
from catfact_app.models import CatFact
from catfact_app.views import CatFactView

class Command(BaseCommand):
    help = 'Import cat facts from the external API and save them to the CatFact model.'

    def handle(self, *args, **kwargs):
        factsData = CatFactView.addFacts()
        self.stdout.write(self.style.SUCCESS(f"Successfully imported fact: {factsData}"))


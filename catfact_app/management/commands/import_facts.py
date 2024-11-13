
from django.core.management.base import BaseCommand
from catfact_app.models import CatFact
from catfact_app.views import CatFactView

class Command(BaseCommand):
    help = 'Import cat facts from the external API and save them to the CatFact model.'

    def handle(self, *args, **kwargs):
        factsData = CatFactView.addFacts()
        self.stdout.write(self.style.SUCCESS(f"Successfully imported fact: {factsData}"))

        # url = 'https://catfact.ninja/fact'
        # response = requests.get(url)
        
        # if response.status_code == 200:
        #     data = response.json()
        #     fact_text = data.get('fact')
        #     length = data.get('length')
        #     if fact_text:
        #         CatFact.objects.create(fact=fact_text, length=length)
        #         self.stdout.write(self.style.SUCCESS(f"Successfully imported fact: {fact_text}, Length: {length}"))
        #     else:
        #         self.stdout.write(self.style.WARNING("No fact available in the response."))
        # else:
        #     self.stderr.write(f"Failed to fetch cat fact. HTTP status code: {response.status_code}")

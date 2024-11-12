import requests
from django.core.management.base import BaseCommand
from catfact_app.models import CatFact

class Command(BaseCommand):
    help = 'Import cat facts from the external API and save them to the CatFact model.'

    def handle(self, *args, **kwargs):
        # The URL from where we fetch the cat facts
        url = 'https://catfact.ninja/fact'

        # Fetch the cat fact
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the JSON data from the API response
            data = response.json()

            # Extract the fact and its length
            fact_text = data.get('fact')
            length = data.get('length')

            # Save the data into the CatFact model
            if fact_text:
                CatFact.objects.create(fact=fact_text, length=length)
                self.stdout.write(self.style.SUCCESS(f"Successfully imported fact: {fact_text}"))
            else:
                self.stdout.write(self.style.WARNING("No fact available in the response."))

        else:
            self.stderr.write(f"Failed to fetch cat fact. HTTP status code: {response.status_code}")

import factory
from .models import *

class CatFactFactory(factory.DictFactory):
    # class Meta:
    #     model = CatFact

    fact = factory.Faker('sentence',nb_words=15)
    length = factory.Faker('random_int')

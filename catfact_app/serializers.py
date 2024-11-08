from rest_framework import serializers
from .models import *

# class CatFactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CatFact
#         fields = ['fact','length']

class CatFactSerializer(serializers.Serializer):
    fact = serializers.CharField(max_length = 500)
    length = serializers.IntegerField()

    def validate_fact(self, value):
        if not value:
            raise serializers.ValidationError("Fact cannot be Empty.")
        return value
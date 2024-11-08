from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

class CatFactView(APIView):
    def get(self, request):
        url = 'https://catfact.ninja/fact'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # cat_fact = CatFact.objects.create(fact=data['fact'], length=data['length'])

            serializer = CatFactSerializer(data)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data,status = status.HTTP_201_CREATED)
        else:
            return Response({"detail":"Failed to get cat Fact"},status=status.HTTP_400_BAD_REQUEST)


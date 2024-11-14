from django.shortcuts import render
import requests
import logging
# from rest_framework.response import Response
# from rest_framework import status
from .models import *
from .serializers import *
from django.conf import settings

logger = logging.getLogger(__name__)

class CatFactView:
    @classmethod
    def addFacts(self):
        logger.info("Fetching cat fact...")

        url = settings.FETCH_URL
        if not settings.FETCH_FLAG:
            logger.info("Fetch is disabled in settings")
            return
        resultData = []
        for i in range(10):

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                serializer = CatFactSerializer(data=data)
                if serializer.is_valid():
                    logger.info(f"Serializer data is valid : {serializer.validated_data}")
                    serializer.save()
                    logger.info(f"CatFact saved successfully: {serializer.validated_data}")
                    resultData.append(serializer.validated_data)

                else:
                    logger.error(f"Serializer validation failed: {serializer.errors}")
            else:
                logger.error(f"Failed to fetch data from API. Status code: {response.status_code}")  
        return resultData                  






# class CatFactView(APIView):
#     def get(self, request):

#         url = settings.FETCH_URL
#         if not settings.FETCH_FLAG:
#             return Response({"fetch is diabled in settings"})
#         response = requests.get(url)

#         if response.status_code == 200:
#             data = response.json()
#             serializer = CatFactSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"detail": "Failed to get cat fact"}, status=status.HTTP_400_BAD_REQUEST)
        
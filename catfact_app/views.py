# from django.shortcuts import render
# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import *
# from .serializers import *
# from django.conf import settings


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
        

# # class CatFactView(APIView):
# #     def get(self, request):
# #         url = 'https://catfact.ninja/fact'
# #         response = requests.get(url)

# #         if response.status_code == 200:
# #             data = response.json()
# #             # cat_fact = CatFact.objects.create(fact=data['fact'], length=data['length'])

# #             serializer = CatFactSerializer(data)
# #             if serializer.is_valid():
# #                serializer.save()
# #                return Response(serializer.data,status = status.HTTP_201_CREATED)
# #         else:
# #             return Response({"detail":"Failed to get cat Fact"},status=status.HTTP_400_BAD_REQUEST)        

# import logging
# import requests
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import CatFactSerializer

# # Set up logger
# logger = logging.getLogger(__name__)

# class CatFactView(APIView):
#     def get(self, request):
#         # Log the initial request
#         logger.info("Received request to fetch cat fact.")

#         # Check the FETCH_FLAG in settings
#         if not settings.FETCH_FLAG:
#             logger.warning("Fetch is disabled in settings.")
#             return Response({"detail": "Fetch is disabled in settings."}, status=status.HTTP_400_BAD_REQUEST)

#         url = settings.FETCH_URL
#         try:
#             response = requests.get(url)

#             # Log the status code of the response
#             logger.info(f"Received response with status code: {response.status_code}")

#             if response.status_code == 200:
#                 data = response.json()
#                 serializer = CatFactSerializer(data=data)

#                 # Log the received data
#                 logger.info(f"Data received: {data}")

#                 if serializer.is_valid():
#                     # Log successful save
#                     logger.info("Serializer is valid, saving data to the database.")
#                     serializer.save()

#                     # Log successful response
#                     logger.info(f"Successfully saved data: {serializer.data}")
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 else:
#                     # Log serializer errors
#                     logger.error(f"Serializer errors: {serializer.errors}")
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 # Log error if response status is not 200
#                 logger.error(f"Failed to fetch data, response status code: {response.status_code}")
#                 return Response({"detail": "Failed to get cat fact"}, status=status.HTTP_400_BAD_REQUEST)

#         except requests.exceptions.RequestException as e:
#             # Log any errors during the request
#             logger.error(f"Error during the request: {str(e)}")
#             return Response({"detail": "Error fetching cat fact"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import logging
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CatFactSerializer

# Set up logger
logger = logging.getLogger(__name__)

class CatFactView(APIView):
    def get(self, request):
        # Log the initial request
        logger.info("Received request to fetch cat fact.")

        # Check if fetching is disabled via FETCH_FLAG
        if not settings.FETCH_FLAG:
            logger.warning("Fetch is disabled in settings.")
            return  # Simply log the warning, no response returned

        url = settings.FETCH_URL
        try:
            # Send the request to the external API
            response = requests.get(url)

            # Log the status code of the response
            logger.info(f"Received response with status code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                serializer = CatFactSerializer(data=data)

                # Log the received data
                logger.info(f"Data received: {data}")

                if serializer.is_valid():
                    # Log successful save
                    logger.info("Serializer is valid, saving data to the database.")
                    serializer.save()

                    # Log successful data saving
                    logger.info(f"Successfully saved data: {serializer.data}")
                else:
                    # Log serializer errors
                    logger.error(f"Serializer errors: {serializer.errors}")
                    return  # No response returned, just log the error
            else:
                # Log error if the external API request fails (non-200 status code)
                logger.error(f"Failed to fetch data, response status code: {response.status_code}")
                return  # Log the error and stop the flow

        except requests.exceptions.RequestException as e:
            # Log error during the request
            logger.error(f"Error during the request: {str(e)}")
            return  # Log the exception and stop the flow


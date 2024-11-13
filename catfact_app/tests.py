from django.conf import settings
from rest_framework.test import APITestCase
from django.core.exceptions import ImproperlyConfigured
from catfact_app.views import CatFactView
from .factories import *
from .serializers import * 
from faker import Faker
import logging
from django.test.utils import override_settings
from unittest.mock import patch, MagicMock
# from django.urls import reverse
# from rest_framework import status
    
class CatFactSerializerTestCase(APITestCase):
    def setUp(self):
        self.fake = Faker()

    def test_serializer_valid_data(self):
        data = {
            'fact': self.fake.sentence(nb_words=15),
            'length': self.fake.random_int()
        }
        serializer = CatFactSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_serializer_invalid_data(self):
        invalid_data = {
            'fact': '',
            'length': self.fake.random_int()
        }
        serializer = CatFactSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())


class TestFetchSettings(APITestCase): 
    @override_settings(FETCH_URL=123,FETCH_FLAG="false")   
    def test_invalid_fetch_url_and_flag(self):  
        
        with self.assertRaises(ImproperlyConfigured):
            if not isinstance(settings.FETCH_URL, str):
                raise ImproperlyConfigured("FETCH_URL must be a string")
            if not isinstance(settings.FETCH_FLAG, bool):
                raise ImproperlyConfigured("FETCH_FLAG must be a boolean")
    
    @override_settings(FETCH_URL="https://api.example.com/cat-fact", FETCH_FLAG=True)
    def test_valid_fetch_url_and_flag(self):
        self.assertIsInstance(settings.FETCH_URL, str)
        self.assertIsInstance(settings.FETCH_FLAG, bool)

class CatFactViewTestCase(APITestCase):    
    @override_settings(FETCH_FLAG=False)
    def test_add_facts_with_fetch_disabled(self):
        with patch('logging.Logger.info') as mock_logger:
            result = CatFactView.addFacts()
            mock_logger.assert_any_call("Fetch is disabled in settings")
            self.assertIsNone(result)

    @override_settings(FETCH_FLAG=True, FETCH_URL="https://api.example.com/cat-fact")
    @patch('requests.get')
    def test_add_facts_successful_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'fact': 'Cats have five toes on their front paws.',
            'length': 40
        }
        mock_get.return_value = mock_response        
        with patch('logging.Logger.info') as mock_logger:
            result = CatFactView.addFacts()
            self.assertEqual(len(result), 10)
            self.assertTrue(CatFact.objects.filter(fact='Cats have five toes on their front paws.').exists())
            mock_logger.assert_any_call("Fetching cat fact...")
            self.assertTrue(
                any(call[0][0].startswith("CatFact saved successfully:") for call in mock_logger.call_args_list)
            )


    @override_settings(FETCH_FLAG=True, FETCH_URL="https://api.example.com/cat-fact")
    @patch('requests.get')
    def test_add_facts_failed_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with patch('logging.Logger.error') as mock_logger:
            result = CatFactView.addFacts()
            self.assertEqual(result, [])
            mock_logger.assert_called_with("Failed to fetch data from API. Status code: 404")


    @override_settings(FETCH_FLAG=True, FETCH_URL="https://api.example.com/cat-fact")
    @patch('requests.get')
    def test_add_facts_multiple_success_responses(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'fact': 'Cats sleep 70% of their lives.',
            'length': 40
        }
        mock_get.return_value = mock_response

        with patch('logging.Logger.info') as mock_logger:
            result = CatFactView.addFacts()
            self.assertEqual(len(result), 10)  
            self.assertEqual(CatFact.objects.count(), 10) 
            self.assertTrue(
            any(call[0][0].startswith("CatFact saved successfully:") for call in mock_logger.call_args_list)
        )
        
# class CatFactViewTestCase(APITestCase):
#     def setUp(self):
#         self.fake = Faker()

#     # @patch('requests.get')
#     def test_fetch_cat_fact_view(self):
#         with patch("requests.get") as mock_get:
#             mock_data = {
#                 'fact': self.fake.sentence(nb_words=15),
#                 'length': self.fake.random_int(min=10, max=150) 
#             }
#             mock_get.return_value.status_code = 200
#             mock_get.return_value.json.return_value = mock_data
#             response = self.client.get(reverse('fetch_cat_fact'))
#             self.assertEqual(response.status_code, 201)  
#             self.assertEqual(response.json()['fact'], mock_data['fact'])
#             self.assertEqual(response.json()['length'], mock_data['length'])
#             self.assertTrue(CatFact.objects.filter(fact=mock_data['fact']).exists())

#     # @patch('requests.get')
#     def test_fetch_cat_fetch_view_failure(self):
#         with patch("requests.get") as mock_get:
#             mock_get.return_value.status_code = 500
#             response = self.client.get(reverse('fetch_cat_fact')) 
#             self.assertEqual(response.status_code, 400)
#             self.assertEqual(response.json()['detail'], "Failed to get cat fact")
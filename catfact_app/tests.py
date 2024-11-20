from django.conf import settings
from rest_framework.test import APITestCase
from django.core.exceptions import ImproperlyConfigured
from catfact_app.views import CatFactView
from .factories import *
from .serializers import *
from faker import Faker
import requests
from django.test.utils import override_settings
from unittest.mock import patch, MagicMock
# from django.urls import reverse
# from rest_framework import status
    
class CatFactSerializerTestCase(APITestCase):
    '''Testing the serializers'''
    def setUp(self):
        self.fake = Faker()

    def test_serializer_valid_data(self):
        '''Chechking the serializer with the valid data'''
        data = {
            'fact': self.fake.sentence(nb_words=15),
            'length': self.fake.random_int()
        }
        serializer = CatFactSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_serializer_invalid_data(self):
        '''verifying the serializer by providing the invalid data'''
        invalid_data = {
            'fact': '',
            'length': self.fake.random_int()
        }
        serializer = CatFactSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
     


class TestFetchSettings(APITestCase): 
    def test_invalid_fetch_settings(self):
        '''Verifies error message response of CatFactView on absence of FETCH_URL and FETCH_FLAG'''
        error = "FETCH_URL and FETCH_FLAG must be valid"
        test_cases = [
        {"FETCH_URL": "ht5656we", "FETCH_FLAG": False},
        {"FETCH_URL": None, "FETCH_FLAG": True},
        {"FETCH_URL": "ht5656we.", "FETCH_FLAG": None},
        {"FETCH_URL": "ht5656we.", "FETCH_FLAG": []},
        {"FETCH_URL": "ht5656we.", "FETCH_FLAG":0},
        {"FETCH_URL": "ht5656we.", "FETCH_FLAG":''}, 
        ]
        for case in test_cases:
            with self.subTest(case=case):
                with self.settings(FETCH_URL=case["FETCH_URL"], FETCH_FLAG=case["FETCH_FLAG"]):
                    with self.assertRaises(ImproperlyConfigured) as im:
                        CatFactView.addFacts()
                    self.assertEqual(str(im.exception), error)
    
    @override_settings(FETCH_URL="https://api.example.com/cat-fact", FETCH_FLAG=True)
    def test_valid_fetch_url_and_flag(self):
        self.assertIsInstance(settings.FETCH_URL, str)
        self.assertIsInstance(settings.FETCH_FLAG, bool)

class CatFactViewTestCase(APITestCase):    
    
    def test_invalid_bool_string_settings(self):
        error = "FETCH_URL must be a string and FETCH_FLAG must be a boolean"
        test_cases = [
        {"FETCH_URL": "ht5656we", "FETCH_FLAG": "false"},
        {"FETCH_URL": 345, "FETCH_FLAG": True},
        ]
        for case in test_cases:
            with self.subTest(case=case):
                with self.settings(FETCH_URL=case["FETCH_URL"], FETCH_FLAG=case["FETCH_FLAG"]):
                    with self.assertRaises(ImproperlyConfigured) as cm:
                        CatFactView.addFacts()
                    self.assertEqual(str(cm.exception), error)

    def test_add_facts_url_flag_successful_response(self):
        '''Verifies successful response of FetchCatFactView on valid FETCH_URL and FETCH_FLAG'''
        with self.settings(FETCH_URL="ejhfw", FETCH_FLAG=True):
            self.assertIsInstance(settings.FETCH_URL, str)
            self.assertIsInstance(settings.FETCH_FLAG, bool)  
            with patch('requests.get') as mock_get:
                # Mock successful API response
                mock_data = CatFactFactory()
                mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_data)
                result = CatFactView.addFacts()
                # Validate facts saved to the database
                saved_facts = CatFact.objects.all()
                self.assertEqual(len(saved_facts), 10) 
                self.assertEqual(len(result), 10)   
                for fact in saved_facts:
                    self.assertEqual(fact.fact, mock_data['fact'])
                    self.assertEqual(fact.length, mock_data['length'])

    # @override_settings(FETCH_FLAG=True, FETCH_URL="https://api.example.com/cat-fact")
    # @patch('requests.get')
    def test_add_facts_multiple_success_responses(self):
        with self.settings(FETCH_URL="https://api.example.com/cat-fact", FETCH_FLAG=True):
            with patch("requests.get") as mock_get:
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
    
    def test_network_error_handling(self):
        with self.settings(FETCH_URL="url", FETCH_FLAG=True):
            with patch('requests.get') as mock_get:
                # Mock a network error
                mock_get.side_effect = requests.exceptions.RequestException("Network Error")
                result = CatFactView.addFacts()
                self.assertEqual(result, [])
                mock_get.assert_called()
                
    def test_unexpected_error_handling(self):
        with self.settings(FETCH_URL="url", FETCH_FLAG=True):
            with patch('requests.get') as mock_get:
                # Mock an unexpected exception
                mock_get.side_effect = Exception("Unexpected Error")
                result = CatFactView.addFacts()
                self.assertEqual(result, [])  # No facts should be saved on error
                mock_get.assert_called()

    def test_http_error_handling(self):
        with self.settings(FETCH_URL="url", FETCH_FLAG=True):
            with patch('requests.get') as mock_get:
                # Mock a 404 Not Found response
                mock_response = MagicMock()
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
                mock_response.status_code = 404
                mock_get.return_value = mock_response
                result = CatFactView.addFacts()
                self.assertEqual(result, [])
                mock_get.assert_called()            
            
        
from rest_framework.test import APITestCase
from .factories import *
from .serializers import * 
from faker import Faker
from django.urls import reverse
from unittest.mock import patch
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

# class CatFactViewTestCase(APITestCase):
#     @patch('requests.get')
#     def test_fetch_cat_fact_view(self, mock_get):
#         cat_fact = CatFactFactory.create()

#         mock_data = {
#             'fact': cat_fact,
#             'length': cat_fact
#         }
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = mock_data

#         response = self.client.get(reverse('fetch_cat_fact'))

#         self.assertEqual(response.status_code,201)

#         self.assertEqual(response.json()['fact'],mock_data['fact'])
#         self.assertEqual(response.json()['length'],mock_data['length'])

#         self.assertTrue(CatFact.objects.filter(fact=mock_data['fact']).exists())

class CatFactViewTestCase(APITestCase):
    def setUp(self):
        self.fake = Faker()

    @patch('requests.get')
    def test_fetch_cat_fact_view(self, mock_get):
        mock_data = {
            'fact': self.fake.sentence(nb_words=15),
            'length': self.fake.random_int(min=10, max=150) 
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        response = self.client.get(reverse('fetch_cat_fact'))

        self.assertEqual(response.status_code, 201)  
        self.assertEqual(response.json()['fact'], mock_data['fact'])
        self.assertEqual(response.json()['length'], mock_data['length'])

        self.assertTrue(CatFact.objects.filter(fact=mock_data['fact']).exists())

    @patch('requests.get')
    def test_fetch_cat_fetch_view_failure(self, mock_get):
        mock_get.return_value.status_code = 500

        response = self.client.get(reverse('fetch_cat_fact')) 

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Failed to get cat fact")





# class CatFactSerializerTestCase(APITestCase):
#     def test_serializer_valid_data(self):
#         cat_fact = CatFactFactory.create()

#         serializer = CatFactSerializer(cat_fact)

#         self.assertEqual(serializer.data["fact"],cat_fact.fact)
#         self.assertEqual(serializer.data["length"],cat_fact.length)

#     def test_serializer_invalid_data(self):
#         data = {'fact': 'This is cat fact'}
#         serializer = CatFactSerializer(data=data)

#         self.assertFalse(serializer.is_valid())
#         self.assertIn('length',serializer.errors)
# coding: utf-8

import json
from django.test import TestCase

from people.models import Person
from people.serializer import PersonSerializer
from people.views import ObtainAuthToken

from model_mommy import mommy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


class PersonTestSerializer(APITestCase):

    def setUp(self):
        self.data = {
            "email": "teste@teste.com",
        }
        self.manager = PersonSerializer()

    def test_create_user_serializer(self):
        response = self.client.post('/v1/people/', data=self.data)
        pk = json.loads(response.content.replace("'", "\""))['id']
        self.person = Person.objects.get(id=pk)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.person.id, 1)

    def test_update_user_serializer(self):
        user = mommy.make(Person)
        token = mommy.make(Token, user=user)
        self.client = APIClient()
        response = self.client.put('/v1/people/1/', data={"name":"Foo"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Foo')

class ObtainAuthTokenTestSerializer(TestCase):
    
    def setUp(self):
        self.manager = ObtainAuthToken()
        self.data = {
            "email": "teste@teste.com",
        }
        response = self.client.post('/v1/people/', data=self.data)
        self.person = json.loads(response.content.replace("'", "\""))

    def test_generate_token_with_facebook(self):
        response = self.client.post('/v1/api-token-auth/', data=self.data)
        token = json.loads(response.content.replace("'", "\""))
        self.assertIsNotNone(token)


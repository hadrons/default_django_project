#coding: utf-8

from django import forms
from django.test import TestCase

from mock import patch, MagicMock

from people.models import PersonManager, Person
from people.forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase):

	def setUp(self):
		self.form = CustomUserCreationForm()
		self.manager = PersonManager()
		self.manager.model = Person

	def test_clean_password_valid(self):
		self.form.cleaned_data = {}
		self.form.cleaned_data['password1'] = '123'
		self.form.cleaned_data['password2'] = '123'
		resposta = self.form.clean_password2()
		esperado = '123'
		self.assertEqual(esperado, resposta)

	def test_clean_password_invalid(self):
		self.form.cleaned_data = {}
		self.form.cleaned_data['password1'] = '123'
		self.form.cleaned_data['password2'] = '312'

		with self.assertRaises(forms.ValidationError):
			resposta = self.form.clean_password2()
	
	def test_clean_email_valid(self):
		self.form.cleaned_data = {}
		self.form.cleaned_data['email'] = 'foo@foo.com'
		resposta = self.form.clean_email()
		esperado = 'foo@foo.com'
		self.assertEqual(esperado, resposta)

	def test_clean_email_invalid(self):
		user = self.manager.create_user('foo@foo.com','1234')
		self.form.cleaned_data = {}
		self.form.cleaned_data['email'] = 'foo@foo.com'
		
		with self.assertRaises(forms.ValidationError):
			resposta = self.form.clean_email()
#coding: utf-8
from django.test import TestCase

from people.models import PersonManager, Person

from mock import patch, MagicMock

class PersonManagerTest(TestCase):

	def setUp(self):
		self.manager = PersonManager()
		self.manager.model = Person

	def test_create_user_without_email(self):
		with self.assertRaises(ValueError):
			self.manager.create_user('', '')

	def teste_create_user_without_email_password(self):
		with self.assertRaises(ValueError):
			self.manager.verify_if_has_email_and_password('', '')

	@patch('people.models.AbstractBaseUser.set_password')
	def test_if_set_password_has_calls(self, _set_password):
		self.manager.create_user(email='foo@foo.com', password='1234')
		_set_password.assert_called_once_with('1234')

	@patch('people.models.AbstractBaseUser.save')
	def test_if_save_has_calls(self, _save):
		self.manager.create_user('foo@foo.com', '1234')
		_save.assert_called_once_with(using=self.manager._db)

	@patch('people.models.AbstractBaseUser.save')
	def test_create_user_and_return(self, _save):
		self.manager._db = MagicMock(Person)
		resposta = self.manager.create_user('foo@foo.com','1234')
		esperado = _save.assert_called_once_with(using=self.manager._db)
		user = Person.objects.filter(id=1).first()
		self.assertEqual(esperado, user)

	@patch('people.models.PersonManager.create_user')
	def test_create_super_user_call_create_user(self, _create_user):
		self.manager.create_superuser('foo@foo.com', '1234')
		_create_user.assert_called_once_with(email='foo@foo.com',
			password='1234')

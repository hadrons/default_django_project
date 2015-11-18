# coding: utf-8

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.utils.encoding import smart_str, smart_text

class PersonManager(BaseUserManager):

    def verify_if_has_email_and_password(self, email, password):
        if not email and not password:
            raise ValueError('Users must have an email and password')
        

    def create_user(self, email, password):

        self.verify_if_has_email_and_password(email, password)

        user = self.model(email=email)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    )
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    name = models.CharField(max_length=255, verbose_name="Nome", blank=True)
    cellular = models.CharField(max_length=13, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=10,choices=GENDER, blank=True, null=True)
    
    objects = PersonManager()
    USERNAME_FIELD = 'email'


    def __unicode__(self):
        return self.name or ''

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

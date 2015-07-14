from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_base',
        'USER': 'root'        
    }
}

DEBUG = False
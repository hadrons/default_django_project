from .settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'dbname',
#         'HOST': 'localhost', #or host database
#         'USER': 'dbuser',
#         'PASSWORD': 'dbpassword',
#     }
# }

MEDIA_ROOT = '/home/webapps/default/media'
STATIC_ROOT = '/home/webapps/default/static_collected'
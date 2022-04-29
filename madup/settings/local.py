import os
from dotenv import load_dotenv

from .base import *


load_dotenv()

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'madup',
        'USER': 'root',
        'PASSWORD': os.environ.get("MYSQL_LOCAL_PASSWORD"),
        'HOST': 'localhost',
        'PORT': 3306
    }
}
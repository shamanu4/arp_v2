# -*- coding: utf-8 -*-

SECRET_KEY = '**************************************************'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password'
        }
}
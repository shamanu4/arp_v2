# -*- coding: utf-8 -*-

SECRET_KEY = 'Cql3kqsq-8y!gwqzt=7h=6#r)g=rs+ifv#zm)lbn&no*kqfu=&'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'arpv2',
        'USER': 'arpv2geouser',
        'PASSWORD': 'geo13arpv2ifvzMlBnno'
        }
}
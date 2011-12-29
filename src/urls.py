from django.conf.urls.defaults import *

from settings import MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^biltv/', include('biltv.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',     
        {'document_root': MEDIA_ROOT}),
    (r'^favicon.ico$', 'django.views.static.serve', 
        {'document_root': MEDIA_ROOT, 'path':'favicon.ico'}),
    (r'^admin/', include(admin.site.urls)),
)

from django.conf.urls.defaults import *
from tests_42cc import settings
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),    
    (r'^', include('tickets.urls')),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root' : os.path.join(settings.CURRENT_PATH, 'static') }),
)

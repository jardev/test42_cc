from django.conf.urls.defaults import *

urlpatterns = patterns('tests_42cc.ticket1.views',
    (r'^$', 'index', { 'template_name' : 'tickets/index.html' }, 'ticket1_home'),
)


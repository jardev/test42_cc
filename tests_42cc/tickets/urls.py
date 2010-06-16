from django.conf.urls.defaults import *

urlpatterns = patterns('tests_42cc.tickets.views',
    (r'^$', 'index', { 'template_name' : 'tickets/index.html' }, 'tickets_home'),
    (r'^edit/', 'edit'),
)


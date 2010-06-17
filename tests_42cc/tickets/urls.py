from django.conf.urls.defaults import *

urlpatterns = patterns('tests_42cc.tickets.views',
    (r'^$', 'index', { 'template_name' : 'tickets/index.html' }, 'tickets_home'),
    (r'^edit/', 'edit'),
    (r'^accounts/logout/$', 'do_logout'),
    (r'^http-log/', 'view_http_log'),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'tickets/login.html'}),
)


from django.conf.urls.defaults import *

urlpatterns = patterns('tests_42cc.tickets.views',
    url(r'^$', 'index', name='tickets_home'),
    url(r'^edit/', 'edit', name='tickets_edit'),
    url(r'^accounts/logout/$', 'do_logout', name='tickets_logout'),
    url(r'^http-log/$', 'view_http_log', kwargs={ 'priority' : 1 }, name='tickets_http_log'),
    url(r'^http-log/(?P<priority>\d+)/$', 'view_http_log'),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'tickets/login.html'}),
)


from django.conf.urls.defaults import *

urlpatterns = patterns('timer.views',
    url(r'^stop/$', 'stop_timer', name='stop_timer'),
    url(r'^start/$', 'start_timer', name='start_timer'),
    url(r'^set/(?P<id>\d+)/$', 'set_time_record', name='set_time_record'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('timer.views',
    url(r'^stop/$', 'stop_timer', name='stop_timer'),
    url(r'^start/$', 'start_timer', name='start_timer'),
    url(r'^set/(?P<id>\d+)/$', 'set_time_record', name='set_time_record'),
    url(r'^delete/(?P<id>\d+)/$', 'delete_timer', name='delete_timer'),
    url(r'^all/$', 'time_records_view', name='time_records_view'),
    url(r'^today/$', 'today_time_records_view', name='today_time_records_view'),
    url(r'^yesterday/$', 'yesterday_time_records_view', name='yesterday_time_records_view'),
    url(r'^last_week/$', 'last_week_time_records_view', name='last_week_time_records_view'),
    url(r'^add/$', 'add_time_record_view', name='add_time_record_view'),
)


from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'^/$', 'project_view', name='project_view'),
)

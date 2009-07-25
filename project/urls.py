from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'^all/$', 'project_list_view', name='project_list_view'),
    url(r'^add/$', 'add_project_view', name='add_project_view'),
    url(r'^mine/$', 'my_projects_list_view', name='my_projects_list_view'),
    url(r'^detail/(?P<id>\d+)/$', 'project_detail_view', name='project_detail_view'),
    url(r'^spectator/(?P<project_id>\d+)/$', 'add_remove_spectator', name='add_remove_spectator'),
    url(r'^collaborator/(?P<project_id>\d+)/$', 'add_remove_collaborator', name='add_remove_collaborator'),
    url(r'^owner/(?P<project_id>\d+)/$', 'add_remove_owner', name='add_remove_owner'),
)



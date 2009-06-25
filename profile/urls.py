from django.conf.urls.defaults import *

urlpatterns = patterns('profile.views',
    url(r'^login/$', 'login_view', name='login_view'),
    url(r'^logout/$', 'logout_view', name='logout_view'),
    url(r'^register/$', 'register_view', name='register_view'),
    url(r'^me/$', 'profile_view', name='profile_view'),
    url(r'^password/$', 'password_view', name='password_view'),
    url(r'^confirm/(?P<key>[0-9a-z\-]+)/$', 'register_confirm', name='register_confirm'),
    #url(r'^new_account/$', 'create_account', name='profile_create_account'),
    #url(r'^accept_invitation/([\w-]+)/$', 'accept_invitation', name='profile_accept_invitation'),
)

urlpatterns += patterns('',
    url(r'^new_account/confirm/$', 'django.views.generic.simple.direct_to_template', {'template':'profile/new_account_confirm.html'}, name='profile_new_account_confirm'),
)

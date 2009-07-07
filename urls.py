from django.conf.urls.defaults import *
from profile.forms import PasswordResetForm
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^profile/', include('profile.urls')),
    (r'^contact/', include('contact.urls')),
    (r'^notification/', include('notification.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'password/password_reset_form.html', 'email_template_name':'email/password_reset_email.txt', 'password_reset_form':PasswordResetForm}, name="password_reset"),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'password/password_reset_done.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'password/password_reset_confirm.html'}),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'password/password_reset_complete.html'}),

)

urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'redirect_to', {'url': '/profile/me/'}),
    )   


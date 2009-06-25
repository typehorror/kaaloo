from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^profile/', include('profile.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns+=patterns('django.views.generic.simple',
    url(r'^$','direct_to_template', {'template': 'base.html'}, name='base_template'),
)


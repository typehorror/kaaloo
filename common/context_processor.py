def static_processor(request):
    from django.conf import settings
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    return {'STATIC_URL': settings.STATIC_URL,
            'SITE_URL': site.domain}


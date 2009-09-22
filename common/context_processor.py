def static_processor(request):
    from django.conf import settings
    from django.contrib.sites.models import Site
    from timer.models import TimeRecord
    site = Site.objects.get_current()
    time_record = TimeRecord.objects.get_time_record(request)
    time_records = TimeRecord.objects.get_time_records(request)
    return {'TIME_RECORD': time_record,
            'TIME_RECORDS': time_records,
            'STATIC_URL': settings.STATIC_URL,
            'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,
            'DEFAULT_EMAIL_FROM': settings.DEFAULT_EMAIL_FROM,
            'SITE_URL': site.domain}


from django import template
from django.utils.translation import ugettext as _
from exceptions import Exception
register = template.Library()

@register.inclusion_tag('status.html')
def user_status(user):
    from timer.models import TimeRecord
    status = _('Unknow')
    time_record = None
    try:
        time_record = TimeRecord.objects.get(user=user, stop_date=None)
        status = _('Working on %s') % (time_record.title)
    except TimeRecord.DoesNotExist, e :
        status = _('On Pause')
    return {'status':status, 'time_record':time_record}

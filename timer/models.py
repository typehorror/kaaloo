from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from task.models import Task, Goal

class TimeRecordManager(models.Manager):
    def get_time_record(self, request, auto_create=False, id=None):
        if id is not None:
            kw_filter = {'id': id}
        else:
            kw_filter = {'stop_date': None}
        if request.user.is_authenticated():
            kw_filter['user'] = request.user
        else:
            kw_filter['user'] = None
            kw_filter['pk__in'] = request.session.get('tr_ids',[]) or []
        time_records = self.filter(**kw_filter)

        if time_records:
            return time_records[0]
        elif auto_create:
            if request.user.is_authenticated():
                return self.create(user=request.user)
            else:
                time_record = self.create()
                if request.session.get('tr_ids'):
                    request.session['tr_ids'].append(time_record.id)
                else:
                    request.session['tr_ids'] = [time_record.id,]
                request.session.modified = True
                return time_record
        return None

    def get_time_records(self, request):
        if request.user.is_authenticated():
            return self.filter(user=request.user).order_by('-start_date')
        else:
            return self.filter(user=None, pk__in=request.session.get('tr_ids',[])).order_by('-start_date')



class TimeRecord(models.Model):
    user =  models.ForeignKey(User, null=True, related_name='time_records')
    task = models.ForeignKey(Task, null=True, related_name='time_records')
    title = models.CharField(max_length=50, default="untitled")
    description = models.TextField(blank=True, null=True)
    goals_achieved = models.ManyToManyField(Goal, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    stop_date = models.DateTimeField(blank=True, null=True)

    objects = TimeRecordManager()

    @property
    def seconds(self):
        #import pdb; pdb.set_trace()
        if self.stop_date:
            time_delta = self.stop_date - self.start_date
            return time_delta.seconds + (time_delta.days * 24 * 3600)
        else:
            time_delta = datetime.now() - self.start_date
            return time_delta.seconds + (time_delta.days * 24 * 3600)
    

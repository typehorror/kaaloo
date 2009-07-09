from django.db import models
from django.contrib.auth.models import User

from task.models import Task, Goal

class TimeRecord(models.Model):
    user =  models.ForeignKey(User, null=True, related_name='time_records')
    task = models.ForeignKey(Task, null=True, related_name='time_records')
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    goals_achieved = models.ManyToManyField(Goal, null=True, limit_choices_to={'task__goals__status':0})
    start_date = models.DateTimeField(auto_now_add=True)
    stop_date = models.DateTimeField(blank=True, null=True)

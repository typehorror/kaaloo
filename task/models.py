from django.db import models
from django.contrib.auth.models import User


from project.models import Project


STATUS_CHOICES = (
    ('active', 'Active'),
    ('stopped', 'Stopped'),
    ('to_delete', 'Marked For Deletion'),
)

class Task(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True)
    owners =  models.ManyToManyField(User, related_name='tasks')
    collaborators =  models.ManyToManyField(User, related_name='tasks_as_colaborator', null=True, blank=True, limit_choices_to = {'owners__contacts__user__is_active': 1})
    spectators = models.ManyToManyField(User, related_name='tasks_as_spectator', null=True, blank=True, limit_choices_to = {'owners__contacts__user__is_active': 1})
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    description = models.TextField(blank=True)
    title = models.CharField(max_length=50)



class Goal(models.Model):
    task = models.ForeignKey(Task, related_name="tasks")
    title = models.CharField(max_length=50)
    done = models.BooleanField(default=False)

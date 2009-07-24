from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

STATUS_CHOICES = (
    ('active', 'Active'),
    ('stopped', 'Stopped'),
    ('to_delete', 'Marked For Deletion'),
)
class ProjectManager(models.Manager):
    def for_user(self, user):
        return self.filter(Q(owners=user)|Q(collaborators=user)|Q(spectators=user)).distinct()

class Project(models.Model):
    owners =  models.ManyToManyField(User, related_name='projects')
    collaborators = models.ManyToManyField(User, related_name='projects_as_collaborator', null=True, blank=True)#, limit_choices_to = {'owners__contacts__user__is_active': 1})
    spectators = models.ManyToManyField(User, related_name='projects_as_spectator', null=True, blank=True)#, limit_choices_to = {'owners__contacts__user__is_active': 1})
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    description = models.TextField(blank=True)
    title = models.CharField(max_length=50)

    objects = ProjectManager()

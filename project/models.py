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
        return self.filter(Q(creator=user)|Q(owners=user)|Q(collaborators=user)|Q(spectators=user)).distinct()

    def write_access(self, user, id):
        return self.filter(Q(creator=user)|Q(owners=user)).distinct().get(id=id)
    
    def get_for_user(self, user, id):
        #import pdb; pdb.set_trace()
        return self.filter(Q(creator=user)|Q(owners=user)|Q(collaborators=user)|Q(spectators=user)).distinct().get(id=id)
    

class Project(models.Model):
    creator = models.ForeignKey(User, related_name='projects')
    owners =  models.ManyToManyField(User, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, related_name='projects_as_collaborator', null=True, blank=True)#, limit_choices_to = {'owners__contacts__user__is_active': 1})
    spectators = models.ManyToManyField(User, related_name='projects_as_spectator', null=True, blank=True)#, limit_choices_to = {'owners__contacts__user__is_active': 1})
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    description = models.TextField(blank=True)
    title = models.CharField(max_length=50)

    objects = ProjectManager()

    def is_creator(self, user):
        return user == self.creator

    def is_admin(self, user):
        return self.is_creator(user) or user in self.owners.all()
    
    def is_collaborator(self, user):
        return self.is_admin(user) or user in self.collaborators.all()

    def is_spectator(self, user):
        return self.is_admin(user) or self.is_collaborator(user) or user in self.spectator.all()

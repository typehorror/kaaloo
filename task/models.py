from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    project = models.ForeignKey('project.Project', related_name='project_tasks', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)

    description = models.TextField(blank=True)
    title = models.CharField(max_length=50)

    @property
    def owners(self):
        return self.project.owners

    @property
    def collaborators(self):
        return self.project.collaborators

    @property
    def spectators(self):
        return self.project.spectators


class Goal(models.Model):
    task = models.ForeignKey('Task', related_name='tasks')
    title = models.CharField(max_length=50)
    done = models.BooleanField(default=False)

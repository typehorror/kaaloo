from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from project.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description')


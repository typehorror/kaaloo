from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db.models import Q


from common.tools import get_user_name

from project.models import Project
from django.contrib.auth.models import User

class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, user):
        return get_user_name(user)


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 
                  'description',
                  'status')

class ProjectOwnerForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('owners',)

class ProjectCollaboratorForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('collaborators',)

class ProjectSpectatorForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('spectators',)
    def __init__(self, user, *args, **kwargs):
        super(ProjectSpectatorForm, self).__init__(*args, **kwargs)
        profile = user.get_profile()
        self.fields['spectators'] = MyModelMultipleChoiceField(queryset=User.objects.filter(profile__contacts=profile))
        

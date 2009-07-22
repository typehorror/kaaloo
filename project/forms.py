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
                  'owners',
                  'collaborators',
                  'spectators',
                  'status')

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(Q(profile__contacts__user = self.instance.owners.all())|Q(id=self.instance.owners.all())).distinct()
        self.fields['owners'] = MyModelMultipleChoiceField(users,widget=forms.CheckboxSelectMultiple)
        self.fields['collaborators'] = MyModelMultipleChoiceField(users,widget=forms.CheckboxSelectMultiple)
        self.fields['spectators'] = MyModelMultipleChoiceField(users,widget=forms.CheckboxSelectMultiple)

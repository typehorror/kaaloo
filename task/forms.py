from django import forms
from django.utils.translation import ugettext as _


from models import Task, Goal

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',
                  'description',)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title',
                  'description',)

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title',
                  'is_done',)


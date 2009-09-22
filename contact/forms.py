from django import forms
from django.utils.translation import ugettext as _

from django.conf import settings

class AddContactForm(forms.Form):
    email = forms.EmailField()

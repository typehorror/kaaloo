from datetime import timedelta, datetime

from django.utils.translation import ugettext as _
from django import forms

from timer.models import TimeRecord

class CustomTimeForm(forms.ModelForm):
    duration = forms.CharField(max_length=50, initial='01:00:00', help_text=("( format: 01:23:45 )"))
    stop_date = forms.DateTimeField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = TimeRecord
        fields = ('title',
                  'description')

    def clean_duration(self):
        import re
        re_time = re.compile(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)', re.I)
        duration = self.cleaned_data['duration'].strip()
        time_result = re_time.search(duration)
        if time_result is None:
            raise forms.ValidationError(_("Please enter duration in format hh:mm:ss ."))
        time_result = time_result.groups()
        if len(time_result) == 3:
            t_delta = { 'hours': int(time_result[0]),
                        'minutes' : int(time_result[1]),
                        'seconds' : int(time_result[2]) }
            delta = timedelta(**t_delta)
            return delta
        else:
            raise forms.ValidationError(_("Please enter duration in format hh:mm:ss ."))

class CloseTimeRecordForm(forms.ModelForm):
    stop_date = forms.DateTimeField(widget=forms.HiddenInput)
    class Meta:
        model = TimeRecord
        fields = ('title',
                  'stop_date',
                  'description')
    def __init__(self, *args, **kwargs):
        super(CloseTimeRecordForm, self).__init__(*args, **kwargs)
        if self.instance.stop_date:
            seconds = self.instance.seconds        
            hours = int(seconds / 3600)
            minutes = int((seconds - hours * 3600) / 60);
            seconds = int(seconds % 60);
            self.fields['duration'] = forms.CharField(max_length=50,
                                                  initial='%02d:%02d:%02d' % (hours, minutes, seconds),
                                                  help_text=("( format: 01:23:45 )"))
    def clean_duration(self):
        import re
        re_time = re.compile(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)', re.I)
        duration = self.cleaned_data['duration'].strip()
        time_result = re_time.search(duration)
        if time_result is None:
            raise forms.ValidationError(_("Please enter duration in format 12:34:56 ."))
        time_result = time_result.groups()
        if len(time_result) == 3:
            t_delta = { 'hours': int(time_result[0]),
                       'minutes' : int(time_result[1]),
                       'seconds' : int(time_result[2]) }
            delta = timedelta(**t_delta)
            self.cleaned_data['stop_date'] = self.instance.start_date + delta
        else:
            raise forms.ValidationError(_("Please enter duration in format 12:34:56 ."))

        
class TimeRecordTitleForm(forms.ModelForm):
    class Meta:
        model = TimeRecord
        fields = ('title',)
          
class OpenTimeRecordForm(forms.ModelForm):
    class Meta:
        model = TimeRecord
        fields = ('title',
                  'description')

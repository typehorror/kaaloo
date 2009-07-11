from datetime import timedelta

from django.utils.translation import ugettext as _
from django import forms

from timer.models import TimeRecord


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
            hours = int(seconds / 3600 )
            minutes = int((seconds - hours * 3600) / 60);
            seconds = int(seconds % 60);
            self.fields['time'] = forms.CharField(max_length=50, initial='%02d:%02d:%02d' % (hours, minutes, seconds))
    def clean_time(self):
        import re
        re_time = re.compile(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)', re.I)
        time = self.cleaned_data['time'].strip()
        time_result = re_time.search(time)
        if time_result is None:
            raise forms.ValidationError(_("Please enter time in format 12:34:56 ."))
        time_result = time_result.groups()
        if len(time_result) == 3:
            t_delta = { 'hours': int(time_result[0]),
                       'minutes' : int(time_result[1]),
                       'seconds' : int(time_result[2]) }
            delta = timedelta(**t_delta)
            self.cleaned_data['stop_date'] = self.instance.start_date + delta
        else:
            raise forms.ValidationError(_("Please enter time in format 12:34:56 ."))

        
          
class OpenTimeRecordForm(forms.ModelForm):
    class Meta:
        model = TimeRecord
        fields = ('title',
                  'description')

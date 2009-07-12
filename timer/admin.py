from django.contrib import admin
from timer.models import TimeRecord

class TimeRecordAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'start_date')
    
admin.site.register(TimeRecord, TimeRecordAdmin)

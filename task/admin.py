from django.contrib import admin
from models import Task

class TaskAdmin(admin.ModelAdmin):
    search_fields = ( 'title', 'description', )
    list_display = ( 'id', 'title', 'project', 'creation_date')
    
admin.site.register(Task, TaskAdmin)

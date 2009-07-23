from django.contrib import admin
from project.models import Project

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ( 'title', 'description', )
    list_display = ( 'id', 'title', 'creation_date')
    
admin.site.register(Project, ProjectAdmin)

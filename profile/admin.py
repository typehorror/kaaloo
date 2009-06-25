from django.contrib import admin
from profile.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    #search_fields = ( 'user__first_name', 'user__email', 'user__last_name', )
    list_filter = ( 'country',)
    list_display = ( 'id', 'country', 'city')
    
admin.site.register(Profile, ProfileAdmin)

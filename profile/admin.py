from django.contrib import admin
from profile.models import Profile, Registration

class ProfileAdmin(admin.ModelAdmin):
    #search_fields = ( 'user__first_name', 'user__email', 'user__last_name', )
    list_filter = ( 'country',)
    list_display = ( 'id', 'country', 'city', 'user')
    
admin.site.register(Profile, ProfileAdmin)

class RegistrationAdmin(admin.ModelAdmin):
    search_fields = ( 'email', 'key' )
    list_display = ( 'email', 'key', 'creation_date')
    
admin.site.register(Registration, RegistrationAdmin)

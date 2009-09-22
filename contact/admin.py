from django.contrib import admin
from contact.models import ContactRequest, InviteRequest


class InviteRequestAdmin(admin.ModelAdmin):
    search_fields = ( 'from_user__email', 'to_email', 'key' )
    list_display = ( 'from_user', 'to_email', 'key', 'creation_date')

class ContactRequestAdmin(admin.ModelAdmin):
    search_fields = ( 'from_user__email', 'to_user__email', 'key' )
    list_display = ( 'from_user', 'to_user', 'key', 'creation_date')
    
admin.site.register(ContactRequest, ContactRequestAdmin)
admin.site.register(InviteRequest, InviteRequestAdmin)

from django.db import models
from common.tools import get_uuid
from django.contrib.auth.models import User

REQUEST_STATUS = (
    ('created','Created'),
    ('sent', 'Sent'),
    ('accepted','Accepted'),
    ('refused','Refused'),
    ('error','Error'),
)

class ContactRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="contact_requests_sent")
    to_user = models.ForeignKey(User, related_name="contact_requests_received")
    key = models.CharField(max_length=55, unique=True, db_index=True, default=get_uuid)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default="created")

    @models.permalink
    def get_absolute_url(self):
        return ('contact.views.contact_confirm_view', [str(self.key)])

    unique_together = (("from_user", "to_user"),)

class InviteRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="invite_requests")
    to_email = models.EmailField()
    key = models.CharField(max_length=55, unique=True, db_index=True, default=get_uuid)
    creation_date = models.DateTimeField(auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('contact.views.invite_confirm_view', [str(self.key)])
    
    unique_together = (("from_user", "to_email"),)

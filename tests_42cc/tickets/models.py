from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    biography = models.TextField()
    birthday = models.DateTimeField(blank=True)
    
    class Meta:
        ordering = ('last_name', 'first_name')
        
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
class ContactInfo(models.Model):
    CONTACT_TYPES = (('phone', 'Phone'),
                     ('email', 'E-Mail'),
                     ('icq',   'ICQ'),
                     ('skype', 'Skype'),
                     ('xmpp',  'XMPP'))
                    
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='email')
    contact = models.CharField(max_length=50)
    additional_info = models.TextField(blank=True)
    agent = models.ForeignKey(Agent)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('contact_type', 'contact')
    
    def __unicode__(self):
        # TODO: Rewrite using custom tags
        return self.get_contact_type_display() + ': ' + self.contact
        
class HttpRequestLogEntry(models.Model):
    host = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True)
    
        
        
        

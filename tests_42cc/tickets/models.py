from django.db import models

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
        
        
        

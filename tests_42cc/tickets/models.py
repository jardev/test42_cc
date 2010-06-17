from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

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
    
    def __unicode__(self):
        return "[%s] From %s %s %s" % (self.date, self.host, self.method, self.url)
    
class ModelActionLogEntry(models.Model):
    ACTION_INSERT = 0
    ACTION_EDIT = 1
    ACTION_DELETE = 2
    ACTION_TYPES = ((ACTION_INSERT, 'Insert'),
                    (ACTION_EDIT, 'Edit'),
                    (ACTION_DELETE, 'Delete'))
    
    action = models.SmallIntegerField(choices=ACTION_TYPES)
    when = models.DateTimeField(auto_now_add=True)
    model_class = models.CharField(max_length=255)
    model_module = models.CharField(max_length=255)
    model_id = models.CharField(max_length=255, blank=True, null=True)
    model_object = generic.GenericForeignKey('model_class', 'model_id')
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return "(%s) [%s]:%s %s" % (self.when, self.action, self.model_class, self.model_id)
    
from tests_42cc.tickets import listeners
listeners.start_default_listening()    
        
      

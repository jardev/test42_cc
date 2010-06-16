from django.contrib import admin
from tests_42cc.tickets.models import Agent, ContactInfo, ModelActionLogEntry

class AgentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birthday')
    list_display_links = ('last_name',)
    list_per_page = 50
    ordering = ['last_name']
    search_fields = ['first_name', 'last_name']
    
admin.site.register(Agent, AgentAdmin)

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'contact', 'agent', 'is_default', 'is_active')
    list_display_links = ('contact',)
    list_per_page = 20
    ordering = ['contact_type', 'contact']
    search_fields = ['contact']
    
class ModelActionLogEntryAdmin(admin.ModelAdmin):
    list_display = ('when', 'action', 'model_module', 'model_class', 'model_id',)
    list_display_links = ('model_id',)
    list_per_page = 100
    ordering = ['-when']
    search_fields = ['model_module', 'model_class']
    
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(ModelActionLogEntry, ModelActionLogEntryAdmin)
    

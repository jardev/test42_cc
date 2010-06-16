from django import forms
from django.forms.models import inlineformset_factory
from tests_42cc.tickets.models import Agent, ContactInfo

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('first_name', 'last_name', 'biography', 'birthday',)
        
ContactFormSet = inlineformset_factory(Agent, ContactInfo, can_delete=True)        
        

from django import forms
from tests_42cc.tickets.models import Agent, ContactInfo

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('first_name', 'last_name', 'biography', 'birthday',)
        

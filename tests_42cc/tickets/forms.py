from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets
from tests_42cc.tickets.models import Agent, ContactInfo, HttpRequestLogEntry

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent        
        fields = ['birthday', 'biography', 'last_name', 'first_name']
        widgets = {
            'birthday' : widgets.AdminDateWidget()
        }
               
ContactFormSet = inlineformset_factory(Agent, ContactInfo, can_delete=True)        


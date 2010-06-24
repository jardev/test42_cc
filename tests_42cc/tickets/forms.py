from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.admin import widgets
from tests_42cc.tickets.models import Agent, ContactInfo, HttpRequestLogEntry

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent        
        fields = ['first_name', 'last_name', 'biography', 'birthday']
        widgets = { 'birthday' : widgets.AdminDateWidget() }
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.reverse()
               
ContactFormSet = inlineformset_factory(Agent, ContactInfo, can_delete=True)        


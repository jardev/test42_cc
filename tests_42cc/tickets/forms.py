from django import forms
from django.forms.models import inlineformset_factory
from django.conf import settings
from tests_42cc.tickets.models import Agent, ContactInfo, HttpRequestLogEntry

class DatePickerWidget(forms.DateInput):
    class Media:
        css = { 'all': ('/static/jquery.ui.custom.css', ) }
        js = ('/static/js/jquery.ui.custom.js', )

    def __init__(self, attrs={'class' : 'datepicker'}):
        super(forms.DateInput, self).__init__(attrs=attrs)


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent        
        fields = ['first_name', 'last_name', 'biography', 'birthday']
        widgets = { 'birthday' : DatePickerWidget }
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder.reverse()
               
ContactFormSet = inlineformset_factory(Agent, ContactInfo, can_delete=True)        


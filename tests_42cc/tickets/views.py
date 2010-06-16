from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from tests_42cc.tickets.models import Agent, ContactInfo
from tests_42cc.tickets.forms import AgentForm

def index(request, template_name='tickets/index.html'):
    page_title = 'About My Self'
    agent = Agent.objects.get() 

    return render_to_response(template_name, locals(), 
        context_instance=RequestContext(request))
        
def edit(request, template_name='tickets/edit.html'):
    page_title = 'About My Self - Edit'    
    agent = Agent.objects.get()
    
    form = AgentForm(instance=agent, label_suffix=':')
    
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))

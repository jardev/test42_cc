from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from tests_42cc.tickets.models import Agent, ContactInfo
from tests_42cc.tickets.forms import AgentForm, ContactFormSet

def index(request, template_name='tickets/index.html'):
    page_title = 'About My Self'
    agent = Agent.objects.get() 

    return render_to_response(template_name, locals(), 
        context_instance=RequestContext(request))

@login_required        
def edit(request, template_name='tickets/edit.html'):
    page_title = 'About My Self - Edit'    
    agent = Agent.objects.get()
    
    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        contacts = ContactFormSet(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            if contacts.is_valid():
                contacts.save()
                return HttpResponseRedirect(urlresolvers.reverse('tickets_home'))
    else:
        form = AgentForm(instance=agent, label_suffix=':')
        form.fields.keyOrder.reverse()
        contacts = ContactFormSet(instance=agent)
    
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))

@login_required        
def do_logout(request):
    logout(request)        
    return HttpResponseRedirect(urlresolvers.reverse('tickets_home'))


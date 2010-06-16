from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import simplejson
from tests_42cc.tickets.models import Agent, ContactInfo
from tests_42cc.tickets.forms import AgentForm, ContactFormSet
from tests_42cc.tickets.forms import HttpRequestLogEntry

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
        success = False
        errors = []
        
        if form.is_valid():
            form.save()
            if contacts.is_valid():
                contacts.save()
                success = True
            else:
                errors = [(key, unicode(value[0])) for key, value in contacts.errors.items()]
        else:
            errors = [(key, unicode(value[0])) for key, value in form.errors.items()]
            
        if success and not request.is_ajax():
            return HttpResponseRedirect(urlresolvers.reverse('tickets_home'))
            
        json_result = simplejson.dumps(({ 'success' : success,
                                          'errors'  : errors }))
        print json_result                                          
        return HttpResponse(json_result, mimetype='application/javascript')
    else:
        form = AgentForm(instance=agent, label_suffix=':')
        contacts = ContactFormSet(instance=agent)
    
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))

@login_required        
def do_logout(request):
    logout(request)        
    return HttpResponseRedirect(urlresolvers.reverse('tickets_home'))
  
@login_required          
def view_http_log(request):
    


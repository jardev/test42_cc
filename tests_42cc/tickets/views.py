from django.core import urlresolvers
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import simplejson
from tests_42cc.tickets.models import Agent, ContactInfo, HttpRequestLogEntry
from tests_42cc.tickets.forms import AgentForm, ContactFormSet
import itertools

def index(request, template_name='tickets/index.html'):
    agent = get_object_or_404(Agent)

    return render_to_response(template_name,
        context_instance=RequestContext(request,
            { 'page_title' : "About My Self",
              'agent' : agent }))

@login_required        
def edit(request, template_name='tickets/edit.html'):
    agent = get_object_or_404(Agent)
    
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
        return HttpResponse(json_result, mimetype='application/javascript')
    else:
        form = AgentForm(instance=agent, label_suffix=':')
        contacts = ContactFormSet(instance=agent)
    
    return render_to_response(template_name,
        context_instance=RequestContext(request,
            { 'form' : form,
              'contacts' : contacts,
              'agent' : agent,
              'page_title' : "About My Self - Edit" }))

@login_required
def do_logout(request):
    logout(request)
    return HttpResponseRedirect(urlresolvers.reverse('tickets_home'))
  
@login_required
def view_http_log(request, template_name='tickets/view_log.html', priority=1):
    log_priority = HttpRequestLogEntry.objects.order_by('date').filter(priority=priority).all()
    log_others = HttpRequestLogEntry.objects.order_by('date').exclude(priority=priority).all()
    log = itertools.chain(log_priority, log_others)
    return render_to_response(template_name,
        context_instance=RequestContext(request,
            { 'page_title' : "Http Request Log",
              'log' : log }))
       
    


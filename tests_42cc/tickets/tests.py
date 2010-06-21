from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest, HttpResponse
from django.template import Template, Context
from tests_42cc.tickets import models
from tests_42cc import settings
from tests_42cc.tickets.templatetags.tickets_tags import build_object_link

class AgentModelTest(TestCase):
    def setUp(self):        
        self.agent = models.Agent.objects.create(
            first_name='Jarik',
            last_name='Luzin',
            biography='Biography',
            birthday = '1984-12-26')        
        self.contact1 = models.ContactInfo.objects.create(
            contact='+38 097 915 20 18',
            contact_type='phone',
            agent=self.agent,
            is_default=True)
        self.contact2 = models.ContactInfo.objects.create(
            contact='jardev@gmail.com',
            additional_info='None',
            agent=self.agent,
            is_default=True)
        self.contact3 = models.ContactInfo.objects.create(
            contact='+38 044 111 22 33',
            contact_type='phone',
            agent=self.agent,            
            is_active=False)
            
    def test_agent(self):
        self.assertEquals(unicode(self.agent), 'Jarik Luzin')
        self.assertEquals(self.agent.contactinfo_set.count(), 3)
        self.assertEquals(self.agent.first_name, 'Jarik')
        self.assertEquals(self.agent.last_name, 'Luzin')
        self.assertEquals(self.agent.biography, 'Biography')
        self.assertEquals(self.agent.birthday, '1984-12-26')
        
    def test_contact1(self):
        self.assertEquals(unicode(self.contact1), 'Phone: +38 097 915 20 18')
        self.assertEquals(self.contact1.agent.pk, self.agent.pk)
        self.assertEquals(self.contact1.contact_type, 'phone')
        self.assertEquals(self.contact1.contact, '+38 097 915 20 18')
        self.assertEquals(self.contact1.additional_info, '')
        self.assertEquals(self.contact1.is_default, True)
        self.assertEquals(self.contact1.is_active, True)
    
    def test_contact2(self):
        self.assertEquals(unicode(self.contact2), 'E-Mail: jardev@gmail.com')
        self.assertEquals(self.contact2.agent.pk, self.agent.pk)
        self.assertEquals(self.contact2.contact_type, 'email')
        self.assertEquals(self.contact2.contact, 'jardev@gmail.com')
        self.assertEquals(self.contact2.additional_info, 'None')
        self.assertEquals(self.contact2.is_default, True)
        self.assertEquals(self.contact2.is_active, True)
            
    def test_contact3(self):
        self.assertEquals(unicode(self.contact3), 'Phone: +38 044 111 22 33')
        self.assertEquals(self.contact3.agent.pk, self.agent.pk)
        self.assertEquals(self.contact3.contact_type, 'phone')
        self.assertEquals(self.contact3.contact, '+38 044 111 22 33')
        self.assertEquals(self.contact3.additional_info, '')
        self.assertEquals(self.contact3.is_default, False)
        self.assertEquals(self.contact3.is_active, False)

class IndexViewTest(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        
class MiddlewareTest(TestCase):
    def test_http_request_logger(self):
        client = Client()        
        response = client.get('/admin/')
        result = models.HttpRequestLogEntry.objects.get(url='/admin/')
        self.assertNotEquals(result, None)
        self.assertEquals(result.method, 'GET') 
        
class ContextProcessorTest(TestCase):
    def test_response(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(response.context['settings'], settings)
        
class EditFormTest(TestCase):
    def setUp(self):        
        self.client = Client()
        self.client.login(username='admin', password='admin')
        
    def test_edit_view(self):        
        response = self.client.get('/edit/')
        self.assertEqual(response.status_code, 200)
        self.failIfEqual(response.context['form'], None)
        self.failIfEqual(response.context['contacts'], None)

class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_unauthorized(self):
        response = self.client.get('/edit/')
        self.assertEqual(response.status_code, 302)
        
    def test_authorized(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/edit/')
        self.assertEqual(response.status_code, 200)

class EditObjectTagTest(TestCase):
    template_text = '{% load tickets_tags %}{% edit_object test_object %}'

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        
        self.test_object = models.Agent.objects.get()
        self.correct_url = build_object_link(self.test_object)
        self.template = Template(EditObjectTagTest.template_text)
                
    def test_generate_link(self):
        result = self.template.render(Context({ 'test_object' : self.test_object }))
        self.assertEqual(result, self.correct_url)

class ModelActionLogTest(TestCase):
    def test_create_object(self):
        count = models.ModelActionLogEntry.objects.count()        
        a = models.Agent()
        a.first_name = 'FirstName'
        a.last_name = 'LastName'
        a.biography = 'Biography'
        a.birthday = '1980-01-01'
        a.save()
        new_count = models.ModelActionLogEntry.objects.count()
        self.assertEqual(count + 1, new_count)
        
        last_log_entry = models.ModelActionLogEntry.objects.latest('when')
        self.assertNotEquals(last_log_entry, None)
        self.assertEquals(last_log_entry.model_id, unicode(a.pk))
        self.assertEquals(last_log_entry.model_class, a.__class__.__name__)
        self.assertEquals(last_log_entry.model_module, a.__class__.__module__)
        self.assertEquals(last_log_entry.action, 0)
        
    def test_edit_object(self):
        count = models.ModelActionLogEntry.objects.count()        
        a = models.Agent.objects.get()
        a.biography = ''
        a.save()
        new_count = models.ModelActionLogEntry.objects.count()
        self.assertEqual(count + 1, new_count)
        
        last_log_entry = models.ModelActionLogEntry.objects.latest('when')
        self.assertNotEquals(last_log_entry, None)
        self.assertEquals(last_log_entry.model_id, unicode(a.pk))
        self.assertEquals(last_log_entry.model_class, a.__class__.__name__)
        self.assertEquals(last_log_entry.model_module, a.__class__.__module__)
        self.assertEquals(last_log_entry.action, 1)
        
    def test_delete_object(self):
        a = models.Agent.objects.get()
        pk = a.pk
        a.delete()
        
        last_log_entry = models.ModelActionLogEntry.objects.latest('when')
        self.assertNotEquals(last_log_entry, None)
        self.assertEquals(last_log_entry.model_id, unicode(pk))
        self.assertEquals(last_log_entry.model_class, a.__class__.__name__)
        self.assertEquals(last_log_entry.model_module, a.__class__.__module__)
        self.assertEquals(last_log_entry.action, 2)
        
class HttpLogViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')
        # make 10 requests
        for i in range(10):
            self.client.get('/')
            
    def test_view_http_log(self):
        response = self.client.get('/http-log/')
        self.assertEquals(response.status_code, 200)
        for log_entry in models.HttpRequestLogEntry.objects.all()[:10]:
            self.assertContains(response, log_entry)
            
        
        
        
        
        
                      

from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest, HttpResponse
from tests_42cc.tickets import models
from tests_42cc import settings

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
        request, response = client.pre_view_get('/middleware-test-url/')
        middleware = HttpRequestLoggerMiddleware()
        middleware.process_response(request, response)
        result = HttpRequestLogEntry.objects.get(url='/middleware-test-url/')
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
        self.assertEqual(response.status_code, 300)
        self.failIfEqual(response.context['form'], None)
        self.failIfEqual(response.context['contacts'], None)


        
            
            

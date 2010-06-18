#from django.test import TestCase
#from django.test.client import Client
#from django.core.urlresolvers import reverse
#from tests_42cc.tickets import views

#class AuthTest(TestCase):
#    def setUp(self):
#        self.client = Client()
#        
#    def test_unauthorized(self):
#        response = self.client.get(reverse(views.edit))
#        self.assertEqual(response.status_code, 302)
#        
#    def test_authorized(self):
#        self.client.login(username='admin', password='admin')
#        response = self.client.get(reverse(views.edit))
#        self.assertEqual(response.status_code, 200)


from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.conf import settings

class Test_Services(TestCase):
    def set_up(self):
        client = Client()
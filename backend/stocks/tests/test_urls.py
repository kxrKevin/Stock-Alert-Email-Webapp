from django.test import SimpleTestCase
from django.urls import reverse, resolve
from stocks.views import portfolio_view, statistics_view
from stocks.services import search_stock, get_betas

class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        url = reverse('portfolio')
        print(resolve(url))
        self.assertEqual(resolve(url).func, portfolio_view)

    def test_statistics_url_is_resolved(self):
        url = reverse('statistics', kwargs={'ticker': 'AAPL'})
        print(resolve(url))
        self.assertEqual(resolve(url).func, statistics_view)
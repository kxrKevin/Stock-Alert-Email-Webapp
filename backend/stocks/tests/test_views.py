from django.test import TestCase, Client
from django.urls import reverse, resolve
from stocks.views import portfolio_view, statistics_view
from stocks.models import TrackedStock
from unittest.mock import patch


class Test_Portfolio_View(TestCase):

    def setUp(self):
        self.client = Client()

    def test_portfolio_get(self):
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stocks/portfolio.html")

    def test_add_stock(self):
        response = self.client.post(reverse("portfolio"), {
            "add_stock": True,
            "ticker": "AAPL",
            "company_name": "Apple Inc",
            "current_price": "150",
            "upper_limit": "200",
            "lower_limit": "100",
            "alertstatus": "on"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("portfolio"))

        self.assertTrue(TrackedStock.objects.filter(ticker="AAPL").exists())

    def test_delete_stock(self):

        stock = TrackedStock.objects.create(
            ticker="AAPL",
            company_name="Apple",
            upperLimit=200,
            lowerLimit=100,
            alertEnabled=True
        )

        response = self.client.post(reverse("portfolio"), {
            "delete": True,
            "stock_id": stock.id
        })

        self.assertRedirects(response, reverse("portfolio"))

        self.assertFalse(TrackedStock.objects.filter(id=stock.id).exists())

    def test_statistics_redirect(self):
        stock = TrackedStock.objects.create(
            ticker="AAPL",
            company_name="Apple",
            upperLimit=200,
            lowerLimit=100,
            alertEnabled=True
        )

        response = self.client.post(reverse("portfolio"), {
            "statistics": True,
            "stock_id": stock.id
        })

        self.assertRedirects(response, reverse("statistics", args=["AAPL"]))
        self.assertEqual(self.client.session["ticker"], "AAPL")

    def test_reset_alerts(self):
        stock = TrackedStock.objects.create(
            ticker="AAPL",
            upperLimit=200,
            lowerLimit=100,
            upperAlertTriggered=True,
            lowerAlertTriggered=True
        )

        response = self.client.post(reverse("portfolio"), {
            "reset_alerts": True
        })

        stock.refresh_from_db()
        self.assertFalse(stock.upperAlertTriggered)
        self.assertFalse(stock.lowerAlertTriggered)



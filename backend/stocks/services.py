import alpaca_trade_api as tradeapi
from django.conf import settings
from django.utils import timezone
from .models import TrackedStock

def search_stock(ticker):
    try:
        api = tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL
        )
        asset = api.get_asset(ticker)
        latest_trade = api.get_latest_trade(ticker)
        return{
            'ticker': asset.symbol,
            'company_name': asset.name,
            'current_price': latest_trade.price,
        }
        print(ticker + "found")

    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None
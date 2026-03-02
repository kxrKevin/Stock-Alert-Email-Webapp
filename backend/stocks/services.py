import alpaca_trade_api as tradeapi
from django.conf import settings
from django.utils import timezone
import yfinance as yf
import pandas as pd

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
    
def get_betas(ticker1, ticker2):
    
    data = yf.download(ticker1, period="3mo")[['Close']]
    spy = yf.download(ticker2, period="3mo")[['Close']]

    data = data.rename(columns={'Close': 'stock_close'})
    spy = spy.rename(columns={'Close': 'spy_close'})

    merged = pd.merge(data, spy, left_index=True, right_index=True)

    merged['stock_ret'] = merged['stock_close'].pct_change()
    merged['spy_ret'] = merged['spy_close'].pct_change()

    covariance = merged[['stock_ret', 'spy_ret']].cov().iloc[0,1]
    variance = merged['spy_ret'].var()

    beta = covariance / variance

    print(data)
    print(spy)
    print(merged)
    return beta


def get_volatility(ticker):

    data = yf.download(ticker, period="3mo")[['Close']]
    data['Returns'] = data['Close'].pct_change() * 100

    print(data)

    volatility = data['Returns'].std()

    return f"{volatility:.4f}"


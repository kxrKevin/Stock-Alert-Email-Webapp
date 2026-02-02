from django.db import models
from django.conf import settings
from django.utils import timezone
import alpaca_trade_api as tradeapi

# Create your models here.
class TrackedStock(models.Model):
    
    ticker = models.CharField(max_length=4)
    company_name = models.CharField(max_length=200)

    # Alert Logic
    upperLimit = models.DecimalField(max_digits = 10, decimal_places=2)
    lowerLimit = models.DecimalField(max_digits = 10, decimal_places=2)
    alertEnabled = models.BooleanField(default = False)

    upperAlertTriggered = models.BooleanField(default = False)
    lowerAlertTriggered = models.BooleanField(default = False)

    marketClosed = models.BooleanField(default = False)
    latestPrice = models.DecimalField(max_digits = 10, decimal_places=2, default=0.00)

    last_alert_type = models.CharField(max_length=20, null=True, blank=True)  

    alertTriggerTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ticker} - {self.company_name}"

    def _get_alpaca_api(self):
        return tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL
        )
    
    def get_current_price(self):
        # fetch live price from Alpaca API
        try:
            api = self._get_alpaca_api()
            # get latest trade for this ticker
            latest_trade = api.get_latest_trade(self.ticker)
            return float(latest_trade.price)

        except Exception as e:
            print(f"Error fetching price for {self.ticker}: {e}")
            return None

    # returns boolean value for if the price has hit a upper or lower threshold
    def check_alert(self, current_price):
        
        # ensure alert is enabled before proceeding to other logic
        if self.alertEnabled == False:
            return False
        else:
            print(self.company_name)
            print(current_price)
            print("Upper limit: " + str(self.upperLimit))
            print("Upper Alert Triggered: " + str(self.upperAlertTriggered))

        if current_price is None:
            return False
        
        if (self.upperLimit and not self.upperAlertTriggered and (current_price >= self.upperLimit)):
            self.upperAlertTriggered = True
            self.last_alert_type = 'upper'
            self.alertTriggerTime = timezone.now()
            self.save()
            print(self.company_name)
            print("UPPER THRESHOLD REACHED")
            return {
                'type': 'upper',
                'price': current_price,
                'threshold':self.upperLimit
            }   
        
        if (self.lowerLimit and not self.lowerAlertTriggered and (current_price <= self.lowerLimit)):
            self.lowerAlertTriggered = True
            self.last_alert_type = 'bottom'
            self.alertTriggerTime = timezone.now()
            self.save()
            print(self.company_name)
            print("LOWER THRESHOLD REACHED")
            return {
                'type': 'lower',
                'price': current_price,
                'threshold':self.lowerLimit
            }

        return None

    

    

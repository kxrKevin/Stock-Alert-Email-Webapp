from django.shortcuts import render, get_object_or_404, redirect
from .models import TrackedStock
from .services import search_stock

from django.core.mail import send_mail
from django.conf import settings

def portfolio_view(request):
    stockList = TrackedStock.objects.all()
    # Portfolio Logic
    stock_data = []
    search_results = None
    
    # Search Results
    if request.method == 'POST':
        # Handle search
        if 'search' in request.POST:
            ticker = request.POST.get('ticker')
            search_results = search_stock(ticker)
        
        elif 'add_stock' in request.POST:
            ticker = request.POST.get('ticker')
            companyName = request.POST.get('company_name')
            currentPrice = request.POST.get('current_price')
            uLimit = request.POST.get('upper_limit')
            lLimit = request.POST.get('lower_limit')

            alerton = False
            alert_status = request.POST.get('alertstatus')

            if alert_status == "on":
                alerton = True

            TrackedStock.objects.create(
                ticker = ticker,
                company_name = companyName,
                upperLimit = uLimit,
                lowerLimit = lLimit,
                alertEnabled = alerton
            )
        elif 'delete' in request.POST:
            stock_id = request.POST.get('stock_id')
            stocks = get_object_or_404(TrackedStock, id=stock_id)
            stocks.delete()
            return redirect('portfolio')

        elif 'reset_alerts' in request.POST:
            for rstock in stockList:
                rstock.upperAlertTriggered = False
                rstock.lowerAlertTriggered = False

    for stock in stockList:
        current_price = stock.get_current_price()
        stock_data.append({
            'stock': stock,
            'ticker': stock.ticker,
            'company_name': stock.company_name,
            'current_price': stock.get_current_price(),
            'upperLimit': stock.upperLimit,
            'lowerLimit': stock.lowerLimit,
            'alertEnabled': stock.alertEnabled
        })

        send_alert_email = stock.check_alert(current_price)
        
        if send_alert_email:
            if send_alert_email['type'] == 'upper':
                send_mail(
                    f"STOCK ALERT: {stock.company_name} has reached over the threshold of {stock.upperLimit}",
                    f"{stock.company_name} Current Price: {current_price}",
                    settings.EMAIL_HOST_USER,
                    [settings.TARGET_EMAIL],
                    fail_silently=False,
                )
                print("SENT UPPER NOTIFICATION EMAIL")
            else:
                send_mail(
                    f"STOCK ALERT: {stock.company_name} has reached below the threshold of {stock.lowerLimit}",
                    f"{stock.company_name} Current Price: {current_price}",
                    settings.EMAIL_HOST_USER,
                    [settings.TARGET_EMAIL], 
                    fail_silently=False,
                )              
                print("SENT LOWER NOTIFICATION EMAIL") 
            

    return render(request, 'stocks/portfolio.html', {
        'stock_data':stock_data,
        'search_results': search_results
    })




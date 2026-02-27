cd C:\COMPSCI\Python\StockAlert\backend

# Start server in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python manage.py runserver"

# Wait a few seconds for server to start
Start-Sleep -Seconds 3

# Open browser
Start-Process "http://127.0.0.1:8000/portfolio/"
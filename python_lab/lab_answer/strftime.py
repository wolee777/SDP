import time

while True:
    year = time.strftime('%Y-%m-%d %a') # year-month-day weekday
    hour = time.strftime('%H:%M:%S %p') # hour:minute:second AM/PM
    print (year,' ',hour)  
    time.sleep(1)


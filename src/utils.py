from datetime import date

def today_yyyymmdd():
    today = date.today().strftime("%Y%m%d")
    return today

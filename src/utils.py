from datetime import date

def today_yyyymmdd():
    today = date.today().strftime("%Y%m%d")
    return today

if __name__ == "__main__":
    print(today_yyyymmdd())

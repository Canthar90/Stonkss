import requests
import datetime
import smtplib
STOCK = "TSLA"
COMPANY_NAME = "Tesla"

my_email = "example@example.com"
password = "Password"

alpha_vantage_api = "G4IISRL91LB7ZAN0"
alpha_vintage_link = "https://www.alphavantage.co/query"
prices_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": alpha_vantage_api
}

news_api = "27c48cf5efca40e3b5eac466ff620361"
news_parameters = {
    "apiKey": news_api,
    "q": COMPANY_NAME,
}

def closing_days_status():
    prices_r = requests.get(alpha_vintage_link, params=prices_parameters)
    prices_r.raise_for_status()
    prices_data = prices_r.json()
    prices_by_day = prices_data["Time Series (Daily)"]
    key_days = []
    for key in prices_by_day:
        key_days.append(key)
    first_day = float(prices_by_day[key_days[0]]["4. close"])
    second_day = float(prices_by_day[key_days[1]]["4. close"])
    value = (first_day / second_day)*100 - 100
    # print(value)
    if value >= 5:
        # print(f"wzrost o {round(value)}%")
        return True, value
    elif value <= -5:
        # print(f"spadek o {round(value)}%")
        return False, value


def get_data(value, state):
    news_data = requests.get("https://newsapi.org/v2/top-headlines", params=news_parameters)
    news_data.raise_for_status()
    newses = news_data.json()
    news_source = (newses["articles"][0]["source"]["id"])
    news_description = (newses["articles"][0]["description"])
    news_link = (newses["articles"][0]["url"])
    news_title = (newses["articles"][0]["title"])
    send_message(source=news_source, title=news_title, description=news_description, link=news_link, value=value, state=state)


def send_message(source, title, description, link, value, state):
    with smtplib.SMTP("smtp.example.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="example@example.com",
                            msg=f"Subject:Tesla stonks\n\nTesla inc notet {round(value)}% {state}.\n"
                                f"Newest related news are from: {source}\n"
                                f"{title}\n{description}\nYou can find orginal article here{link}")
    pass


date = datetime.datetime.now()
date_key = date.date()
# print(date_key)





# newsapi = NewsApiClient(api_key=news_api)
one_for_day = True
if date.weekday() < 5 and date.hour == 7 and one_for_day:
    one_for_day = False
    try:
        rise_or_fall, value = closing_days_status()
        if rise_or_fall:
            state = "rise"
            get_data(value=value, state=state)
        elif not rise_or_fall:
            state = "drop"
            get_data(value=value, state=state)
    except ValueError:
        pass
elif not one_for_day and date.hour == 8:
    one_for_day = True







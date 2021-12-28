"""
Stock Price of Bitcoin (Yesterday Closing - Previous Closing = Direction)
Relevant News!
Mail/SMS
"""

import requests
import os
import smtplib
from datetime import datetime

STOCK = "BTC"
CURRENCY = "USD"

STOCK_OPTION = "TIME_SERIES_DAILY"
CRYPTO_OPTION = "DIGITAL_CURRENCY_DAILY"

year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")
day = datetime.now().strftime("%d")
yesterday_date = int(day) - 1
day_before_date = int(day) - 2

# Mail parameters
my_email = os.environ.get("MY_EMAIL")
my_password = os.environ.get("MY_PASSWORD")

# Stock API
stock_url = 'https://www.alphavantage.co/query'
stock_api_key = os.environ.get("ALPHA_API_KEY")

# News API
news_url = 'https://newsapi.org/v2/everything'
news_api_key = os.environ.get("NEWS_API_KEY")

# Creating a list of dictionaries to hold 3 news.
news_list = []
news_dict = {}

# Stock Query
stock_parameters = {
    "function": CRYPTO_OPTION,
    "symbol": STOCK,
    "market": CURRENCY,
    "apikey": stock_api_key,
}

# News Query
news_parameters = {
    "apiKey": news_api_key,
    "q": STOCK,
    "pageSize": 3,
    "language": "en",

}

# GET Request
response = requests.get(stock_url, params=stock_parameters)
response.raise_for_status()
currency_data = response.json()

# Day Formatting to get yesterday and day before
yesterday_string = f"{year}-{month}-{yesterday_date}"
day_before_string = f"{year}-{month}-{day_before_date}"

# Getting close price of yesterday and day before
yesterday = currency_data["Time Series (Digital Currency Daily)"][yesterday_string]["4b. close (USD)"]
day_before = currency_data["Time Series (Digital Currency Daily)"][day_before_string]["4b. close (USD)"]
# Change types to calculate alteration
yesterday = float(yesterday)
day_before = float(day_before)


def calculate_percent(yesterday_closing, day_before_closing):
    """Calculating alteration in BTCUSD."""
    percentage = (yesterday_closing - day_before_closing) / day_before_closing
    return percentage


def get_news():
    """Request for news."""
    response_news = requests.get(news_url, params=news_parameters)
    response_news.raise_for_status()
    news_data = response_news.json()
    for i in range(3):
        news_dict["title"] = news_data["articles"][i]["title"]
        news_dict["description"] = news_data["articles"][i]["description"]
        news_dict["link"] = news_data["articles"][i]["url"]
        news_list.append(news_dict)


get_news()
# Calculate the change in price
percent = calculate_percent(yesterday, day_before)
if percent > 0:
    stock_string = f"BTC {percent:.4f}%"
else:
    stock_string = f"BTC {percent:.4f}%"

# Create the message
message = f"{stock_string}\n" \
          f"Headline: {news_list[0]['title']}\n" \
          f"Description: {news_list[0]['description']}\n" \
          f"Link: {news_list[0]['link']}"

# Send message via e-mail
with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="tahatsahin@gmail.com",
        msg=f"{message} "
    )

import requests
import datetime
import smtplib


STOCK = "STOCK TICKER"
COMPANY_NAME = "COMPANY NAME"
news_api_key = "NEWS API KEY"
stock_api_key = "STOCK API KEY"


def send_email():
    my_email = "YOUR EMAIL"
    password = "YOUR PASSWORD"

    # using gmail settings
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject: {STOCK} {up_down}{formatted_pct_diff}%\n\n{formatted_articles[0]}\n{formatted_articles[1]}\n"
                f" {formatted_articles[2]} "
        )

# alphavantage api call
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "full",
    "apikey": stock_api_key,
}
stock = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
stock.raise_for_status()
stock_data = stock.json()["Time Series (Daily)"]

# create list from stock data dictionary
stock_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
previous_day_closing_price = float(stock_list[1]["4. close"])

# calculate difference and pct
difference = yesterday_closing_price - previous_day_closing_price
pct_diff = (abs(difference) / yesterday_closing_price) * 100
formatted_pct_diff = "{:.2f}".format(pct_diff)
up_down = None
if difference > 0:
    up_down = "+"
else:
    up_down = "-"

# if greater than 5 pct difference, email top stories
if pct_diff > 0.05:
    # news api call
    news_parameters = {
        "qinTitle": COMPANY_NAME,
        "apiKey": news_api_key,
    }
    news = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
    news.raise_for_status()
    articles = news.json()["articles"]
    top_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}. \nLink:{article['url']}\n\n"
                          for article in top_articles]
    send_email()

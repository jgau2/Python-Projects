import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
owm_api_key = "YOUR OPEN WEATHER MAP API KEY"
twilio_account_sid = "YOUR TWILLO SID"
twilio_auth_token = "YOUR TWILLO TOKEN"

parameters = {
    "lat": YOUR LATTITUDE,
    "lon": YOUR LONGITUDE,
    "exclude": ["current","minutely","daily"],
    "appid": owm_api_key,
}

response = requests.get(OWM_endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()

will_rain = False

weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    weather_id = hour_data["weather"][0]["id"]
    if int(weather_id) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(twilio_account_sid, twilio_auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain",
        from_='TWILLO PHONE NUMBER',
        to='YOUR PHONE NUMBER'
    )
    print(message.status)




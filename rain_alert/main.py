import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "301fbc444e749149afae371d964536e3"
account_sid = "ACe0858bb2623caca9d795d5f70cf7aa9e"
auth_token = "c78424d7e5f29a620025d73459cafc69"

parameters = {
    "lat": 81.3603155,
    "lon": 28.5154053,
    "exclude": ["current","minutely","daily"],
    "appid": api_key,
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

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain",
        from_='+17652953679',
        to='+17722013969'
    )
    print(message.status)




import requests
import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

weather_endpoint= "https://api.openweathermap.org/data/2.5/forecast"
geocoding_endpoint= "http://api.openweathermap.org/geo/1.0/direct"
api_key = os.environ.get("OWM_API_KEY")

geocoding_params= {
    "appid": api_key,
    "q": os.environ.get("MY_CITY"),
}

geocoding_data = requests.get(geocoding_endpoint,
                              params= geocoding_params)
geocoding_data.raise_for_status()
geocoding_data = geocoding_data.json()


weather_params = {
    "lat": geocoding_data[0]["lat"],
    "lon": geocoding_data[0]["lon"],
    "cnt": 4,
    "appid": api_key
}

weather_data = requests.get(weather_endpoint, params= weather_params)
weather_data.raise_for_status()
weather_data = weather_data.json()

print(f"http code: {weather_data['cod']}")
will_rain = False
summary_str = ''
for forecast in weather_data['list']:
    date_time = forecast['dt_txt'].split('-')
    if '00:00:00' in date_time[2]:
        print('')
    date_time = date_time[1] + '-' + date_time[2]
    date_time = date_time.split(':')
    date_time = date_time[0]

    weather_id = forecast['weather'][0]['id']

    if weather_id < 700:
        will_rain = True

    summary_str += f"{date_time}: {forecast['weather'][0]['description']}\n"

if will_rain:
    print("umbrella")
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            content_sid=os.environ.get("CONTENT_SID"),
            body='It is going to rain!\n\n'
                 f'{summary_str}\n'
                 'Bring your umbrella.☔',
            from_=os.environ.get("FROM"),
            to=os.environ.get("TO")
        )
        print(message.sid)
    except Exception as e:
        print(e)

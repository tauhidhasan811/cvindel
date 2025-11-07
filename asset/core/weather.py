import json
import urllib.request

def get_temp (lat, lon):
    baseurl = 'https://api.openweathermap.org/data/2.5/weather?'
    apikey = '2770c4578d6db354b592f37b02bb02e8'
    url = f"{baseurl}lat={lat}&lon={lon}&appid={apikey}&units=metric"

    with urllib.request.urlopen(url) as response:
        data = response.read()  
        weather = json.loads(data)  

    temp = weather['main']['temp']
    country = weather['sys']['country']
    all_data = {
        'temperacture': f'{temp} cel',
        'country' : country,
        'city_cor' : f'[{lat}, {lon}]'
    }
    return all_data
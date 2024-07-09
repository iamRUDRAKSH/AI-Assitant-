import requests
import json
from main import talk

if __name__ == "__main__":

    city = "pune"
    url = f"https://api.weatherapi.com/v1/current.json?key=fc481608852a4675b6865641242206&q={city}"

    r = requests.get(url)
    info = json.loads(r.text)
    k = list(info.keys())   
    if k[0] == "error":
        print(info["error"]["message"])
        exit(1)    
    district = info["location"]["name"]
    state = info["location"]["region"]
    country = info["location"]["country"]
    today = info["location"]["localtime"]
    temp = info["current"]["temp_c"]
    rain = info["current"]["condition"]["text"]
    humidity = info["current"]["humidity"]

    talk(f"Location : {district}, {state}, {country}")
    talk(f"Date and Time : {today}")
    talk(f"Temperature : {temp}°C")
    talk(f"Weather : {rain}")
    talk(f"Humidity : {humidity}")
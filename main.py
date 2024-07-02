from fastapi import FastAPI, Request
import requests
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

WEATHER_API_KEY = "5ff9dc0511e3457280c71936240107"


def get_location_by_ip():
    url = f"http://api.weatherapi.com/v1/ip.json?key={WEATHER_API_KEY}&q=auto:ip"
    response = requests.get(url)
    data = response.json()
    ip = data["ip"]
    city = data["city"]
    return ip, city

def get_weather(location: str):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
    response = requests.get(url)
    data = response.json()
    temperature = data["current"]["temp_c"]
    return temperature

@app.get("/api/hello")
async def visitor_info(request: Request, visitor_name: str):
    visitor_name = visitor_name.strip('"')
    client_ip, location = get_location_by_ip()
    temperature = get_weather(location)
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    
    return {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }

import os
import asyncio

from sanic import Blueprint, response
from sanic.response import text, HTTPResponse, json
from sanic.request import Request
from sanic.exceptions import SanicException

from geopy.geocoders import Nominatim

import httpx
from dotenv import load_dotenv

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


load_dotenv()

geolocator = Nominatim(user_agent="weather_app")

bp = Blueprint("weather", url_prefix="/weather")


async def get_async(url: str):
    async with httpx.AsyncClient() as client:
        return await client.get(url)


async def get_city(city: str):
    location = geolocator.geocode(city)
    return location


@bp.get("/")
async def test_handler(request):
    return json({"app": "weather"})


@bp.get("/current/<city:str>")
async def get_current(request, city: str, units: str = "metric"):
    """
    Get table with current weather for the city
    """
    location = await get_city(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&units={units}&appid={os.getenv('OPEN_WEATHER_KEY')}"
    raw_data = await get_async(url)
    json_data = raw_data.json()
    temp_data = [
        {
            "city": json_data["name"],
            "temp": json_data["main"]["temp"],
            "feels_like": json_data["main"]["feels_like"],
            "min_temp": json_data["main"]["temp_min"],
            "max_temp": json_data["main"]["temp_max"],
            "humidity": json_data["main"]["humidity"],
            "pressure": json_data["main"]["pressure"],
        }
    ]
    df = pd.DataFrame.from_dict(temp_data)
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color="paleturquoise",
                    align="center",
                ),
                cells=dict(
                    values=[
                        df.city,
                        df.temp,
                        df.feels_like,
                        df.min_temp,
                        df.max_temp,
                        df.humidity,
                        df.pressure,
                    ],
                    fill_color="lavender",
                    align="center",
                ),
            )
        ]
    )
    # fig.write_image(f"stats/current_{city}.png")
    fig.write_image(f"stats/current_{city}.jpeg", width=800, height=350, scale=2)
    return await response.file(f"stats/current_{city}.jpeg", 200)


# @bp.get("/users")
# async def list_all(request):
#     users = await Tags.all()
#     # return json({"list": len(users)})
#     return response.json({"users": [str(user) for user in users]})


# @bp.get("/user/<pk:int>")
# async def get_user(request, pk):
#     user = await Tags.query(pk=pk)
#     return response.json({"user": str(user)})

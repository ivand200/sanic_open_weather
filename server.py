import os

from sanic import Sanic, response 

from routers.weather import bp as weather_app

from tortoise.contrib.sanic import register_tortoise
from dotenv import load_dotenv

load_dotenv()

app = Sanic(__name__)
app.blueprint(weather_app)

register_tortoise(
    app, db_url=os.getenv("DATABASE"), modules={"models": ["models.test"]},
)
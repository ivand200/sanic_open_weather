from sanic import Sanic, response 

from routers.weather import bp as weather_app

app = Sanic(__name__)
app.blueprint(weather_app)
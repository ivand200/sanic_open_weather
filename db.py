import os
from sys import get_coroutine_origin_tracking_depth

# from tortoise.contrib.sanic import register_tortoise
# from server import app 
from dotenv import load_dotenv

load_dotenv()


TORTOISE_ORM = {
    "connections": {
         "default": os.getenv("DATABASE")
    },
    "apps": {
        "weather": {
            "models": [
                 "models.test", "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}
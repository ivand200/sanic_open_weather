import asyncio

from sanic import Blueprint
from sanic.response import text, HTTPResponse, json
from sanic.request import Request
from sanic.exceptions import SanicException

bp = Blueprint("weather", url_prefix="/weather")

@bp.get("/")
async def test_handler(request):
    return json({"app": "weather"})
import pytest
from server import app


test_data_cities = [
    ("london"),
    ("beijing"),
    ("tokyo"),
    ("Moscow"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("city", test_data_cities)
async def test_get_current_weather(city):
    """
    WHEN the "/weather/currennt/<city:str>" page is requested (GET)
    THRN check that the response is valid
    """
    request, response = await app.asgi_client.get(f"/weather/current/{city}")
    assert request.method.lower() == "get"
    assert response.status == 200

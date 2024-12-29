import time
from data_providers.base_provider import DataProvider
import requests


class WeatherProvider(DataProvider):
    def __init__(self, api_key: str, locality_id: int, update_interval: float = 120):
        """
        Initializes the weather provider. Uses zomato's weather union API.

        :param update_interval: the interval at which to fetch data in seconds
        :param api_key: the API
        :locality_id: the locality id of the city
        """
        super().__init__(update_interval)
        self.api_key = api_key
        self.locality_id = locality_id
        self.url = "https://www.weatherunion.com/gw/weather/external/v0/get_locality_weather_data"

    def fetch_data(self):

        querystring = {"locality_id": self.locality_id}
        headers = {"X-Zomato-Api-Key": self.api_key}
        print("Fetching weather data")
        response = requests.get(self.url, headers=headers, params=querystring)
        res = response.json()
        last_updated = {"last_updated": time.time()}
        if response.status_code == 200:
            res.update(last_updated)
            self.set_data(res)
        else:
            print(f"Failed to fetch weather data: {response.status_code}")

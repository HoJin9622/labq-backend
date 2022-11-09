import requests
from django.conf import settings


class RainfallController:
    ROOT_URL = "http://openapi.seoul.go.kr:8088/"
    SERVICE_RAINFALL = "ListRainfallService"

    def call(self, location):
        response = requests.get(
            f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_RAINFALL}/1/1000/{location}"
        )
        data = response.json().get("ListRainfallService")
        return data.get("row")

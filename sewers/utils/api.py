import requests
from django.conf import settings


class SewerController:
    ROOT_URL = "http://openapi.seoul.go.kr:8088/"
    SERVICE_SEWER = "DrainpipeMonitoringInfo"

    def call(self, location, start_date, end_date):
        START_PAGE = 1
        END_PAGE = 20
        response = requests.get(
            f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_SEWER}/{START_PAGE}/{END_PAGE}/{location}/{start_date}/{end_date}"
        )
        data = response.json().get("DrainpipeMonitoringInfo")
        sewers = data.get("row")
        return sewers

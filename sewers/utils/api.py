import requests
from django.conf import settings


class SewerController:
    ROOT_URL = "http://openapi.seoul.go.kr:8088/"
    SERVICE_SEWER = "DrainpipeMonitoringInfo"
    START_PAGE = 1
    END_PAGE = 1000

    def __init__(self, location_code, start_date, end_date):
        self.location_code = location_code
        self.start_date = start_date
        self.end_date = end_date

    def call(self):
        """
        하수관 수위 정보를 반환합니다.
        """
        response = requests.get(
            f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_SEWER}/{self.START_PAGE}/{self.END_PAGE}/{self.location_code}/{self.start_date}/{self.end_date}"
        )
        data = response.json().get("DrainpipeMonitoringInfo")
        sewers = data.get("row")
        return sewers

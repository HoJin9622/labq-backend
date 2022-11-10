import requests
from django.conf import settings


class SewerController:
    ROOT_URL = "http://openapi.seoul.go.kr:8088/"
    SERVICE_SEWER = "DrainpipeMonitoringInfo"
    START_PAGE = 1
    END_PAGE = 1000

    def call(self, location, start_date, end_date):
        """
        하수관 수위 정보를 반환합니다.
        """
        response = requests.get(
            f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_SEWER}/{self.START_PAGE}/{self.END_PAGE}/{location}/{start_date}/{end_date}"
        )
        data = response.json().get("DrainpipeMonitoringInfo")
        sewers = data.get("row")
        return sewers

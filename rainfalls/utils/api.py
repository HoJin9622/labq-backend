import math
import requests
from datetime import datetime
from django.conf import settings


class RainfallController:
    ROOT_URL = "http://openapi.seoul.go.kr:8088/"
    SERVICE_RAINFALL = "ListRainfallService"
    START_PAGE = 1
    END_PAGE = 1000

    def filter_date(self, rainfall, start_date, end_date):
        receive_time = datetime.strptime(rainfall["RECEIVE_TIME"], "%Y-%m-%d %H:%M")

        return receive_time > start_date and receive_time < end_date

    def call(self, location, start_datetime, end_datetime):
        response = requests.get(
            f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_RAINFALL}/{self.START_PAGE}/{self.END_PAGE}/{location}"
        )
        data = response.json().get("ListRainfallService")
        rainfalls = data.get("row")
        filtered_rainfalls = [
            rainfall
            for rainfall in rainfalls
            if self.filter_date(rainfall, start_datetime, end_datetime)
        ]
        total_count = data["list_total_count"]
        total_page = math.ceil(total_count / self.END_PAGE)
        if len(filtered_rainfalls) == 0:
            for i in range(1, total_page):
                print("start", self.START_PAGE + i * self.END_PAGE)
                print("end", self.END_PAGE + i * self.END_PAGE)
                response = requests.get(
                    f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_RAINFALL}/{self.START_PAGE + i * self.END_PAGE}/{self.END_PAGE + i * self.END_PAGE}/{location}"
                )
                data = response.json().get("ListRainfallService")
                rainfalls = data.get("row")
                list = [
                    rainfall
                    for rainfall in rainfalls
                    if self.filter_date(rainfall, start_datetime, end_datetime)
                ]
                filtered_rainfalls = filtered_rainfalls + list
        return filtered_rainfalls

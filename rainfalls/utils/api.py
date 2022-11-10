import math
import requests
from datetime import datetime
from django.conf import settings

LOCATION = {
    "01": "종로구",
    "02": "중구",
    "03": "용산구",
    "04": "성동구",
    "05": "광진구",
    "06": "동대문구",
    "07": "중랑구",
    "08": "성북구",
    "09": "강북구",
    "10": "도봉구",
    "11": "노원구",
    "12": "은평구",
    "13": "서대문구",
    "14": "마포구",
    "15": "양천구",
    "16": "강서구",
    "17": "구로구",
    "18": "금천구",
    "19": "영등포구",
}


class RainfallController:
    ROOT_URL = "http://openapi.seoul.go.kr:8088/"
    SERVICE_RAINFALL = "ListRainfallService"
    START_PAGE = 1
    PAGE_COUNT = 1000

    def __init__(self, location_code, start_date, end_date):
        self.location = LOCATION[location_code]
        self.start_date = start_date
        self.end_date = end_date

    def filter_date(self, rainfall):
        """
        강우량 정보에 start_date와 end_date 사이에 해당되는 정보를 제거 후 반환합니다.
        """
        receive_time = datetime.strptime(rainfall["RECEIVE_TIME"], "%Y-%m-%d %H:%M")

        return receive_time > self.start_date and receive_time < self.end_date

    def filter_rainfalls(self, rainfalls):
        return [rainfall for rainfall in rainfalls if self.filter_date(rainfall)]

    def get_rainfalls(self, start_page, end_page):
        """
        강우량 정보 API를 호출합니다.
        """
        response = requests.get(
            f"{self.ROOT_URL}{settings.API_KEY}/json/{self.SERVICE_RAINFALL}/{start_page}/{end_page}/{self.location}"
        )
        data = response.json().get("ListRainfallService")
        rainfalls = data.get("row")
        return rainfalls, data["list_total_count"]

    def call(self):
        """
        start_datetime과 end_datetime 사이의 강우량 정보를 불러옵니다.
        존재하지 않는다면 빈 배열을 반환합니다.
        """
        rainfalls, list_total_count = self.get_rainfalls(
            self.START_PAGE, self.PAGE_COUNT
        )
        filtered_rainfalls = self.filter_rainfalls(rainfalls)
        total_page = math.ceil(list_total_count / self.PAGE_COUNT)
        if len(filtered_rainfalls) == 0:
            for page in range(1, total_page):
                rainfalls, list_total_count = self.get_rainfalls(
                    self.START_PAGE + page * self.PAGE_COUNT,
                    self.PAGE_COUNT + page * self.PAGE_COUNT,
                )
                list = self.filter_rainfalls(rainfalls)
                filtered_rainfalls = filtered_rainfalls + list
        return filtered_rainfalls

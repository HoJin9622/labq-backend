import requests
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError


ROOT_URL = "http://openapi.seoul.go.kr:8088/"
API_KEY = settings.API_KEY
SERVICE_SEWER = "DrainpipeMonitoringInfo"
SERVICE_RAINFALL = "ListRainfallService"

LOCATION_CODE = {
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


def get_sewers(location, start_date, end_date):
    START_PAGE = 1
    END_PAGE = 20
    response = requests.get(
        f"{ROOT_URL}{API_KEY}/json/{SERVICE_SEWER}/{START_PAGE}/{END_PAGE}/{location}/{start_date}/{end_date}"
    )
    data = response.json().get("DrainpipeMonitoringInfo")
    sewers = data.get("row")
    return sewers


def get_rainfalls(location):
    response = requests.get(
        f"{ROOT_URL}{API_KEY}/json/{SERVICE_RAINFALL}/1/1000/{location}"
    )
    data = response.json().get("ListRainfallService")
    return data.get("row")


def filter_date(rainfall, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y%m%d%H")
    end_date = datetime.strptime(end_date, "%Y%m%d%H")
    receive_time = datetime.strptime(rainfall["RECEIVE_TIME"], "%Y-%m-%d %H:%M")

    return receive_time > start_date and receive_time < end_date


class Rainfalls(APIView):
    def get(self, request):
        """
        강우량 및 하수관 수위 정보 API
        GET api/v1/rainfalls/?location_code=01&start_date=2022100614&end_date=2022100615
        RESPONSE {
            location: "종로구",
            receive_time: "2022-11-04 03:29",
            rainfall10: "0",
            sewers: [
                {
                    "remark": "종로구 세종대로178 뒤 맨홀(KT광화문사옥뒤 자전거보관소앞 종로1길, 미대사관~종로소방서 남측, 중학천 하스박스)",
                    "mea_wal": 0.14
                },
                {
                    "remark": "종로구 세종대로178 뒤 맨홀(KT광화문사옥뒤 자전거보관소앞 종로1길, 미대사관~종로소방서 남측, 중학천 하스박스)",
                    "mea_wal": 0.14
                }
            ]
        }
        """
        location = request.query_params.get("location_code")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if location not in LOCATION_CODE:
            raise ParseError("location_code는 01~19 사이의 숫자를 입력해주세요.")

        sewers = get_sewers(location, start_date, end_date)
        rainfalls = get_rainfalls(LOCATION_CODE[location])

        filtered_rainfalls = [
            rainfall
            for rainfall in rainfalls
            if filter_date(rainfall, start_date, end_date)
        ]

        result = {}
        result["sewers"] = sewers
        result["rainfalls"] = filtered_rainfalls
        return Response(result)

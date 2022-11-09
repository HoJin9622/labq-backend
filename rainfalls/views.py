from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .utils.api import RainfallController
from sewers.utils.api import SewerController


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


class Rainfalls(APIView):
    def get(self, request):
        """
        강우량 및 하수관 수위 정보 API
        GET api/v1/rainfalls/?location_code=01&start_date=2022100614&end_date=2022100615
        RESPONSE {
            sewers: [
                {
                    "IDN": "19-0012",
                    "GUBN": "19",
                    "GUBN_NAM": "영등포",
                    "MEA_YMD": "2022-11-06 14:00:00.0",
                    "MEA_WAL": 0.16,
                    "SIG_STA": "통신양호",
                    "REMARK": "서울특별시 영등포구 여의대방로 145"
                }
            ],
            rainfalls: [
                {
                    "RAINGAUGE_CODE": 1901.0,
                    "RAINGAUGE_NAME": "영등포구청",
                    "GU_CODE": 119.0,
                    "GU_NAME": "영등포구",
                    "RAINFALL10": "0",
                    "RECEIVE_TIME": "2022-11-06 14:09"
                },
            ]
        }
        """
        location_code = request.query_params.get("location_code")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        try:
            start_datetime = datetime.strptime(start_date, "%Y%m%d%H")
            end_datetime = datetime.strptime(end_date, "%Y%m%d%H")
        except ValueError:
            raise ParseError("start_date와 end_date 형식을 지켜주세요.(YYYYMMDDHH)")

        if location_code not in LOCATION:
            raise ParseError("location_code는 01~19 사이의 숫자를 입력해주세요.")

        rainfall_controller = RainfallController()
        sewer_controller = SewerController()

        sewers = sewer_controller.call(location_code, start_date, end_date)
        rainfalls = rainfall_controller.call(
            LOCATION[location_code],
            start_datetime,
            end_datetime,
        )

        result = {}
        result["sewers"] = sewers
        result["rainfalls"] = rainfalls
        return Response(result)

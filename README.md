# :test_tube: labq-backend

소비내역을 기록/관리하는 서버

## :scroll: 목차

- [:test_tube: labq-backend](#test_tube-labq-backend)
  - [:scroll: 목차](#scroll-목차)
  - [:notebook_with_decorative_cover: 프로젝트 요구사항](#notebook_with_decorative_cover-프로젝트-요구사항)
  - [:whale: Development(Docker)](#whale-developmentdocker)
  - [:mag_right: Development(Poetry)](#mag_right-developmentpoetry)
  - [:pencil2: Commit Message Convention](#pencil2-commit-message-convention)
  - [:chart_with_upwards_trend: Git Flow / Branch Information](#chart_with_upwards_trend-git-flow--branch-information)
  - [:closed_book: API Docs](#closed_book-api-docs)
    - [하수관 수위/강우량 정보](#하수관-수위강우량-정보)

## :notebook_with_decorative_cover: 프로젝트 요구사항

1. 서울시 하수관로 수위 현황과 강우량 정보 데이터를 수집
2. 출력 값 중 GUBN_NAM과 GU_NAME 기준으로 데이터를 결합
3. 데이터는 JSON으로 전달

- 서울시 하수관로 수위 현황
  - https://data.seoul.go.kr/dataList/OA-2527/S/1/datasetView.do
- 서울시 강우량 정보
  - http://data.seoul.go.kr/dataList/OA-1168/S/1/datasetView.do

## :whale: Development(Docker)

```bash
# Application Run
docker-compose up
```

## :mag_right: Development(Poetry)

```bash
# 가상환경 진입
poetry shell

# 관련 패키지 설치
poetry install

# Application Run
python manage.py runserver
```

## :pencil2: Commit Message Convention

- feat: 기능 추가, 삭제, 변경(or ✨ emoji) - 제품 코드 수정 발생
- fix: 버그 수정(or 🐛 emoji) - 제품 코드 수정 발생
- docs: 문서 추가, 삭제, 변경(or 📝 emoji) - 코드 수정 없음
- style: 코드 형식, 정렬, 주석 등의 변경, eg; 세미콜론 추가(or 💎 emoji) - 제품 코드 수정 발생, 하지만 동작에 영향을 주는 변경은 없음
- refactor: 코드 리펙토링, eg. renaming a variable(or ♻️ emoji) - 제품코드 수정 발생
- test: 테스트 코드 추가, 삭제, 변경 등(or 🧪 emoji) - 제품 코드 수정 없음. 테스트 코드에 관련된 모든 변경에 해당
- chore: 위에 해당하지 않는 모든 변경(or 🧹 emoji), eg. 빌드 스크립트 수정, 패키지 배포 설정 변경 - 코드 수정 없음

위 규칙에 맞게 커밋메시지를 작성한다.

## :chart_with_upwards_trend: Git Flow / Branch Information

```
- main: 제품으로 출시 될 수 있는 브랜치입니다.
- develop: 다음 출시 버전을 개발합니다.
- feature: 다가오는 배포(release)를 위한 새 기능(feature)을 개발합니다.
- release: 새로운 제품 출시 준비를 지원합니다.
- hotfix: 핫픽스는 현재 출시된 제품에 문제가 생겨서 즉각 대응해야하는 상황에서 필요합니다.
```

## :closed_book: API Docs

### 하수관 수위/강우량 정보

| Method | URL               | Description                         |
| ------ | ----------------- | ----------------------------------- |
| GET    | api/v1/rainfalls/ | 하수관 수위/강우량 정보를 확인한다. |

**Query Parameter**

- location_code: 지역코드(01~19)
- start_date: 시작일자(YYYYMMDDHH 형식)
- end_date: 종료일자(YYYYMMDDHH 형식)

**Result**

- Response Example
  ```json
  {
    "sewers": [
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
    "rainfalls": [
      {
        "RAINGAUGE_CODE": 1902.0,
        "RAINGAUGE_NAME": "도림2동P",
        "GU_CODE": 119.0,
        "GU_NAME": "영등포구",
        "RAINFALL10": "0",
        "RECEIVE_TIME": "2022-11-07 14:59"
      }
    ]
  }
  ```

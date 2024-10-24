from .models import WeatherData
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


def data_weatherforecast():
    # 현재 시간 설정
    now = datetime.now()
    input_time = now - timedelta(hours=1)
    base_date = input_time.strftime("%Y%m%d")
    base_time = input_time.strftime("%H00")

    # 10개 지점 좌표 리스트 (위도경도가아니고 기상청에사 사용하는 좌표래유.. )
    locations = [
        {"name": "서울 잠실", "nx": 62, "ny": 126},
        {"name": "수원 KT", "nx": 61, "ny": 121},
        {"name": "문학 SSG", "nx": 55, "ny": 124},
        {"name": "창원 NC", "nx": 89, "ny": 77},
        {"name": "광주 기아", "nx": 59, "ny": 74},
        {"name": "사직 야구장", "nx": 98, "ny": 76},
        {"name": "대구 삼성", "nx": 90, "ny": 90},
        {"name": "대전 한화", "nx": 68, "ny": 100},
        {"name": "고척 키움", "nx": 58, "ny": 125},
        {"name": "제주", "nx": 53, "ny": 38},
    ]

    for location in locations:
        nx = location["nx"]
        ny = location["ny"]
        location_name = location["name"]

        print(f"Fetching data for {location_name} (nx: {nx}, ny: {ny})")

        # API 요청 URL 설정
        url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        params = {
            "serviceKey": os.getenv("WEATHER_API_KEY"),  # 환경변수에서 API 키를 가져옴
            "pageNo": "1",
            "numOfRows": "1000",
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": nx,
            "ny": ny,
        }

        # API 요청
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            continue  
        try:
            data = response.json()
            print(f"응답 데이터: {data}")  # 리스폰스 데이터 출력
        except ValueError:
            continue  

        
        # 받은 데이터에서 필요한 정보 응답>바디>하위정보 
        informations = dict()
        for items in data["response"]["body"]["items"]["item"]:
            cate = items["category"]
            fcstValue = items["obsrValue"]
            informations[cate] = fcstValue

        print(f"추출 데이터: {informations}")  # 추출된 정보 출력

        # 필요한 데이터를 추출하고 저장
        temperature = float(informations.get("T1H", 0.0))  # 기온
        humidity = float(informations.get("REH", 0.0))  # 습도
        wind_speed = float(informations.get("WSD", 0.0))  # 풍속
        wind_direction = deg_to_dir(float(informations.get("VEC", 0.0)))  # 풍향
        rain_status = pyt_code.get(
            int(informations.get("PTY", 0)), "강수 없음"
        )  # 강수 상태
        rain_probability = float(informations.get("POP", 0.0))  # 강수 확률
        sky_status = sky_code.get(int(informations.get("SKY", 0)), "정보 없음")  # 하늘 상태
        precipitation = float(informations.get("PCP", 0.0))  # 강수량
        min_temperature = float(informations.get("TMN", 0.0))  # 최저 기온
        max_temperature = float(informations.get("TMX", 0.0))  # 최고 기온

        print(f"지역 {location_name}: 온도: {temperature}, 습도: {humidity}")

        # 데이터베이스에 저장
        WeatherData.objects.create(
            base_date=base_date,
            base_time=base_time,
            location=location_name,
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            rain_status=rain_status,
            rain_probability=rain_probability,
            sky_status=sky_status,
            precipitation=precipitation,
            min_temperature=min_temperature,
            max_temperature=max_temperature,
        )
        
        # 중복 체크 (base_date와 base_time이 모두 같은 스킵 경우 처리)
        if WeatherData.objects.filter(base_date=base_date, base_time=base_time).exists():
            print(f"중복 데이터 !! : {base_date}, {base_time}. 스킵스킵!!")
    
        print(f"{location_name}의 날씨 데이터 저장 완료.")


# 풍향 변환 함수 (각도를 방위로 변환)
def deg_to_dir(deg):
    deg_code = {
        0: "북",
        360: "북",
        180: "남",
        270: "서",
        90: "동",
        22.5: "북북동",
        45: "북동",
        67.5: "동북동",
        112.5: "동남동",
        135: "남동",
        157.5: "남남동",
        202.5: "남남서",
        225: "남서",
        247.5: "서남서",
        292.5: "서북서",
        315: "북서",
        337.5: "북북서",
    }

    # value를 가장 가까운 방향과 절대값으로 변환
    closest_dir = min(deg_code.keys(), key=lambda x: abs(deg - x))
    return deg_code[closest_dir]


# 강수 형태 코드 변환
pyt_code = {
    0: "강수 없음",
    1: "비",
    2: "비/눈",
    3: "눈",
    5: "빗방울",
    6: "진눈깨비",
    7: "눈날림",
}

#기상상황 >> 최고, 최저,기온.. 하늘상태 안나오나??....
sky_code = {1 : '맑음', 2:'보통', 3 : '구름많음', 4 : '흐림'}

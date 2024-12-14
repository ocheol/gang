# HTTP 요청을 보내기 위해 requests 라이브러리 사용하였다.
import requests 
# JSON 데이터 처리에 필요한 라이브러리이다.
import json      
# 문자열 유사도 계산에 사용되는 difflib 라이브러리이다.
from difflib import get_close_matches  
# API 키 및 기본 설정이다.
# OpenWeatherMap에서 발급받은 API 키이다.
apikey = "39ce00f348bab0f4c0a86507d1fc762d"  
# OpenWeatherMap API에서 사용할 언어 (kr: 한국어)
lang = "kr"  
# 미리 정의된 도시 리스트이다.
# 사용자가 입력한 도시 이름이 잘못된 경우, 이 리스트를 참조하여 유사한 도시 이름을 추천한다.
city_list = [
    "Seoul", "Busan", "Daegu", "Incheon", "Gwangju",
    "Daejeon", "Ulsan", "Jeju", "Tokyo", "New York",
    "Paris", "London"
]# 사용자 입력 단계이다.
# 여러 도시를 쉼표(,)로 구분해서 입력받는다.
# 입력받은 문자열을 쉼표로 나누고 각 도시 이름을 리스트에 저장한다.
cities = input("날씨를 확인할 도시들을 콤마(,)로 구분해서 입력하세요: ").split(",")
# 도시별 날씨를 조회 한다.
# 입력받은 도시 리스트를 하나씩 순회한다.
for city in cities:  
# 도시 이름의 앞뒤 공백 제거한다. (예: " Seoul " -> "Seoul")
    city = city.strip()  
    # 도시 이름이 미리 정의된 리스트에 없는 경우
    if city not in city_list:
        # 입력한 도시와 유사한 도시 이름을 찾는다.
        # get_close_matches 함수: (사용자 입력, 비교 대상 리스트, 최대 추천 개수, 유사도 기준)
        close_matches = get_close_matches(city, city_list, n=1, cutoff=0.6)
        # 유사한 도시 이름이 있는 경우
        if close_matches:
            # 가장 유사한 도시 이름을 출력한다.
            print(f"'{city}'를 찾을 수 없습니다. 혹시 '{close_matches[0]}'을(를) 찾으셨나요?")
            # 추천된 도시 이름을 사용한다.
            city = close_matches[0]
        else:
            # 유사한 도시 이름이 없을 경우 메시지를 출력하고 다음 도시로 넘어간다.
            print(f"'{city}'를 찾을 수 없습니다. 정확한 도시 이름을 입력해주세요.")
            continue  # 현재 루프를 건너뛰고 다음 도시로 이동
    # OpenWeatherMap API URL 생성
    # 사용자 입력(또는 수정된 도시 이름)을 사용하여 API 요청 URL을 생성한다.
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
    # API 요청을 보낸다.
    result = requests.get(api)  # HTTP GET 요청을 통해 날씨 데이터를 가져옴
    # API 응답 상태 코드 확인한다. (200: 성공)
    if result.status_code == 200:
        # 응답 데이터를 JSON 형식으로 변환한다.
        data = json.loads(result.text)
        # 도시 날씨 정보 출력한다.
        print(f"\n{data['name']}의 날씨입니다.")  # 도시 이름 출력
        print("날씨는 ", data["weather"][0]["description"], "입니다.")  # 날씨 설명
        print("현재 온도는 ", data["main"]["temp"], "입니다.")  # 현재 온도
        print("하지만 체감 ", data["main"]["feels_like"], "일 거에요.")  # 체감 온도
        print("최저 기온은 ", data["main"]["temp_min"], "입니다.")  # 최저 기온
        print("최고 기온은 ", data["main"]["temp_max"], "입니다.")  # 최고 기온
        print("습도는 ", data["main"]["humidity"], "입니다.")  # 습도
        print("기압은 ", data["main"]["pressure"], "입니다.")  # 기압
        print("풍향은 ", data["wind"]["deg"], "입니다.")  # 풍향
        print("풍속은 ", data["wind"]["speed"], "입니다.")  # 풍속
        # 날씨 상태에 따른 메시지 출력한다.
	 # 날씨 설명 데이터
        weather_description = data["weather"][0]["description"] 
        # 조건문: 특정 날씨 상태에 따른 메시지 출력한다.
	# "비"라는 단어가 날씨 설명에 포함된 경우
        if "비" in weather_description:  
            print("비가 와요. 우산을 챙겨주세요!")
	# 눈과 비가 동시에 포함된 경우
        elif "눈" in weather_description and "비" in weather_description:  
            print("비 또는 눈이 와요. 따뜻하게 입고 우산을 챙기세요!")
	# "눈"이라는 단어가 포함된 경우
        elif "눈" in weather_description:  
            print("눈이 와요. 장갑을 꼭 챙기세요!")
	# 그 외의 날씨 상태
        else:  
            print("날씨가 좋네요!")
    else:
        # API 요청 실패 시 메시지 출력
        # 예: 잘못된 도시 이름 또는 API 서버 오류
        print(f"\n{city}의 날씨 정보를 가져올 수 없습니다.")


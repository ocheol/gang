import requests
import json

# API 키와 언어 설정
apikey = "39ce00f348bab0f4c0a86507d1fc762d"
lang = "kr"

# 사용자 입력: 여러 도시를 콤마로 구분해 입력받음
cities = input("날씨를 확인할 도시들을 콤마(,)로 구분해서 입력하세요: ").split(",")

# 도시별 날씨 조회
for city in cities:
    city = city.strip()  # 앞뒤 공백 제거
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
    result = requests.get(api)
    
    if result.status_code == 200:  # API 요청 성공 여부 확인
        data = json.loads(result.text)
        
        # 날씨 데이터 출력
        print(f"\n{data['name']}의 날씨입니다.")
        print("날씨는 ", data["weather"][0]["description"], "입니다.")
        print("현재 온도는 ", data["main"]["temp"], "입니다.")
        print("하지만 체감 ", data["main"]["feels_like"], "일 거에요.")
        print("최저 기온은 ", data["main"]["temp_min"], "입니다.")
        print("최고 기온은 ", data["main"]["temp_max"], "입니다.")
        print("습도는 ", data["main"]["humidity"], "입니다.")
        print("기압은 ", data["main"]["pressure"], "입니다.")
        print("풍향은 ", data["wind"]["deg"], "입니다.")
        print("풍속은 ", data["wind"]["speed"], "입니다.")
        
        # 날씨 상태에 따른 메시지 출력
        weather_description = data["weather"][0]["description"]
        
        if "비" in weather_description:
            print("비가 와요. 우산을 챙겨주세요!")
        elif "눈" in weather_description and "비" in weather_description:
            print("비 또는 눈이 와요. 따뜻하게 입고 우산을 챙기세요!")
        elif "눈" in weather_description:
            print("눈이 와요. 장갑을 꼭 챙기세요!")
        else:
            print("날씨가 좋네요!")
    else:
        # API 요청 실패 시 메시지 출력
        print(f"\n{city}의 날씨 정보를 가져올 수 없습니다. 도시 이름을 확인해주세요.")
